from unittest import TestCase

from dm.reuse import rebindFunction


## Elementary tests
from . import _DataHelper, _LargeDataHelper

class DataHelperTests(TestCase):
  CLS = _DataHelper
  DATA = dict(a="A", b="B")

  def setUp(self):
    self.data = data = self.CLS()
    data.update(self.DATA)

  def test_read_access(self):
    data = self.data
    self.assertEqual(len(data), len(self.DATA))
    self.assertTrue("a" in data)
    self.assertTrue("x" not in data)
    self.assertEqual(data["a"], "A")
    self.assertEqual(sorted(data.keys()), ["a", "b"])
    self.assertEqual(sorted(data.values()), ["A", "B"])
    self.assertEqual(sorted(data.items()), [("a", "A"), ("b", "B")])
    self.assertIsNone(data.get("x"))
    self.assertIs(data.get("x", data), data)

  def test_setitem(self):
    data = self.data
    data["a"] = "X"
    self.assertEqual(len(data), 2)
    self.assertEqual(data["a"], "X")
    data["x"] = "X"
    self.assertEqual(len(data), 3)
    self.assertEqual(data["x"], "X")

  def test_delitem(self):
    data = self.data
    with self.assertRaises(KeyError):
      del data["x"]
    self.assertEqual(len(data), 2)
    del data["a"]
    self.assertEqual(len(data), 1)
    self.assertIsNone(data.get("a"))

  def test_pop(self):
    data = self.data
    self.assertEqual(data.pop("a"), "A")
    self.assertEqual(len(data), 1)
    with self.assertRaises(KeyError): data.pop("a")
    self.assertEqual(len(data), 1)
    self.assertIsNone(data.pop("a", None))
    self.assertEqual(len(data), 1)

  def test_setdefault(self):
    data = self.data
    self.assertEqual(data.setdefault("a", "X"), "A")
    self.assertEqual(len(data), 2)
    self.assertEqual(data.setdefault("x", "X"), "X")
    self.assertEqual(len(data), 3)
    self.assertEqual(data["x"], "X")

  def test_clear(self):
    data = self.data
    data.clear()
    self.assertEqual(list(data.keys()), [])
    self.assertEqual(len(data), 0)

  def test_update(self):
    data = self.data
    data.update(dict(a="a", x="x"))
    self.assertEqual(sorted(data.items()),
                     [("a", "a"), ("b", "B"), ("x", "x")])
    self.assertEqual(len(data), 3)


class LargeDataHelperTests(DataHelperTests):
  CLS = _LargeDataHelper

  def test_len(self):
    data = self.data; length = data._LargeDataHelper__length
    self.assertEqual(length(), 2)
    length.change(1)
    self.assertEqual(len(data), 3)


## Container tests
# We use a global timer and sleeper.
#   The timer and sleeper are reset before each test

from . import Container, Session, \
     SessionCreatedEvent, \
     MaximalSessionNumberExceededEvent, SessionCleanupEvent, \
     MaximalSessionNumberExceededError


class Timer(object):
  """An externally controllable timer."""
  def __init__(self): self.time = 0
  def __call__(self): return self.time
  reset = __init__
timer = Timer()

class TestSession(Session):
  __init__ = rebindFunction(Session.__init__, time=timer)

class TestContainer(Container):
  cleanup_external = True # suppress automatic cleanup
  __init__ = rebindFunction(Container.__init__, time=timer)
  new_or_existing = rebindFunction(Container.new_or_existing,
                                   time=timer, Session=TestSession)
  _cleanup = rebindFunction(Container._cleanup, time=timer)
  _update_lc_ = rebindFunction(Container._update_lc_, time=timer)

  

from zope import event
class EventHandler(object):
  def __init__(self): self.events = []
  def __call__(self, event): self.events.append(event)

class ContainerTestsBase(TestCase):
  def setUp(self):
    self.subscribers = event.subscribers
    self.event_handler = EventHandler()
    self.events = self.event_handler.events
    event.subscribers = [self.event_handler]
    timer.reset()
    self.container = TestContainer()

  def tearDown(self):
    event.subscribers = self.subscribers


