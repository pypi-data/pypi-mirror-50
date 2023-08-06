"""Conflict reduced sessions for Zope."""
from collections import MutableMapping
from heapq import nsmallest
from logging import getLogger
from os.path import join
from threading import Thread
from time import time, sleep
from weakref import WeakValueDictionary

from BTrees.Length import Length
from BTrees.OOBTree import OOBTree
from transaction.interfaces import TransientError

from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from Acquisition import Implicit
from App.config import getConfiguration
from DateTime import DateTime
from ExtensionClass import Base
from OFS.PropertyManager import PropertyManager
from OFS.SimpleItem import SimpleItem
from Persistence import Persistent
from transaction import abort, savepoint
from zope.component.interfaces import ObjectEvent
from zope.event import notify
from zope.interface import implementer
from zope.lifecycleevent import ObjectCreatedEvent

from dm.zodb.asynchronous.zope2 import transactional
from dm.zope.generate.constructor import add_form_factory, add_action_factory

from zc.lockfile import LockFile, LockError

from .interfaces import ISessionContainer, ISession, \
     ISessionCreatedEvent, ISessionCleanupEvent, \
     IMaximalSessionNumberExceededEvent, MaximalSessionNumberExceededError


logger = getLogger(__name__)


class _DataHelper(object):
  """Mixin class to provide ``OOBTree`` based data.

  We would like to inherit from ``MutableMapping`` here
  but we can't due to a metaclass clash below. Instead
  we delegate its methods to the data.
  """
  def __init__(self):
    self.__data = OOBTree()

  def delegate_to_data(self, name):
    return getattr(self.__data, name)

class _Delegator(object):
  def __init__(self, name): self.__name = name

  def __get__(self, obj, type):
    return self if obj is None else obj.delegate_to_data(self.__name)

for _ in dir(MutableMapping):
  if not hasattr(_DataHelper, _) and hasattr(OOBTree, _):
    setattr(_DataHelper, _, _Delegator(_))


class _LargeDataHelper(_DataHelper):
  """``_DataHelper`` with local length (for efficiency)."""
  def __init__(self):
    _DataHelper.__init__(self)
    self.__length = Length()

  def __len__(self): return self.__length()

  def __setitem__(self, k, v):
    missing = k not in self
    super(_LargeDataHelper, self).__setitem__(k, v)
    if missing: self.__length.change(1)

  def __delitem__(self, k):
    super(_LargeDataHelper, self).__delitem__(k)
    self.__length.change(-1)

  def pop(self, k, *args):
    try:
      v = super(_LargeDataHelper, self).pop(k)
      self.__length.change(-1)
      return v
    except KeyError:
      if args: return args[0]
      raise

  def setdefault(self, k, d):
    if k in self: return self[k]
    self[k] = d
    return d

  def clear(self):
    super(_LargeDataHelper, self).clear()
    self.__length.set(0)

  def update(self, d):
    super(_LargeDataHelper, self).update(d)
    self.__length.set(super(_LargeDataHelper, self).__len__())
  


