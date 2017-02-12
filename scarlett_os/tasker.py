#!/usr/bin/env python  # NOQA
# -*- coding: utf-8 -*-

# source: http://stackoverflow.com/questions/16981921/relative-imports-in-python-3

"""Scarlett Tasker Module."""

# from __future__ import with_statement, division, absolute_import

import os
import sys
import time
import pprint
import signal
import threading
import logging
import random

from gettext import gettext as _

from scarlett_os.internal.gi import gi
from scarlett_os.internal.gi import GObject
from scarlett_os.internal.gi import GLib


from scarlett_os.exceptions import NoStreamError
from scarlett_os.exceptions import FileReadError

import queue
from urllib.parse import quote

from scarlett_os.utility.gnome import abort_on_exception
from scarlett_os.utility.gnome import _IdleObject

from scarlett_os.utility import thread as s_thread
from scarlett_os import player
from scarlett_os import speaker
from scarlett_os import commands

import pydbus
from pydbus import SessionBus

from scarlett_os.utility.dbus_runner import DBusRunner


# global pretty print for debugging
pp = pprint.PrettyPrinter(indent=4)
logger = logging.getLogger(__name__)

_INSTANCE = None

SCARLETT_DEBUG = True

# Prevents player or command callbacks from running multiple times
player_run = False
command_run = False

STATIC_SOUNDS_PATH = '/home/pi/dev/bossjones-github/scarlett_os/static/sounds'

# loop = GLib.MainLoop()


class SoundType:
    """Enum of Player Types."""
    SCARLETT_CANCEL = "pi-cancel"
    SCARLETT_LISTENING = "pi-listening"
    SCARLETT_RESPONSE = "pi-response"
    SCARLETT_FAILED = "pi-response2"

    @staticmethod
    def get_path(sound_type):
        return ["{}/{}.wav".format(STATIC_SOUNDS_PATH, sound_type)]


class SpeakerType:
    """Enum of Player Types."""

    @staticmethod
    def speaker_to_array(sentance):
        return ["{}".format(sentance)]


class TaskSignalHandler(object):
    """Helper for tracking dbus signal registrations"""

    def __init__(self):
        self._ids = {}

    def connect(self, bus, dbus_signal, func, *args):
        """Connect a function + args to dbus_signal dbus_signal on an bus.

        Each dbus_signal may only be handled by one callback in this implementation.
        """
        assert (bus, dbus_signal) not in self._ids
        self._ids[(bus, dbus_signal)] = bus.subscribe(sender=None,
                                                      iface="org.scarlett.Listener",
                                                      signal=dbus_signal,
                                                      object="/org/scarlett/Listener",
                                                      arg0=None,
                                                      flags=0,
                                                      signal_fired=func)

    def disconnect(self, bus, dbus_signal):
        """Disconnect whatever handler we have for an bus+dbus_signal pair.

        Does nothing it the handler has already been removed.
        """
        signal_id = self._ids.pop((bus, dbus_signal), None)
        if signal_id is not None:
            signal_id.disconnect()

    def clear(self):
        """Clear all registered signal handlers."""
        # NOTE: How to avoid “RuntimeError: dictionary changed size during iteration” error?
        # source: http://stackoverflow.com/questions/11941817/how-to-avoid-runtimeerror-dictionary-changed-size-during-iteration-error
        # HINT: use list()
        for bus, dbus_signal in list(self._ids):
            signal_id = self._ids.pop((bus, dbus_signal))
            signal_id.disconnect()


