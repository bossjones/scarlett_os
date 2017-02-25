#!/usr/bin/env python  # NOQA
# -*- coding: utf-8 -*-

# source: http://stackoverflow.com/questions/16981921/relative-imports-in-python-3

"""Scarlett Tasker Module."""

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
from scarlett_os.internal.path import touch_empty_file
from scarlett_os.internal.path import fname_exists

from scarlett_os.utility.generators import GIdleThread

#######################################
# FIXME: Temporary, till we figure out best way to approach logging module
# FIXME: FAM, THIS SHIT IS NOT THREADSAFE AT ALL. LETS SEE HOW MOPIDY/PITIVI/SOMEBODY-ELSE IS HANDLING THINGS
# import scarlett_os.logger
# import logging
# import logging.config
# import logging.handlers

# from scarlett_os.const import __version__
# from scarlett_os import log

logger = logging.getLogger(__name__)


# global pretty print for debugging
pp = pprint.PrettyPrinter(indent=4)
# logger = logging.getLogger(__name__)

_INSTANCE = None

SCARLETT_DEBUG = True

# Prevents player or command callbacks from running multiple times
player_run = False
command_run = False


STATIC_SOUNDS_PATH = '/home/pi/dev/bossjones-github/scarlett_os/static/sounds'

pause_in_seconds = 1


class SoundType:
    """Enum of Player Types."""
    SCARLETT_CANCEL = "pi-cancel"
    SCARLETT_LISTENING = "pi-listening"
    SCARLETT_RESPONSE = "pi-response"
    SCARLETT_FAILED = "pi-response2"

    @staticmethod
    def get_path(sound_type):
        return ["{}/{}.wav".format(STATIC_SOUNDS_PATH, sound_type)]

    @staticmethod
    def get_speaker_path():
        return ["/home/pi/dev/bossjones-github/scarlett_os/espeak_tmp.wav"]


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

    ###############################################################################################
    # source: exaile
    # HACK: Notice that this is not __gsignals__; descendants need to manually
    # merge this in. This is because new PyGObject doesn't like __gsignals__
    # coming from mixin. See:
    # * https://bugs.launchpad.net/bugs/714484
    # * http://www.daa.com.au/pipermail/pygtk/2011-February/019394.html
    # _gsignals_ = {
    #     'playlist-selected': (GObject.SignalFlags.RUN_LAST, None, (object,)),
    #     'tracks-selected': (GObject.SignalFlags.RUN_LAST, None, (object,)),
    #     'append-items': (GObject.SignalFlags.RUN_LAST, None, (object, bool)),
    #     'replace-items': (GObject.SignalFlags.RUN_LAST, None, (object,)),
    #     'queue-items': (GObject.SignalFlags.RUN_LAST, None, (object,)),
    # }
    #
    # .... later on ....
    # class PlaylistsPanel(panel.Panel, BasePlaylistPanelMixin):
    # """
    #     The playlists panel
    # """
    # __gsignals__ = BasePlaylistPanelMixin._gsignals_
    ###############################################################################################

    ###############################################################################################
    # SOURCE: scarlett
    # __gsignals__ = {
    #     "completed": (
    #         GObject.SignalFlags.RUN_LAST, None, []),
    #     "progress": (
    #         GObject.SignalFlags.RUN_LAST, None, [
    #             GObject.TYPE_FLOAT])  # percent complete
    # }
    ###############################################################################################

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
        self._id_do_play_sound = None

    # FIXME: Okay, when this file doesn't exist, espeak can hang. For now create in advance to get around it
    def _prep_tmp_espeak(self, wavepath="/home/pi/dev/bossjones-github/scarlett_os/espeak_tmp.wav"):
        if not fname_exists(wavepath):
            print('[prep_tmp_espeak]: MISSING TEMP ESPEAK FILE')
            touch_empty_file(wavepath)

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
        self._prep_tmp_espeak()

    def configure(self):
        """Configure the supplied bus for use.
        """
        bus = self.__dr.get_session_bus()

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
        # self.emit('tasker-configured')


def print_keyword_args(**kwargs):
    # kwargs is a dict of the keyword args passed to the function
    for key, value in kwargs.items():
        print(("%s = %s" % (key, value)))


def print_args(args):  # pragma: no cover
    for i, v in enumerate(args):
        print("another arg through *arg : {}".format(v))