@implementer(ISessionContainer)
class Container(SimpleItem, PropertyManager, _LargeDataHelper):
  """Session (data) container."""
  meta_type = "dm.zope.session:Container"

  manage_options = SimpleItem.manage_options + PropertyManager.manage_options

  _properties = PropertyManager._properties + (
    dict(id="session_timeout_min", type="int", mode="w",
         label="session timeout in minutes",
         description="session is deleted after an inactivity of this " 
                     "duration; 0 means unlimited."
         ),
    dict(id="session_access_time_resolution_min", type="int", mode="w",
         label="session access time resolution in minutes.",
         description="0 means a huge value. "
                     "The effective resolution is the minimum of the "
                     "value specified by this option and about "
                     "1/8 of of the session timeout.",
         ),
    dict(id="session_max_lifetime_min", type="int", mode="w",
         label="maximal session lifetime in minutes",
         description="the session becomes invalid after this many minutes; "
                     "0 means unlimited.",
         ),
    dict(id="session_target_number", type="int", mode="w",
         label="target session number",
         description="periodic cleanup tries to keep the session number below "
                     "this threshold by deleting the oldest sessions. "
                     "0 means deactivate this feature",
         ),
    dict(id="session_max_number", type="int", mode="w",
         label="maximal session number",
         description="the session number is not allowed to exceed this value. "
                     "0 means unlimited.",
         ),
    dict(id="cleanup_period_sec", type="int", mode="w",
         label="cleanup period in seconds",
         description="period with which invalid or outdated sessions "
                     "are removed or old sessions are "
                     "deleted to stay below the session target number. "
                     "A value <= 0 effectively results in 10. "
                     "If you change this value and the cleanup is performed "
                     "externally, then the change might only become effective "
                     "only with a delay, unless you restart the external "
                     "process.",
         ),
##    dict(id="cleanup_external", type="boolean", mode="w",
##         label="cleanup via external process",
##         description="indicates that the cleanup is not performed by an "
##                     "external process (you must start and supervise) "
##                     "and not internally. You should use this feature "
##                     "in a ZEO setup to avoid that concurrent cleanups "
##                     "are performed by different ZEO clients.",
##         ),
    dict(id="session_number", type="int", mode="r",
          label="session number",
          ),
    dict(id="last_cleanup_date", type="date", mode="r",
          label="last cleanup date",
          ),
    )

  session_timeout_min = session_max_lifetime_min \
                      = session_access_time_resolution_min = 0
  session_target_number = 5000
  session_max_number = 10000
  cleanup_period_sec = 10
  cleanup_external = False

  @property
  def session_number(self): return len(self)

  @session_number.setter
  def session_number(self, value): pass

  @property
  def last_cleanup_date(self): return DateTime(self._last_cleanup.value)

  @last_cleanup_date.setter
  def last_cleanup_date(self, value): pass


  def __init__(self):
    super(Container, self).__init__()
    self._last_cleanup = _Max(time())

  __len__ = _LargeDataHelper.__len__

  def new_or_existing(self, key):
    now = time()
    if not self.cleanup_external: start_cleanup(self, False)
    s = self.get(key)
    if s is None:
      if self.session_max_number > 0 and len(self) >= self.session_max_number:
        notify(MaximalSessionNumberExceededEvent(self))
        if len(self) >= self.session_max_number:
          raise MaximalSessionNumberExceededError(self)
      s = self[key] = Session(key)
    else:
      lt = self.lifetime
      if lt > 0 \
             and now > s.created + lt:
        s = self[key] = Session(key)
      else:
        r = self.resolution
        if r > 0 \
           and now - s._last_access.value > r:
          s._last_access.set(now)
    return s.__of__(self)

  _v_lfn = None # may need to register a `MoveEvent` handler to clear
  def get_lock_file_name(self):
    fn = self._v_lfn
    if fn is None:
      fn = self._v_lfn = join(
        getConfiguration().clienthome,
        self.absolute_url(1).replace("/", "-") + ".lock"
        )
    return fn

  @property
  def period(self):
    """the effective cleanup period in seconds."""
    p = self.cleanup_period_sec
    return p if p > 0 else 10

  @property
  def timeout(self):
    """session timeout in seconds."""
    st = self.session_timeout_min
    return 60 * st if st > 0 else 0

  @property
  def lifetime(self):
    """session maximal lifetime in seconds."""
    lt = self.session_max_lifetime_min
    return 60 * lt if lt > 0 else 0

  @property
  def resolution(self):
    r = self.session_access_time_resolution_min
    st = self.session_timeout_min
    if r <= 0: return st << 3 if st > 0 else 0
    r *= 60
    if st <= 0: return r
    st <<= 3
    return r if r <= st else st

  # ATTENTION: the methods below are called in a separate thread
  #   Most Zope services are unavailable
  def _cleanup(self):
    """implement a cleanup round."""
    sno = len(self)
    now = time()
    logger.debug("starting session cleanup")
    timeout = self.timeout
    mlt = self.lifetime
    if timeout or mlt:
      def deactivate(s):
        return (timeout and s._last_access.value + timeout < now
                or mlt and s.created + mlt < now)
      self._bucketed_delete_sessions(deactivate)
    stn = self.session_target_number
    if stn > 0 and len(self) > stn:
      dno = len(self) - stn
      created = lambda s: s.created
      to_del = nsmallest(dno, self.values(), created) if dno < 100 \
               else sorted(self.values(), created)[:dno]
      to_del = set(s.id for s in to_del)
      self._bucketed_delete_sessions(lambda s, ss=to_del: s.id in ss)
    self._notify_cleanup()
    self._update_lc()
    logger.debug("session cleanup finished: "
                 "start session no %s, end session no %s", sno, len(self))

  @transactional
  def _delete_sessions(self, sessions):
    for s in sessions:
      cs = self.get(s.id)
      if cs is None \
         or cs.created != s.created \
         or cs._last_access.value != s._last_access.value:
        continue # session changed
      del self[s.id]

  def _bucketed_delete_sessions(self, filter):
    """delet bucket wisee sessions identified by *filter*.

    Each bucket is processed in its own transaction
    (to get small transactions).
    """
    state = self.delegate_to_data("__getstate__")()
    if state is not None:
      mapping = self if len(state) == 1 else state[1]
      del_chunks = []
      while mapping:
        to_del = []
        for s in mapping.values():
          if filter(s): to_del.append(s)
        if to_del:
          del_chunks.append(to_del)
        mapping = getattr(mapping, "_next", None)
      for to_del in del_chunks: self._delete_sessions(to_del)
    

  @transactional
  def _notify_cleanup(self):
    try: notify(SessionCleanupEvent(self))
    except TransientError: raise
    except Exception:
      logger.exception("unexpected exception in session cleanup event handler")

  # to facilitate testing
  def _update_lc_(self): self._last_cleanup.set(time())
  @transactional
  def _update_lc(self): self._update_lc_()

    