class ScarlettTasker(_IdleObject):

    DEVICES = []

    # source: gosa
    # Type map for signature checking
    _type_map = {
        'as': [list],
        'a{ss}': [dict],
        'i': [int],
        'n': [int],
        'x': [int],
        'q': [int],
        'y': [chr],
        'u': [int],
        't': [int],
        'b': [bool],
        's': [str],
        'o': [object],
        'd': [float]}

    __active = False
    __instance = None

    # source: https://github.com/samdroid-apps/something-for-reddit/blob/6ec982f6fb776387ab007e2603671ec932b2005c/src/identity.py
    # sign_in_status = GObject.Signal('sign-in-status', arg_types=[str, bool])
    # token_changed = GObject.Signal('token-changed', arg_types=[object])

    __gsignals__ = {
        "tasker-started": (GObject.SignalFlags.RUN_LAST, None, ()),
        "tasker-configured": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    # tasker_started = GObject.Signal('tasker-started', arg_types=[str])
    # self.token_changed.emit(self._tokens[id])
    # self.sign_in_status.emit('', True)
    #
    # if callback is not None:
    #     callback()

    __bus = None
    __scarlett_dbus = None
    __dr = None

    @abort_on_exception
    def __init__(self, *args):
        _IdleObject.__init__(self)
        # Returns the global default main context.
        # This is the main context used for main loop functions
        # when a main loop is not explicitly specified,
        # and corresponds to the "main" main loop.
        # See also GLib.MainContext.get_thread_default().
        context = GObject.MainContext.default()

        self.bucket = bucket = queue.Queue()  # NOQA
        self.hello = None
        self.running = False
        self.bus = None
        self.scarlett_dbus = None
        self.available = False
        self._handler = TaskSignalHandler()

        # Get a dbus proxy and check if theres a service registered called 'org.scarlett.Listener'
        # if not, then we can skip all further processing. (The scarlett-os-mpris-dbus seems not to be running)
        self.__dr = DBusRunner.get_instance()

        logger.info("Initializing ScarlettTasker")

        self._failed_signal_callback = None
        self._ready_signal_callback = None
        self._keyword_recognized_signal_callback = None
        self._command_recognized_signal_callback = None
        self._cancel_signal_callback = None
        self._connect_signal_callback = None

        # # dbus related variables
        # self._id_dbus_watch_name = None
        # self._ran_configure_dbus_proxy = False

        # call back to quit mainloop
        self._connect_quit = None

        # Help on method watch_name in module pydbus.bus_names:

        # watch_name(name, flags=0, name_appeared=None, name_vanished=None) method of pydbus.bus.Bus instance
        #     Asynchronously watches a bus name.
        #
        #     Starts watching name on the bus specified by bus_type and calls
        #     name_appeared and name_vanished when the name is known to have a owner
        #     respectively known to lose its owner.
        #
        #     To receive name_appeared and name_vanished callbacks, you need an event loop.
        #     https://github.com/LEW21/pydbus/blob/master/doc/tutorial.rst#setting-up-an-event-loop
        #
        #     Parameters
        #     ----------
        #     name : string
        #             Bus name to watch
        #     flags : NameWatcherFlags, optional
        #     name_appeared : callable, optional
        #             Invoked when name is known to exist
        #             Called as name_appeared(name_owner).
        #     name_vanished : callable, optional
        #             Invoked when name is known to not exist
        #
        #     Returns
        #     -------
        #     NameWatcher
        #             An object you can use as a context manager to unwatch the name later.
        #
        #     See Also
        #     --------
        #     See https://developer.gnome.org/gio/2.44/gio-Watching-Bus-Names.html#g-bus-watch-name
        #     for more information.
        # (END)

        # __bus = None
        # __active = False
        # __instance = None
        # __proxy = None
        # __timeout = 30
        # __retry = 5
        # __bus_name = "org.scarlett"
        # __object_path = '/org/scarlett/Listener'
        # __default_interface = "org.scarlett.Listener"

        # FIXME: Figure out if we want to use this or not
        # self.configure_dbus_proxy()

        # #  TODO: If we want to keep track of signals,
        # #  we'll probably need to yield values we
        # #  append to notification list/obj
        # #  difference between yield and return
        # # Yes, it' still a generator. The return is (almost) equivalent to raising StopIteration
        # # source: http://stackoverflow.com/questions/26595895/return-and-yield-in-the-same-function

    # def configure_dbus_proxy(self):
    #     self.bus = self.__dr.get_session_bus()
    #     # NOTE: This doesn't work if we don't have a mainloop running
    #     # NOTE: To receive name_appeared and name_vanished callbacks, you need an event loop.
    #     self._id_dbus_watch_name = self.bus.watch_name("org.scarlett",
    #                                                    name_appeared=self._on_name_appeared, name_vanished=self._on_name_vanished)
    #
    #     self._ran_configure_dbus_proxy = True
    #
    #     logger.info("[configure_dbus_proxy] waiting on dbus proxy object")

    # source: https://github.com/GNOME/tracker/blob/811ad968ed549b126e75c70eaa00cbb37dfa55cc/tests/functional-tests/common/utils/helpers.py
    # def _bus_name_appeared(self, name, owner, data):
    #     log ("[%s] appeared in the bus as %s" % (self.PROCESS_NAME, owner))
    #     self.available = True
    #     self.loop.quit()
    #
    # def _bus_name_vanished(self, name, data):
    #     log ("[%s] disappeared from the bus" % self.PROCESS_NAME)
    #     self.available = False
    #     self.loop.quit()
    #
    # def _on_name_appeared(self):
    #     if "org.scarlett" in self.bus.list_names():
    #         if self.scarlett_dbus:
    #             del self.scarlett_dbus
    #
    #         # Trigger resend of capapability event
    #         self.available = True
    #         self.scarlett_dbus = self.bus.get("org.scarlett", '/org/scarlett/Listener')
    #         # ccr = PluginRegistry.getInstance('ClientCommandRegistry')
    #         # ccr.register("request_inventory", 'Inventory.request_inventory', [], ['old_checksum=None'], 'Request client inventory information')
    #         # mqtt = PluginRegistry.getInstance('MQTTClientService')
    #         # mqtt.reAnnounce()
    #         logger.info("[on_name_appeared][{}]: Established dbus connection".format(self.__class__))
    #     else:
    #         logger.info("[on_name_appeared][{}]: no dbus connection".format(self.__class__))
    #
    # def _on_name_vanished(self):
    #     if "org.scarlett" not in self.bus.list_names():
    #         if self.scarlett_dbus:
    #             # NOTE: This might come up soon
    #             # source: http://blender.stackexchange.com/questions/18802/how-to-delete-property-from-object
    #             del(self.scarlett_dbus)
    #             self.available = False
    #
    #             # Trigger resend of capapability event
    #             # ccr = PluginRegistry.getInstance('ClientCommandRegistry')
    #             # ccr.unregister("request_inventory")
    #             # mqtt = PluginRegistry.getInstance('MQTTClientService')
    #             # mqtt.reAnnounce()
    #             logger.info("[on_name_vanished][{}]: lost dbus connection".format(self.__class__))
    #     else:
    #         logger.info("[on_name_appeared][{}]: no dbus connection".format(self.__class__))

    # NOTE
    # source: http://www.pygtk.org/pygtk2tutorial/examples/helloworld.py
    # If the callback function is an object method then it will have the general form:
    # def on_connected_to_listener(self):
    #     pass
    # where self is the object instance invoking the method. This is the form used in the helloworld.py example program.

    # @property
    # def bus(self):
    #     """Get the Bus Object"""
    #     if self.__bus is None:
    #         return None
    #     return self.__bus
    #
    # @bus.setter
    # def bus(self, bus_obj):
    #     """Set the Bus Object
    #     """
    #     if bus_obj is None:
    #         self.__bus = None
    #         return
    #     else:
    #         if type(bus_obj) == pydbus.bus.Bus:
    #             self.__bus = bus_obj
    #         else:
    #             raise ValueError("bus_obj '{0} must be of type pydbus.bus.Bus'")
    #
    # @property
    # def scarlett_dbus(self):
    #     """Get the scarlett dbus proxy object"""
    #     if self.__scarlett_dbus is None:
    #         return None
    #     return self.__scarlett_dbus
    #
    # @scarlett_dbus.setter
    # def scarlett_dbus(self, s_dbus):
    #     """Set the scarlett dbus proxy Object
    #     """
    #     if s_dbus is None:
    #         self.__scarlett_dbus = None
    #         return
    #     else:
    #         # Check that proxy object has a Introspect method
    #         proxy_obj = getattr(s_dbus, "Introspect")
    #         if callable(proxy_obj.Introspect):
    #             self.__scarlett_dbus = s_dbus
    #         else:
    #             raise ValueError("proxy_obj.Introspect '{0} is not callable. Something wrong with proxy object!'")

    def do_tasker_started(self):
        logger.info("Starting up ScarlettTasker ...")

    def do_tasker_configured(self):
        logger.info("ScarlettTasker is configured...")

    def reset(self):
        """Reset the helper.

        Should be called whenever the source changes and we are not setting up
        a new appsrc.
        """
        self._handler.clear()
        self._failed_signal_callback = None
        self._ready_signal_callback = None
        self._keyword_recognized_signal_callback = None
        self._command_recognized_signal_callback = None
        self._cancel_signal_callback = None
        self._connect_signal_callback = None

    def prepare(self, player_cb, command_cb, connected_to_listener_cb):
        """Store info we will need when the appsrc element gets installed."""
        self._handler.clear()
        self._failed_signal_callback = player_cb
        self._ready_signal_callback = player_cb
        self._keyword_recognized_signal_callback = player_cb
        self._command_recognized_signal_callback = command_cb
        self._cancel_signal_callback = player_cb
        self._connect_signal_callback = connected_to_listener_cb

    def teardown_handling(self):
        # disconnect all signals
        self._handler.clear()
        self._failed_signal_callback = None
        self._ready_signal_callback = None
        self._keyword_recognized_signal_callback = None
        self._command_recognized_signal_callback = None
        self._cancel_signal_callback = None
        self._connect_signal_callback = None

        if hasattr(self, "_id_dbus_watch_name"):
            self._id_dbus_watch_name.unwatch()
            self._id_dbus_watch_name = None

    def configure(self):
        """Configure the supplied bus for use.
        """
        # NOTE: OLD VALUE
        # bus = self.__dr.get_session_bus()
        # bus = self.bus = self.__dr.get_session_bus()
        # bus = self.bus
        bus = self.__dr.get_session_bus()

        # def connect(self, bus, dbus_signal, func, *args):

        if self._failed_signal_callback:
            self._handler.connect(bus, "SttFailedSignal", self._failed_signal_callback)

        if self._ready_signal_callback:
            self._handler.connect(bus, "ListenerReadySignal", self._ready_signal_callback)

        if self._keyword_recognized_signal_callback:
            self._handler.connect(bus, "KeywordRecognizedSignal", self._keyword_recognized_signal_callback)

        if self._command_recognized_signal_callback:
            self._handler.connect(bus, "CommandRecognizedSignal", self._command_recognized_signal_callback)

        if self._cancel_signal_callback:
            self._handler.connect(bus, "ListenerCancelSignal", self._cancel_signal_callback)

        if self._connect_signal_callback:
            self._handler.connect(bus, "ConnectedToListener", self._connect_signal_callback)

        # This function always returns False so that it may be safely
        # invoked via GLib.idle_add(). Use of idle_add() is necessary
        # to ensure that watchers are always called from the main thread,
        # even if progress updates are received from other threads.
        self.emit('tasker-configured')


def print_keyword_args(**kwargs):
    # kwargs is a dict of the keyword args passed to the function
    for key, value in kwargs.items():
        print(("%s = %s" % (key, value)))


def print_args(args):  # pragma: no cover
    for i, v in enumerate(args):
        print("another arg through *arg : {}".format(v))


def connected_to_listener_cb(*args, **kwargs):
    logging.debug('HERE IN connected_to_listener_cb')

    print_args(args)
    print_keyword_args(**kwargs)

    for i, v in enumerate(args):
        if isinstance(v, tuple):
            # FIXME: This is def a race condition waiting to happen
            # FIXME: Convert devices into a real class that has a context manager to deal with things
            ScarlettTasker.DEVICES.append(v)
            logging.debug("[DEVICES] append: {}".format(v))


@abort_on_exception
def player_cb(*args, **kwargs):
    if os.environ.get('SCARLETT_DEBUG_MODE'):
        logger.debug("player_cb PrettyPrinter: ")
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(args)
        # MAR 13 2016
        logger.debug("player_cb kwargs")
        print_keyword_args(**kwargs)
        # (con=<DBusConnection object at 0x7f3fba21f0f0 (GDBusConnection at 0x2ede000)>,
        # sender=':1.0',
        # object='/org/scarlett/Listener',
        # iface='org.scarlett.Listener',
        # signal='CommandRecognizedSignal',
        # params=GLib.Variant('(sss)', ('  ScarlettListener caugh...ommand match', 'pi-response', 'what time is it')))

    # NOTE: THIS IS WHAT FIXED THE GENERATOR NONSENSE
    # source: https://www.python.org/dev/peps/pep-0343/
    def player_generator_func():
        for path in wavefile:
            path = os.path.abspath(os.path.expanduser(path))
            yield True
            print("for path in wavefile")
            p = player.ScarlettPlayer(path, False, False)
            while True:
                try:
                    yield next(p)
                finally:
                    time.sleep(p.duration)
                    p.close(force=True)
                    yield False

    def run_player(function):
        gen = function()
        GObject.idle_add(lambda: next(gen, False), priority=GLib.PRIORITY_HIGH)

    for i, v in enumerate(args):
        if os.environ.get('SCARLETT_DEBUG_MODE'):
            logger.debug("Type v: {}".format(type(v)))
            logger.debug("Type i: {}".format(type(i)))
        if isinstance(v, tuple):
            if os.environ.get('SCARLETT_DEBUG_MODE'):
                logger.debug("THIS SHOULD BE A Tuple now: {}".format(v))

            # Unbundle tuples and make sure you know how many items are returned
            tuple_args = len(v)
            if tuple_args == 1:
                msg = v
            elif tuple_args == 2:
                msg, scarlett_sound = v
            elif tuple_args == 3:
                msg, scarlett_sound, command = v

            logger.warning(" msg: {}".format(msg))
            logger.warning(" scarlett_sound: {}".format(scarlett_sound))

            wavefile = SoundType.get_path(scarlett_sound)
            run_player_result = run_player(player_generator_func)

            logger.info('END PLAYING WITH SCARLETTPLAYER OUTSIDE IF')
        else:
            logger.debug("THIS IS NOT A GLib.Variant: {} - TYPE {}".format(v, type(v)))


# NOTE: enumerate req to iterate through tuple and find GVariant
# @trace
@abort_on_exception
def command_cb(*args, **kwargs):
    if os.environ.get('SCARLETT_DEBUG_MODE'):
        logger.debug("command_cb PrettyPrinter: ")
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(args)
        # MAR 13 2016
        logger.debug("command_cb kwargs")
        print_keyword_args(**kwargs)
        # (con=<DBusConnection object at 0x7f3fba21f0f0 (GDBusConnection at 0x2ede000)>,
        # sender=':1.0',
        # object='/org/scarlett/Listener',
        # iface='org.scarlett.Listener',
        # signal='CommandRecognizedSignal',
        # params=GLib.Variant('(sss)', ('  ScarlettListener caugh...ommand match', 'pi-response', 'what time is it')))

        # NOTE: THIS IS WHAT FIXED THE GENERATOR NONSENSE
        # source: https://www.python.org/dev/peps/pep-0343/
    def player_generator_func():
        for path in wavefile:
            path = os.path.abspath(os.path.expanduser(path))
            yield True
            print("for path in wavefile")
            p = player.ScarlettPlayer(path, False, False)
            while True:
                try:
                    yield next(p)
                finally:
                    time.sleep(p.duration)
                    p.close(force=True)
                    yield False

    def run_player(function):
        gen = function()
        GObject.idle_add(lambda: next(gen, False), priority=GLib.PRIORITY_HIGH)

    def speaker_generator_func():
        for scarlett_text in tts_list:
            yield True
            print("scarlett_text in tts_list")
            _wavepath = "/home/pi/dev/bossjones-github/scarlett_os/espeak_tmp.wav"
            s = speaker.ScarlettSpeaker(text_to_speak=scarlett_text,
                                        wavpath=_wavepath,
                                        skip_player=True)
            p = player.ScarlettPlayer(_wavepath, False, False)
            logger.error("Duration: p.duration: {}".format(p.duration))
            while True:
                try:
                    yield next(p)
                finally:
                    time.sleep(p.duration)
                    p.close(force=True)
                    s.close(force=True)
                    yield False

    def run_speaker(function):
        gen = function()
        GObject.idle_add(lambda: next(gen, False), priority=GLib.PRIORITY_HIGH)

    for i, v in enumerate(args):
        if os.environ.get('SCARLETT_DEBUG_MODE'):
            logger.debug("Type v: {}".format(type(v)))
            logger.debug("Type i: {}".format(type(i)))
        if isinstance(v, tuple):
            if os.environ.get('SCARLETT_DEBUG_MODE'):
                logger.debug("THIS SHOULD BE A Tuple now: {}".format(v))

            # Unbundle tuples and make sure you know how many items are returned
            tuple_args = len(v)
            if tuple_args == 1:
                msg = v
            elif tuple_args == 2:
                msg, scarlett_sound = v
            elif tuple_args == 3:
                msg, scarlett_sound, command = v

            logger.warning(" msg: {}".format(msg))
            logger.warning(" scarlett_sound: {}".format(scarlett_sound))
            logger.warning(" command: {}".format(command))

            # 1. play sound first
            wavefile = SoundType.get_path(scarlett_sound)
            run_player_result = run_player(player_generator_func)

            # 2. Perform command
            command_run_results = commands.Command.check_cmd(command_tuple=v)

            # 3. Verify it is not a command NO_OP
            if command_run_results == '__SCARLETT_NO_OP__':
                logger.error("__SCARLETT_NO_OP__")
                return False

            # 4. Scarlett Speaks
            tts_list = SpeakerType.speaker_to_array(command_run_results)
            run_speaker_result = run_speaker(speaker_generator_func)

            # 5. Emit signal to reset keyword match ( need to implement this )
            bus = SessionBus()
            ss = bus.get("org.scarlett", object_path='/org/scarlett/Listener')  # NOQA
            time.sleep(1)
            ss.emitListenerCancelSignal()
            # 6. Finished call back
        else:
            logger.debug("THIS IS NOT A GLib.Variant: {} - TYPE {}".format(v, type(v)))


if __name__ == "__main__":
    if os.environ.get('SCARLETT_DEBUG_MODE'):
        import faulthandler
        faulthandler.register(signal.SIGUSR2, all_threads=True)

        from scarlett_os.internal.debugger import init_debugger
        init_debugger()

        from scarlett_os.internal.debugger import enable_remote_debugging
        enable_remote_debugging()

    #######################################################################
    loop = GLib.MainLoop()
    _INSTANCE = st = ScarlettTasker()
    st.prepare(player_cb, command_cb, connected_to_listener_cb)
    st.configure()
    #######################################################################

    if os.environ.get('TRAVIS_CI'):
        # Close application silently
        try:
            loop.run()
        except KeyboardInterrupt:
            logger.warning('***********************************************')
            logger.warning('Note: Added an exception "pass" for KeyboardInterrupt')
            logger.warning('It is very possible that this might mask other errors happening with the application.')
            logger.warning('Remove this while testing manually')
            logger.warning('***********************************************')
            st.teardown_handling()
            pass
        except:
            raise
    else:
        # Close into a ipython debug shell
        loop.run()
