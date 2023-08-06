__all__ = ['Trigger', 'TAccept']

from Akuanduba.core import Logger, EnumStringification, NotSet
from Akuanduba.core.messenger.macros import *
from Akuanduba.core import StatusCode, StatusTool,  AkuandubaTool


class TAccept(object):

  def __init__(self):
    import collections
    self._accept = collections.OrderedDict()

  def setResult( self, key, result ):
    self._accept[key] = result

  def getResult(self, key):
    return self._accept[key]

  def getResultOrdered(self):
    return self._accept

  def passedOR(self):
    return any( [ answer for _, answer in self._accept.items() ])

  def passedAND(self):
    return all( [ answer for _, answer in self._accept.items() ])

  def clear(self):
    self._accept.clear()



class Trigger( AkuandubaTool ):

  def __init__(self, name):
    AkuandubaTool.__init__(self, name)
    import collections
    self._hypos = collections.OrderedDict()

  def __add__(self, hypo):
      self._hypos[hypo.name()] = hypo
      return self

  def initialize( self ):
    # Loop over hypos
    for key, hypo in self._hypos.items():

      if hypo.isInitialized(): continue
      MSG_INFO( self, 'Initializing hypothesis test with name: %s', key)
      hypo.setContext( self.getContext() )
      hypo.level = self._level

      if hypo.initialize().isFailure():
        MSG_FATAL( self, "Can not initialize hypothesis %s.", key)

    MSG_INFO( self, "Trigger %s initialization completed.",self.name())
    self.init_lock()
    return StatusCode.SUCCESS


  def execute(self, context):

    MSG_DEBUG(self, 'Running trigger...')

    # get the system flags
    status = self.getContext().getHandler("EventStatus")

    # create the trigger object
    accept = TAccept()

    # Tools
    for key, hypo in self._hypos.items():

      MSG_DEBUG( self, "Execute hypo %s", hypo.name())

      if( hypo.execute_r( self.getContext(), accept ).isFailure() ):
        MSG_WARNING( self, "Impossible to execute %s.", tool.name())


    if not accept.passedOR():
      # stop the tool stack execution.
      MSG_DEBUG( self, "Sending stop signal for the tools stack.")
      status.forceStop()
    else:
      MSG_INFO( self, '%s triggered!',self.name())


    return StatusCode.SUCCESS


  def finalize(self):
    # Services
    for key, hypo in self._hypos.items():
      if( hypo.finalize().isFailure() ):
        MSG_WARNING( self, "Impossible to execute %s.", hypo.name())
        return StatusCode.FAILURE
    self.fina_lock()
    return StatusCode.SUCCESS