from zope.component.interfaces import IObjectEvent
from zope.interface.common.mapping import IMapping, IWriteMapping
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.schema import Float, Date


class ISessionContainer(IMapping):
  """Session container with `IMapping` access to the session objects."""
  def __delitem__(key): "delete the corresponding key"

  def new_or_existing(key):
    """return existing session with *key* or create one."""


class ISession(IMapping, IWriteMapping):
  created = Float(description=u"creation time in seconds since epoch")
  created_date = Date(description=u"creation time as `DateTime`",
                      readonly=True)
  last_access = Float(description=u"last access time in seconds since epoch."
                      u"Attention: limited resolution",
                      readonly=True)
  last_access_date = Date(description=u"last access time as `DateTime`."
                          u"Attention: limited resolution",
                          readonly=True)


class ISessionCreatedEvent(IObjectEvent):
  """A new session has been created.

  This event can be used to monitor session creation and
  help detect denial of service attacks.
  """

class IMaximalSessionNumberExceededEvent(IObjectEvent):
  """Event to indicate that the maximal session number has been exceeded.

  The associated object is the affected session container.

  This event can (e.g.) be used to trigger the detection of
  a denial of service attack and potentially delete sessions.
  """


class ISessionCleanupEvent(IObjectEvent):
  """Event notified during a cleanup run.

  The associated object is the affected session container.

  The event can be used to implement custom cleanup
  operations, e.g. check for suspicious sessions and
  delete or modify them. Examples are the detection
  of a DOS attacks or the enforcement of "one session per
  authenticated user" policy.

  The corresponding handler is executed in a separate thread: the
  typical Zope request context does not exist.
  """



class MaximalSessionNumberExceededError(Exception):
  """Exception to indicate that the maximal session number is exceeded."""