def call_player(sound):
    """Global function to allow calls to Scarlett Player via generator function. Should help reduce duplicate code."""
    # NOTE: THIS IS WHAT FIXED THE GENERATOR NONSENSE
    # source: https://www.python.org/dev/peps/pep-0343/
    # The generator gets instantiated and the next() function, which resumes the execution of the generator, is scheduled using GLib.idle_add(). GLib.idle_add() will re-schedule the call to next() until it returns False which will happen if the generator is exhausted, meaning the function is finished and has returned. Every time the generator yields, GTK+ has time to process events and update the user interface.
    def player_generator_func():
        for path in wavefile:
            path = os.path.abspath(os.path.expanduser(path))
            # FIXME: fix this comment, slightly true, but stolen from another example
            # Yield True if any of the incoming values from generator.send() match the given test_value.
            # Always yield True after the first match is found
            # Meaning, yield True when we create scarlettPlayer
            yield True
            print("for path in wavefile")
            logger.info("Running in call_player")
            p = player.ScarlettPlayer(path, False, False)
            while True:
                try:
                    yield next(p)
                finally:
                    time.sleep(p.duration)
                    p.close(force=True)
                    yield False

    def run_player(function):
        # Create generator function
        gen = function()

        # next() - Return the next item from the iterator.
        # If default is given and the iterator
        # is exhausted, it is returned instead of raising StopIteration.
        # NOTE: OLD WAYS OF DOING THIS.
        # NOTE: PROBLEM WITH THIS IS THAT ALL OF THESE GUYS WOULD RUN TOGETHER AT THE SAME TIME
        # GObject.idle_add(lambda: next(gen, False), priority=GLib.PRIORITY_HIGH)
        # _t = GIdleThread(lambda: next(gen, False))

        # source: https://gist.github.com/bossjones/916fd12b72627b6b5403
        # Pass generator function to pseudo-"thread" GIdleThread
        _t = GIdleThread(gen)
        # Run pseudo-"thread" with a given priority
        _t.start(priority=GLib.PRIORITY_HIGH)
        # Wait till pseudo-"thread" is finished running before continuing forward
        _t.wait()

    # Convert this into full path
    wavefile = SoundType.get_path(sound)

    run_player(player_generator_func)


def call_espeak_subprocess(command_run_results):
    logger.info("Running in call_espeak_subprocess")

    # NOTE: Throw results from command into an array for iteratining over
    tts_list = SpeakerType.speaker_to_array(command_run_results)

    # iterate through each comannd string
    for scarlett_text in tts_list:
        # Get command as string ( ie. first value )
        _wavepath = SoundType.get_speaker_path()[0]

        # Simply write TTS -> Disk
        s = speaker.ScarlettSpeaker(text_to_speak=scarlett_text,
                                    wavpath=_wavepath,
                                    skip_player=True)

        # Close file descriptor for subprocess when finished
        s.close(force=True)


def call_speaker(command_run_results):
    logger.info("Running in call_speaker")

    def speaker_generator_func():
        for scarlett_text in tts_list:
            # Yield True if any of the incoming values from generator.send() match the given test_value.
            # Always yield True after the first match is found
            # source: https://wiki.gnome.org/Projects/PyGObject/Threading
            # PyGObject: uses yield True to pass control to the main loop in regular intervals.
            yield True
            print("scarlett_text in tts_list")
            print("[scarlett_text]: {}".format(scarlett_text))
            print("type[scarlett_text]: {}".format(type(scarlett_text)))
            _wavepath = SoundType.get_speaker_path()[0]
            p = player.ScarlettPlayer(_wavepath, False, False)
            logger.error("Duration: p.duration: {}".format(p.duration))
            while True:
                try:
                    yield next(p)
                finally:
                    time.sleep(p.duration)
                    p.close(force=True)
                    # source: https://wiki.gnome.org/Projects/PyGObject/Threading
                    # PyGObject: uses yield True to pass control to the main loop in regular intervals.
                    yield False

    def run_speaker(function):
        # Create generator function
        gen = function()

        # next() - Return the next item from the iterator.
        # If default is given and the iterator
        # is exhausted, it is returned instead of raising StopIteration.
        # NOTE: OLD WAYS OF DOING THIS.
        # NOTE: PROBLEM WITH THIS IS THAT ALL OF THESE GUYS WOULD RUN TOGETHER AT THE SAME TIME
        # GObject.idle_add(lambda: next(gen, False), priority=GLib.PRIORITY_HIGH)
        # GObject.idle_add(lambda: next(gen, False), priority=GLib.PRIORITY_DEFAULT_IDLE)
        # GObject.idle_add(lambda: next(gen, False), priority=GLib.PRIORITY_HIGH)
        # _t = GIdleThread(lambda: next(gen, False))

        # source: https://gist.github.com/bossjones/916fd12b72627b6b5403
        # Pass generator function to pseudo-"thread" GIdleThread
        _s = GIdleThread(gen)
        # Run pseudo-"thread" with a given priority
        _s.start(priority=GLib.PRIORITY_HIGH)
        # Wait till pseudo-"thread" is finished running before continuing forward
        _s.wait()

    tts_list = SpeakerType.speaker_to_array(command_run_results)
    run_speaker(speaker_generator_func)


