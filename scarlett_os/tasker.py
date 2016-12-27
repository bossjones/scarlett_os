#!/usr/bin/env python  # NOQA
# -*- coding: utf-8 -*-

# source: http://stackoverflow.com/questions/16981921/relative-imports-in-python-3

"""Scarlett Tasker Module."""

# from __future__ import with_statement, division, absolute_import

import os
import sys
import time

from scarlett_os.internal.debugger import init_debugger

init_debugger()

import pprint
import signal
import threading
import logging
import pprint
import time
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
from scarlett_os import subprocess
from scarlett_os import player
from scarlett_os import speaker
from scarlett_os import commands

from pydbus import SessionBus


# global pretty print for debugging
pp = pprint.PrettyPrinter(indent=4)
logger = logging.getLogger(__name__)

_INSTANCE = None

SCARLETT_DEBUG = True

# Prevents player or command callbacks from running multiple times
player_run = False
command_run = False

STATIC_SOUNDS_PATH = '/home/pi/dev/bossjones-github/scarlett_os/static/sounds'

if SCARLETT_DEBUG:
    # Setting GST_DEBUG_DUMP_DOT_DIR environment variable enables us to have a
    # dotfile generated
    os.environ[
        "GST_DEBUG_DUMP_DOT_DIR"] = "/home/pi/dev/bossjones-github/scarlett_os/_debug"
    os.putenv('GST_DEBUG_DUMP_DIR_DIR',
              '/home/pi/dev/bossjones-github/scarlett_os/_debug')

loop = GLib.MainLoop()

try:
    from rfoo.utils import rconsole
    rconsole.spawn_server()
except ImportError:
    logger.debug("No socket opened for debugging -> please install rfoo")


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


class ScarlettTasker(_IdleObject):

    @abort_on_exception
    def __init__(self, *args):
        _IdleObject.__init__(self)
        context = GObject.MainContext.default()

        self.bucket = bucket = queue.Queue()  # NOQA
        self.hello = None

        # with SessionBus() as bus:
        bus = SessionBus()
        ss = bus.get("org.scarlett", object_path='/org/scarlett/Listener')  # NOQA
        time.sleep(1)

        ss_failed_signal = bus.subscribe(sender=None,
                                         iface="org.scarlett.Listener",
                                         signal="SttFailedSignal",
                                         object="/org/scarlett/Listener",
                                         arg0=None,
                                         flags=0,
                                         signal_fired=player_cb)

        ss_rdy_signal = bus.subscribe(sender=None,
                                      iface="org.scarlett.Listener",
                                      signal="ListenerReadySignal",
                                      object="/org/scarlett/Listener",
                                      arg0=None,
                                      flags=0,
                                      signal_fired=player_cb)

        ss_kw_rec_signal = bus.subscribe(sender=None,
                                         iface="org.scarlett.Listener",
                                         signal="KeywordRecognizedSignal",
                                         object="/org/scarlett/Listener",
                                         arg0=None,
                                         flags=0,
                                         signal_fired=player_cb)

        ss_cmd_rec_signal = bus.subscribe(sender=None,
                                          iface="org.scarlett.Listener",
                                          signal="CommandRecognizedSignal",
                                          object="/org/scarlett/Listener",
                                          arg0=None,
                                          flags=0,
                                          signal_fired=command_cb)

        ss_cancel_signal = bus.subscribe(sender=None,
                                         iface="org.scarlett.Listener",
                                         signal="ListenerCancelSignal",
                                         object="/org/scarlett/Listener",
                                         arg0=None,
                                         flags=0,
                                         signal_fired=player_cb)

        pp.pprint((ss_failed_signal,
                   ss_rdy_signal,
                   ss_kw_rec_signal,
                   ss_cmd_rec_signal,
                   ss_cancel_signal))

        logger.debug("ss_failed_signal: {}".format(ss_failed_signal))
        logger.debug("ss_rdy_signal: {}".format(ss_rdy_signal))
        logger.debug("ss_kw_rec_signal: {}".format(ss_kw_rec_signal))
        logger.debug("ss_cmd_rec_signal: {}".format(ss_cmd_rec_signal))
        logger.debug("ss_cancel_signal: {}".format(ss_cancel_signal))

        ss.emitConnectedToListener('ScarlettTasker')

        loop.run()

        try:
            print("ScarlettTasker Thread Started")
        except Exception:
            ss_failed_signal.disconnect()
            ss_rdy_signal.disconnect()
            ss_kw_rec_signal.disconnect()
            ss_cmd_rec_signal.disconnect()
            ss_cancel_signal.disconnect()
            loop.quit()
            self.bucket.put(sys.exc_info())
            raise