class ContainerTests(ContainerTestsBase):
  def test_new_or_existing(self):
    container = self.container
    s = container.new_or_existing("")
    self.assertEqual(len(self.events), 1)
    self.assertIsInstance(self.events[0], SessionCreatedEvent)
    self.assertIs(self.events[0].object, s.aq_base)
    ns = container.new_or_existing("")
    self.assertEqual(len(self.events), 1)
    self.assertIs(s.aq_base, ns.aq_base)

  def test_max_session_number(self):
    container = self.container
    container.session_max_number = 1
    container.new_or_existing("1")
    with self.assertRaises(MaximalSessionNumberExceededError):
      container.new_or_existing("2")
    self.assertEqual(len(container), 1)
    self.assertIsInstance(self.events[1], MaximalSessionNumberExceededEvent)
    self.assertIs(self.events[1].object, container)

  def test_max_session_lifetime(self):
    container = self.container
    self.assertEqual(container.lifetime, 0)
    container.session_max_lifetime_min = 1
    self.assertEqual(container.lifetime, 60)
    s = container.new_or_existing("")
    ns = container.new_or_existing("")
    self.assertIs(s.aq_base, ns.aq_base)
    timer.time = 61
    ns = container.new_or_existing("")
    self.assertIsNot(s.aq_base, ns.aq_base)

  def test_resolution(self):
    container = self.container
    self.assertEqual(container.resolution, 0)
    container.session_timeout_min = 1
    self.assertEqual(container.resolution, 8)
    container.session_access_time_resolution_min = 1
    self.assertEqual(container.resolution, 8)
    container.session_timeout_min = 10
    self.assertEqual(container.resolution, 60)
    container.session_timeout_min = 0
    self.assertEqual(container.resolution, 60)
    s = container.new_or_existing("")
    self.assertEqual(s.last_access, 0)
    timer.time = 60
    s = container.new_or_existing("")
    self.assertEqual(s.last_access, 0)
    timer.time = 61
    s = container.new_or_existing("")
    self.assertEqual(s.last_access, 61)

  def test_period(self):
    container = self.container
    self.assertEqual(container.period, 10)
    container.cleanup_period_sec = -1
    self.assertEqual(container.period, 10)
    container.cleanup_period_sec = 1
    self.assertEqual(container.period, 1)

  def test_cleanup_timeout(self):
    container = self.container
    container.session_timeout_min = 1
    for i in range(5):
      timer.time = 30 * i
      container.new_or_existing(str(i))
    container._cleanup()
    self.assertNotIn("0", container)
    self.assertIn("4", container)
    timer.time = 500
    container.new_or_existing("4")
    container._cleanup()
    self.assertEqual(len(container), 1)
    self.assertIn("4", container)

  def test_cleanup_lifetime(self):
    container = self.container
    container.session_max_lifetime_min = 1
    for i in range(5):
      timer.time = 30 * i
      container.new_or_existing(str(i))
    container.new_or_existing("0")
    container._cleanup()
    self.assertIn("0", container)
    self.assertNotIn("1", container)
    self.assertIn("4", container)

  def test_cleanup_target_number(self):
    container = self.container
    container.session_target_number = 2
    for i in range(5):
      timer.time = 30 * i
      container.new_or_existing(str(i))
    container.new_or_existing("0")
    container._cleanup()
    self.assertNotIn("0", container)
    self.assertIn("4", container)
    self.assertEqual(len(container), 2)

  def test_cleanup_time(self):
    container = self.container
    self.assertEqual(container._last_cleanup.value, 0)
    timer.time = 60
    container._cleanup()
    self.assertEqual(container._last_cleanup.value, 60)

  def test_cleanup_event(self):
    container = self.container
    container._cleanup()
    self.assertIsInstance(self.events[0], SessionCleanupEvent)
    self.assertIs(self.events[0].object, container)

  def test_bucketed_delete_sessions(self):
    container = self.container
    bds = container._bucketed_delete_sessions
    any = lambda s: True
    # empty
    bds(any); self.assertEqual(len(container), 0)
    # bucket
    container.new_or_existing("0")
    bds(any); self.assertEqual(len(container), 0)
    # real tree
    for i in range(200): container.new_or_existing(str(i))
    bds(any); self.assertEqual(len(container), 0)