def on_signal_recieved(*args, **kwargs):
    if os.environ.get('SCARLETT_DEBUG_MODE'):
        logger.debug("player_cb args")
        print_args(args)
        logger.debug("player_cb kwargs")
        print_keyword_args(**kwargs)

    # source: https://gist.github.com/bossjones/916fd12b72627b6b5403
    # Get mainthread context before running anything that requires a MainLoop
    main = GObject.main_context_default()

    if args[3] == 'ListenerReadySignal':
        msg, scarlett_sound = args[4]
        call_player(scarlett_sound)
    elif args[3] == 'SttFailedSignal':
        msg, scarlett_sound = args[4]
        call_player(scarlett_sound)
    elif args[3] == 'KeywordRecognizedSignal':
        msg, scarlett_sound = args[4]
        call_player(scarlett_sound)
    elif args[3] == 'CommandRecognizedSignal':
        msg, scarlett_sound, command = args[4]
        logger.debug("[CommandRecognizedSignal] WE WOULD RUN SOMETHING HERE")

        # 1. acknowledge that we are moving forward with running command
        # FIXME: Turn this into a dbus signal to emit?
        call_player('pi-response')

        # 2. Perform command
        print('args[4]')
        print(args[4])
        command_run_results = commands.Command.check_cmd(command_tuple=args[4])
        logger.debug("[command_run_results]: {}".format(command_run_results))

        # 3. Verify it is not a command NO_OP
        if command_run_results == '__SCARLETT_NO_OP__':
            logger.error("__SCARLETT_NO_OP__")
            return False

        # 4. Espeak gst plugin doesn't work, write sound to wav file
        call_espeak_subprocess(command_run_results)

        # # 4. Scarlett Speaks
        # tts_list = SpeakerType.speaker_to_array(command_run_results)
        # run_speaker_result = run_speaker(speaker_generator_func)

        # 5. Play speaker
        call_speaker(command_run_results)

        # FIXME: Turn this into a call back function. Pass it to run_speaker
        # 5. Emit signal to reset keyword match ( need to implement this )
        dr = DBusRunner.get_instance()
        bus = dr.get_session_bus()
        ss = bus.get("org.scarlett", object_path='/org/scarlett/Listener')  # NOQA
        ss.emitListenerCancelSignal()

    elif args[3] == 'ListenerCancelSignal':
        msg, scarlett_sound = args[4]
        call_player(scarlett_sound)
    elif args[3] == 'ConnectedToListener':
        msg = args[4]
        ScarlettTasker.DEVICES.append(msg)
        logger.debug("[DEVICES] append: {}".format(msg))


if __name__ == "__main__":
    if os.environ.get('SCARLETT_DEBUG_MODE'):
        import faulthandler
        faulthandler.register(signal.SIGUSR2, all_threads=True)

        from scarlett_os.internal.debugger import init_debugger
        init_debugger()

        from scarlett_os.internal.debugger import enable_remote_debugging
        enable_remote_debugging()

    from scarlett_os.logger import setup_logger
    setup_logger()

    #######################################################################
    # New logging setup - START
    #######################################################################
    # log.bootstrap_delayed_logging()
    #
    # logger.info('Starting ScarlettOS Tasker %s', str(__version__))
    #
    # # SET VERBOSITY TO DEBUG BY DEFAULT
    # verbosity_level = 3
    #
    # log.setup_logging(verbosity_level, False)
    #######################################################################
    # New logging setup - END
    #######################################################################

    #######################################################################
    # Pitivi logging setup
    #######################################################################
    # Init logging as early as possible so we can log startup code
    # enable_color = not os.environ.get(
    #     'PITIVI_DEBUG_NO_COLOR', '0') in ('', '1')
    # # Let's show a human-readable Pitivi debug output by default, and only
    # # show a crazy unreadable mess when surrounded by gst debug statements.
    # enable_crack_output = "GST_DEBUG" in os.environ
    # loggable.init('PITIVI_DEBUG', enable_color, enable_crack_output)
    #
    # self.info('starting up')
    #######################################################################
    # Pitivi logging setup - END
    #######################################################################

    #######################################################################
    loop = GLib.MainLoop()
    _INSTANCE = st = ScarlettTasker()
    # NOTE: OLD WAY OF DOING THINGS
    # st.prepare(player_cb, command_cb, connected_to_listener_cb)
    st.prepare(on_signal_recieved, on_signal_recieved, on_signal_recieved)
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
            st.reset()
            pass
        except:
            raise
    else:
        # Close into a ipython debug shell
        loop.run()