def signal_handler_player_thread(scarlett_sound):
    '''No-Op Function to handle playing Gstreamer.'''

    def function_calling_player_gst(event, *args, **kwargs):
        player_run = True
        logger.info('BEGIN PLAYING WITH SCARLETTPLAYER')
        if player_run:
            wavefile = SoundType.get_path(scarlett_sound)
            for path in wavefile:
                path = os.path.abspath(os.path.expanduser(path))
                with player.ScarlettPlayer(path, False, False) as f:
                    print((f.channels))
                    print((f.samplerate))
                    print((f.duration))
                    for s in f:
                        yield
        event.set()
        wavefile = None
        player_run = False
        logger.info('END PLAYING WITH SCARLETTPLAYER INSIDE IF')
        event.clear()

    event = threading.Event()
    logger.info('event = threading.Event()')
    GObject.idle_add(function_calling_player_gst, event, priority=GLib.PRIORITY_HIGH)
    logger.info('BEFORE event.wait()')
    event.wait()
    logger.info('END PLAYING WITH SCARLETTPLAYER INSIDE IF')


@abort_on_exception
def signal_handler_speaker_thread():

    def function_calling_speaker(event, result, tts_list):
        for scarlett_text in tts_list:
            with s_thread.time_logger('Scarlett Speaks'):
                speaker.ScarlettSpeaker(text_to_speak=scarlett_text,
                                        wavpath="/home/pi/dev/bossjones-github/scarlett_os/espeak_tmp.wav")
        event.set()


@abort_on_exception
def fake_cb(*args, **kwargs):
    if SCARLETT_DEBUG:
        logger.debug("fake_cb")


def print_keyword_args(**kwargs):
    # kwargs is a dict of the keyword args passed to the function
    for key, value in kwargs.items():
        print(("%s = %s" % (key, value)))


@abort_on_exception
def player_cb(*args, **kwargs):
    if SCARLETT_DEBUG:
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
        if SCARLETT_DEBUG:
            logger.debug("Type v: {}".format(type(v)))
            logger.debug("Type i: {}".format(type(i)))
        if isinstance(v, tuple):
            if SCARLETT_DEBUG:
                logger.debug(
                    "THIS SHOULD BE A Tuple now: {}".format(v))
            msg, scarlett_sound = v
            logger.warning(" msg: {}".format(msg))
            logger.warning(
                " scarlett_sound: {}".format(scarlett_sound))

            wavefile = SoundType.get_path(scarlett_sound)
            run_player_result = run_player(player_generator_func)

            logger.info('END PLAYING WITH SCARLETTPLAYER OUTSIDE IF')
        else:
            logger.debug("THIS IS NOT A GLib.Variant: {} - TYPE {}".format(v, type(v)))


# NOTE: enumerate req to iterate through tuple and find GVariant
# @trace
@abort_on_exception
def command_cb(*args, **kwargs):
    if SCARLETT_DEBUG:
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
        if SCARLETT_DEBUG:
            logger.debug("Type v: {}".format(type(v)))
            logger.debug("Type i: {}".format(type(i)))
        if isinstance(v, tuple):
            if SCARLETT_DEBUG:
                logger.debug(
                    "THIS SHOULD BE A Tuple now: {}".format(v))
            msg, scarlett_sound, command = v
            logger.warning(" msg: {}".format(msg))
            logger.warning(
                " scarlett_sound: {}".format(scarlett_sound))
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
    _INSTANCE = st = ScarlettTasker()