## `start_cleanup` tests
from threading import Condition
from time import sleep

from ZODB.DemoStorage import DemoStorage
from ZODB.DB import DB
from transaction import commit

class Sleeper(object):
  """A `sleep` implementation which allows external wakeup."""
  def __init__(self): self.cond = Condition()

  def wait(self): return self.cond.wait()
  def notify_all(self): return self.cond.notify_all()
  def notify(self, no=1): return self.cond.notify(no)
  def __enter__(self): return self.cond.__enter__()
  def __exit__(self, *args): return self.cond.__exit__(*args)

  def sleep(self, unused):
    with self: self.wait()

  def wakeup(self, no=1):
    with self: self.notify(no)

  def reset(self):
    with self: self.notify_all()
    self.__init__()
sleeper = Sleeper()

from . import start_cleanup, Cleanup, _cleanup_reg, LockError

class StartCleanupTests(ContainerTestsBase):
  def setUp(self):
    super(StartCleanupTests, self).setUp()
    self.container.id = "sessions"
    sleeper.reset()
    self.sleeper=sleeper
    class TestCleanup(Cleanup): pass
    TestCleanup.run = rebindFunction(
      Cleanup.__dict__["run"],
      sleep=self.sleeper.sleep
      )
    self.wakeup = self.sleeper.wakeup
    self.start = rebindFunction(start_cleanup, Cleanup=TestCleanup, time=timer)

  def tearDown(self):
    for cl in _cleanup_reg.values(): cl.lf.close()
    _cleanup_reg.clear()
    sleeper.wakeup(10)
    sleep(0.1) # external thread
    super(StartCleanupTests, self).tearDown()

  def test_periodic_and_lock(self):
    container = self.container
    fn = container.get_lock_file_name()
    self.start(container)
    sleep(0.1) # external thread
    self.assertEqual(len(self.events), 1)
    self.wakeup()
    sleep(0.1) # external thread
    self.assertEqual(len(self.events), 2)
    with self.assertRaises(LockError): self.start(container)
    cl = _cleanup_reg[fn]
    cl.serial = "1"
    self.start(container)
    sleep(0.1) # external thread
    self.assertEqual(len(self.events), 3)
    self.wakeup(2)
    sleep(0.1) # external thread
    self.assertEqual(len(self.events), 4) # only one round

  def test_zodb(self):
    container = self.container
    db = DB(DemoStorage())
    conn = db.open()
    root = conn.root()
    root["container"] = container
    commit()
    self.start(container)
    sleep(0.1) # external thread
    cc = self.events[0].object
    self.assertEqual(cc._p_oid, container._p_oid)
    self.assertIsNot(cc, container)


## Session tests
from AccessControl.ZopeGuards import get_safe_globals
from RestrictedPython import compile_restricted_function
from six import exec_

from . import Session

class SessionTests(TestCase):
  def test_unauthenticated_access(self):
    s = Session("")
    s["a"] = "A"
    c = compile_restricted_function(
      "s",
      body="""\
s["a"]
s["x"] = "X"
s.set("y", "Y")
for i in s: pass
for it in s.items(): pass
for v in s.values(): pass
s.keys()
s.values()
s.items()
s.pop("x")
del s["a"]
s.update({"a":"A", "z":"Z"})
s.delete("z")
""",
      name="f",
      filename="<string>",
      )
    self.assertEqual(c[1], ())
    g = get_safe_globals(); l = {}
    # Zope 2.13 compatibility
    from AccessControl.ZopeGuards import guarded_getattr
    g["_getattr_"] = guarded_getattr
    exec_(c[0], g, l)
    f = l["f"]
    f(s)
    self.assertEqual(sorted(s.keys()), ["a", "y"])


