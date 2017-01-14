# NOTE: Borrowed basically all of this from Gosa project.

import sys

try:
    # import pydbus
    from pydbus import SessionBus

except ImportError:
    print("Please install the python dbus module.")
    sys.exit(1)

import time
import threading
import logging
from scarlett_os.internal.gi import GLib

logger = logging.getLogger(__name__)

# from pydbus import SessionBus
# bus = SessionBus()
# bus.own_name(name='org.scarlett')
# sl = ScarlettListener(bus=bus.con, path='/org/scarlett/Listener')
#
# In [1]: from scarlett_os.internal.dbus_runner import DBusRunner
#
# In [2]: _dr = DBusRunner.get_instance()
#
# In [3]: _dr
# Out[3]: <scarlett_os.internal.dbus_runner.DBusRunner at 0x7fa552e8e468>
#
# In [4]: dir(_dr)
# Out[4]:
# ['_DBusRunner__active',
#  '_DBusRunner__bus',
#  '_DBusRunner__instance',
#  '_DBusRunner__runner',
#  '__class__',
#  '__delattr__',
#  '__dict__',
#  '__dir__',
#  '__doc__',
#  '__eq__',
#  '__format__',
#  '__ge__',
#  '__getattribute__',
#  '__gt__',
#  '__hash__',
#  '__init__',
#  '__le__',
#  '__lt__',
#  '__module__',
#  '__ne__',
#  '__new__',
#  '__reduce__',
#  '__reduce_ex__',
#  '__repr__',
#  '__setattr__',
#  '__sizeof__',
#  '__str__',
#  '__subclasshook__',
#  '__weakref__',
#  'get_instance',
#  'get_session_bus',
#  'is_active',
#  'start',
#  'stop']

# In [5]: _session = _dr.get_session_bus()

# In [6]: _session
# Out[6]: <pydbus.bus.Bus at 0x7fa552e8ef60>

# In [7]: _session.request_name('org.scarlett')
# Out[7]: <pydbus.request_name.NameOwner at 0x7fa55a0e1bb8>

# In [8]:


class DBusRunner(object):
    """
    The *DBusRunner* module acts as a singleton for the DBUS system
    bus. Interested instances can obtain the system bus from the
    runner.
    """
    __bus = None
    __active = False
    __instance = None

    def __init__(self):
        DBusRunner.__bus = SessionBus()

    def start(self):
        """
        Start the :func:`gi.MainLoop` to establish DBUS communications.
        """
        if self.__active:
            return

        self.__active = True

        self.__thread = threading.Thread(target=self.__runner)
        self.__thread.daemon = True
        self.__thread.start()

    def __runner(self):
        self.__gloop = GLib.MainLoop()
        try:
            self.__gloop.run()
            context = self.__gloop.get_context()
            while self.__active:
                context.iteration(False)
                if not context.pending():
                    time.sleep(.1)
        except KeyboardInterrupt:
            self.__active = False
            # env = Environment.getInstance()
            # if hasattr(env, "active"):
            #     env.active = False

    def stop(self):
        """
        Stop the :func:`gobject.MainLoop` to shut down DBUS communications.
        """
        # Don't stop us twice
        if not self.__active:
            return

        self.__active = False
        self.__gloop.quit()
        self.__thread.join(5)

    def get_session_bus(self):
        """
        Return the current DBUS session bus.

        ``Return:`` DBusRunner bus object
        """

        # pydbus.bus.Bus at 0x7fa552e8ef60
        return DBusRunner.__bus

    def is_active(self):
        """
        Return the current DBUS session bus.

        ``Return:`` Bool value
        """
        return self.__active

    @staticmethod
    def get_instance():
        """
        Singleton to return a DBusRunner object.

        ``Return:`` :class:`scarlett_os.internal.dbus_runner.DBusRunner`
        """
        if not DBusRunner.__instance:
            DBusRunner.__instance = DBusRunner()
        return DBusRunner.__instance
