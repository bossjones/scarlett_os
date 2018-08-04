# NOTE: Borrowed basically all of this from Gosa project.

import sys

try:
    import pydbus
    from pydbus import SessionBus

except ImportError:
    print("Please install the python dbus module.")
    sys.exit(1)

import time
import threading
import logging
from scarlett_os.internal.gi import GLib

logger = logging.getLogger(__name__)

# DBUS_SESSION_BUS_ADDRESS=unix:abstract=/tmp/dbus-AmtpYxooYR,guid=c32e70e0207846dc470144d3587a6283

# from pydbus import SessionBus
# bus = SessionBus()
#
# In [3]: bus
# Out[3]: <pydbus.bus.Bus at 0x7fb8f407dae8>

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
    # __proxy = None
    __timeout = 30
    __attempts = 0
    __bus_name = "org.scarlett"
    __object_path = "/org/scarlett/Listener"
    __default_interface = "org.scarlett.Listener"
    __scarlett_dbus = None

    def __init__(self):
        # FIXME: Temporarily disabled
        # DBusRunner.__bus = SessionBus()
        self.configure_session_bus()
        # self.bus_name = DBusRunner.__bus_name
        # self.object_path = DBusRunner.__object_path
        # self.default_interface = DBusRunner.__default_interface
        # FIXME: Break out dbus proxy object into classes that need them
        # DBusRunner.__proxy = DBusRunner.__bus.get("org.scarlett", object_path='/org/scarlett/Listener')

        # self._id_dbus_watch_name = self.bus.watch_name("org.scarlett",
        #                                                name_appeared=self._on_name_appeared, name_vanished=self._on_name_vanished)

    def configure_session_bus(self, attempts=0):
        while attempts < 5:
            try:
                DBusRunner.__bus = SessionBus()
                time.sleep(0.3)
                break
            except Exception as e:
                attempts += 1
                logger.error(
                    "Error getting Session Bus %d: %s" % (e.args[0], e.args[1])
                )

    def configure_dbus_proxy(self, attempts=0):
        while attempts < 5:
            try:
                self.__scarlett_dbus = self.__bus.get(
                    "org.scarlett", "/org/scarlett/Listener"
                )
                time.sleep(0.3)
                break
            except Exception as e:
                attempts += 1
                logger.error(
                    "Scarlett DBusRunner Error %d: %s" % (e.args[0], e.args[1])
                )

    @property
    def bus(self):
        """Get the Bus Object"""
        if self.__bus is None:
            return None
        return self.__bus

    @bus.setter
    def bus(self, bus_obj):
        """Set the Bus Object
        """
        if bus_obj is None:
            self.__bus = None
            return
        else:
            if type(bus_obj) == pydbus.bus.Bus:
                self.__bus = bus_obj
            else:
                raise ValueError("bus_obj '{0} must be of type pydbus.bus.Bus'")

    @property
    def scarlett_dbus(self):
        """Get the scarlett dbus proxy object"""
        if self.__scarlett_dbus is None:
            return None
        return self.__scarlett_dbus

    @scarlett_dbus.setter
    def scarlett_dbus(self, s_dbus):
        """Set the scarlett dbus proxy Object
        """
        if s_dbus is None:
            self.__scarlett_dbus = None
            return
        else:
            # Check that proxy object has a Introspect method
            proxy_obj = getattr(s_dbus, "Introspect")
            if callable(proxy_obj.Introspect):
                self.__scarlett_dbus = s_dbus
            else:
                raise ValueError(
                    "proxy_obj.Introspect '{0} is not callable. Something wrong with proxy object!'"
                )

    @property
    def bus_name(self):
        """Get the bus name"""
        if self._bus_name is None:
            return None
        return self._bus_name

    @bus_name.setter
    def bus_name(self, bus_name):
        r"""Set the Bus Name
        http://dbus.freedesktop.org/doc/dbus-specification.html\
        #message-protocol-names-bus
        """
        if bus_name is None:
            self._bus_name = None
            return
        bus = str(bus_name)
        self._bus_name = bus

    @property
    def object_path(self):
        """Get the object path"""
        return self._object_path

    @object_path.setter
    def object_path(self, object_path):
        r"""Set the object_path
        http://dbus.freedesktop.org/doc/dbus-specification.html\
        #message-protocol-marshaling-object-path
        """
        if not object_path:
            raise ValueError("object_path '{0} cannot be blank'")
        else:
            obj = str(object_path)
            if obj[0] == "/":
                self._object_path = obj
            else:
                raise ValueError(
                    "object_path must follow specifications"
                    " mentioned at "
                    "http://dbus.freedesktop.org/doc/"
                    "dbus-specification.html"
                    "#message-protocol-marshaling-object-path"
                    ""
                )

    @property
    def default_interface(self):
        """Get the default interface"""
        return self._default_interface

    @default_interface.setter
    def default_interface(self, default_interface):
        r"""Set the default_interface
        http://dbus.freedesktop.org/doc/dbus-specification.html\
        #message-protocol-names-interface
        """
        if not default_interface:
            raise ValueError("default_interface '{0} cannot be blank'")
        else:
            intr = str(default_interface)
            if intr.count(".") > 1:
                self._default_interface = intr
            else:
                raise ValueError(
                    "default_interface must follow "
                    "specifications mentioned at "
                    "http://dbus.freedesktop.org/"
                    "doc/dbus-specification.html"
                    "#message-protocol-names-interface"
                )

    # def wait_for_bus_object(self, dest, path):
    #     # we check whether the name is owned first, to avoid race conditions
    #     # with service activation; once it's owned, wait until we can actually
    #     # call methods
    #     while DBusRunner.__timeout > 0:
    #         if bus.name_has_owner(dest):
    #             try:
    #                 p = dbus.Interface(bus.get_object(dest, path),
    #                                    dbus_interface=dbus.INTROSPECTABLE_IFACE)
    #                 p.Introspect()
    #                 break
    #             except dbus.exceptions.DBusException as e:
    #                 last_exc = e
    #                 if '.UnknownInterface' in str(e):
    #                     break
    #                 pass
    #
    #         timeout -= 1
    #         time.sleep(0.1)
    #     if timeout <= 0:
    #         assert timeout > 0, 'timed out waiting for D-BUS object %s: %s' % (path, last_exc)

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
            # Definition: GLib.MainLoop.get_context

            # The GLib.MainContext with which the source is associated,
            # or None if the context has not yet been added to a source.
            # Return type: GLib.MainContext or None

            # Gets the GLib.MainContext with which the source is associated.
            # You can call this on a source that has been destroyed,
            # provided that the GLib.MainContext it was attached to still
            # exists (in which case it will return that GLib.MainContext).
            # In particular, you can always call this function on the
            # source returned from GLib.main_current_source().
            # But calling this function on a source whose
            # GLib.MainContext has been destroyed is an error.
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

    # def get_proxy_object(self):
    #     """
    #     Return the current DBUS session bus.
    #
    #     ``Return:`` DBusRunner bus object
    #     """
    #
    #     # if not DBusRunner.__proxy:
    #     #     DBusRunner.__proxy = DBusRunner.__bus.get("org.scarlett", object_path='/org/scarlett/Listener')
    #
    #     return DBusRunner.__proxy

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
