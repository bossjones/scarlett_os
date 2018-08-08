#!/usr/bin/env python  # NOQA
# -*- coding: utf-8 -*-

# NOTE: WE NEEDED TO REMOVE THE HASHBAG AT THE BEGINNING TO GET python3 -m scarlett_os.speaker to work!!!
# source: http://stackoverflow.com/questions/16981921/relative-imports-in-python-3

"""Scarlett Listener Module."""

# NOTE: THIS IS THE CLASS THAT WILL BE REPLACING scarlett_speaker.py eventually.
# It is cleaner, more object oriented, and will allows us to run proper tests.
# Also threading.RLock() and threading.Semaphore() works correctly.

# There are a LOT of threads going on here, all of them managed by Gstreamer.
# If pyglet ever needs to run under a Python that doesn't have a GIL, some
# locks will need to be introduced to prevent concurrency catastrophes.
#
# At the moment, no locks are used because we assume only one thread is
# executing Python code at a time.  Some semaphores are used to block and wake
# up the main thread when needed, these are all instances of
# threading.Semaphore.  Note that these don't represent any kind of
# thread-safety.

import sys
import os

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
from scarlett_os.internal.gi import Gst
from scarlett_os.internal.gi import Gio

from scarlett_os.exceptions import NoStreamError
from scarlett_os.exceptions import FileReadError

import queue
from urllib.parse import quote

from scarlett_os.utility.gnome import abort_on_exception
from scarlett_os.utility.gnome import _IdleObject

from scarlett_os.utility import thread as s_thread
from scarlett_os import subprocess
from scarlett_os import player
from scarlett_os.sounds import STATIC_SOUNDS_PATH

from scarlett_os.common.configure.ruamel_config import ConfigManager


# global pretty print for debugging
pp = pprint.PrettyPrinter(indent=4)
logger = logging.getLogger(__name__)


class ScarlettSpeaker(object):
    """Scarlett Speaker Class."""

    def __init__(self, text_to_speak="", wavpath="", skip_player=False):
        """ScarlettSpeaker object. Anything defined here belongs to the INSTANCE of the class."""
        self._wavefile = []
        self._pitch = 75
        self._speed = 175
        self._wavpath = wavpath
        self._wavefile.append(self._wavpath)
        self._voice = "en+f3"
        self._text = _("{}".format(text_to_speak))
        self._word_gap = 1
        self._command = self.create_cmd()

        # TODO: Add check values before attempting to run

        self.path = None

        # Write espeak data
        with s_thread.time_logger("Espeak Subprocess To File"):
            self.running = True
            self.finished = False
            # FIXME: Looks like we could have a memory/file-descriptors leak here
            # FIXME: Need to close out self.res when finished
            self.res = subprocess.Subprocess(
                self._command, name="speaker_tmp", fork=False
            ).run()
            subprocess.check_pid(int(self.res))
            print("Did is run successfully? {}".format(self.res))

        # Have Gstreamer play it
        if skip_player:
            print("[Speaker] skip_player=True")
        else:
            print("[Speaker] skip_player=False")
            for path in self._wavefile:
                path = os.path.abspath(os.path.expanduser(path))
                with player.ScarlettPlayer(path, False, False) as f:
                    print((f.channels))
                    print((f.samplerate))
                    print((f.duration))
                    for s in f:
                        pass

    def create_cmd(self):
        cmd = [
            "espeak",
            "-p%s" % self._pitch,
            "-s%s" % self._speed,
            "-g%s" % self._word_gap,
            "-w",
            self._wavpath,
            "-v%s" % self._voice,
            ".   %s   ." % self._text,
        ]
        print("cmd: {}".format(cmd))
        return cmd

    # Cleanup.
    def close(self, force=False):
        """Close the file and clean up associated resources.

        Calling `close()` a second time has no effect.
        """
        if self.running or force:
            self.running = False
            self.finished = True

    def __del__(self):
        """Garbage Collection, delete Speaker after using it."""
        self.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """If something goes wrong, close class, then return exceptions."""
        self.close()
        return False


# Smoke test.
if __name__ == "__main__":
    if os.environ.get("SCARLETT_DEBUG_MODE"):
        import faulthandler

        faulthandler.register(signal.SIGUSR2, all_threads=True)

        from scarlett_os.internal.debugger import init_debugger
        from scarlett_os.internal.debugger import set_gst_grapviz_tracing

        init_debugger()
        set_gst_grapviz_tracing()
        # Example of how to use it

    from scarlett_os.logger import setup_logger

    setup_logger()

    tts_list = [
        "Hello sir. How are you doing this afternoon?"
        " I am full lee function nall, andd red ee for your commands"
    ]
    for scarlett_text in tts_list:
        with s_thread.time_logger("Scarlett Speaks"):
            path_to_espeak_tmp_wav = os.path.join(
                STATIC_SOUNDS_PATH, "espeak_tmp.wav"
            )
            ScarlettSpeaker(text_to_speak=scarlett_text, wavpath=path_to_espeak_tmp_wav)