@implementer(ISession)
class Session(Implicit, _DataHelper):
  """A session object.

  Currently based on `BTrees.OOBTree.OOBTree`.
  We might want to use our own data container to get a less
  conservative conflict resolution.
  """
  security = ClassSecurityInfo()
  security.setDefaultAccess('allow')
  security.declareObjectPublic()

  def __init__(self, key):
    _DataHelper.__init__(self)
    self.id = key
    now = time()
    self.created = now
    self._last_access = _Max(now)
    notify(SessionCreatedEvent(self))

  @property
  def last_access(self): return self._last_access.value

  @property
  def created_date(self): return DateTime(self.created)

  @property
  def last_access_date(self): return DateTime(self._last_access.value)

  @property
  def token(self): return self.id

  # TTW (copied from `Products.Transience.TransientObject.TransientObject`)
  set = __guarded_setitem__ = _DataHelper.__setitem__
  delete = __guarded_delitem__ = _DataHelper.__delitem__



class _Max(Persistent):
  def __init__(self, val): self.value = val

  def set(self, val): self.value = max(self.value, val)

  def _p_resolveConflict(self, old, s1, s2): return max(s1, s2)


# cleanup
_cleanup_reg = WeakValueDictionary()

def start_cleanup(container, exc=True):
  fn = container.get_lock_file_name()
  cl = _cleanup_reg.get(fn)
  start = False
  if cl is not None:
    # we are responsible for the cleanup
    if cl.serial != container._p_serial:
      try:
        cl.lf.close()
        start = True
      except: pass # raise condition possible
  else:
    start = container._last_cleanup.value + (container.period << 1) < time()
  if exc or start:
    try:
      cl = _cleanup_reg[fn] = Cleanup(fn, container)
    except LockError:
      if exc: raise
      return # someone else is doing the cleanup
    cl.start()

InitializeClass(Session)




class Cleanup(Thread):
  container = None

  def __init__(self, fn, container):
    self.fn = fn
    self.lf = LockFile(fn)
    self.serial = container._p_serial
    if container._p_jar is None:
      savepoint()
    # to ease testing
    if container._p_jar is None: self.container = container
    else:
      self.db = container._p_jar.db()
      self.oid = container._p_oid
    Thread.__init__(self)

  def run(self):
    conn = None
    container = self.container
    if container is None:
      conn = self.db.open()
      container = conn[self.oid]
    try:
      while True:
        if _cleanup_reg.get(self.fn) is not self: break
        abort() # allow new state to be seen
        try:
          container._cleanup()
        except TransientError:
          logger.exception("unexpected conflict -- continuing")
          pass
        except Exception:
          logger.critical("unexpected exception -- giving up", exc_info=True)
          raise
        sleep(container.period)
    finally:
      if conn is not None: conn.close()
      try: self.lf.close()
      except Exception: pass


def initialize(context):
  context.registerClass(
    Container,
    constructors=(add_form_factory(Container), add_action_factory(Container)),
    )


@implementer(ISessionCreatedEvent)
class SessionCreatedEvent(ObjectCreatedEvent): pass


@implementer(IMaximalSessionNumberExceededEvent)
class MaximalSessionNumberExceededEvent(ObjectEvent): pass


@implementer(ISessionCleanupEvent)
class SessionCleanupEvent(ObjectEvent): pass
