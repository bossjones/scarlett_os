#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Scarlett Thead Utility module."""

# NOTE: THIS IS THE CLASS THAT WILL BE REPLACING scarlett_player.py eventually.
# It is cleaner, more object oriented, and will allows us to run proper tests.
# Also threading.RLock() and threading.Semaphore() works correctly.

#
# There are a LOT of threads going on here, all of them managed by Gstreamer.
# If pyglet ever needs to run under a Python that doesn't have a GIL, some
# locks will need to be introduced to prevent concurrency catastrophes.
#
# At the moment, no locks are used because we assume only one thread is
# executing Python code at a time.  Some semaphores are used to block and wake
# up the main thread when needed, these are all instances of
# threading.Semaphore.  Note that these don't represent any kind of
# thread-safety.

from __future__ import with_statement, division, absolute_import

import os
import sys

from scarlett_os.internal.debugger import init_debugger

init_debugger()

import signal
import threading
import logging
import pprint

from scarlett_os.internal.gi import gi, GObject, GLib, Gst, Gio
#
# from scarlett_os.exceptions import IncompleteGStreamerError, MetadataMissingError, NoStreamError, FileReadError, UnknownTypeError

import queue
from urllib.parse import quote

from scarlett_os.utility.gnome import trace, abort_on_exception, _IdleObject

from enum import IntEnum
# Alias
# gst = Gst

# global pretty print for debugging
pp = pprint.PrettyPrinter(indent=4)

logger = logging.getLogger(__name__)


# Constants
QUEUE_SIZE = 10
BUFFER_SIZE = 10
SENTINEL = '__GSTDEC_SENTINEL__'


class Priority(IntEnum):
    """Priority constants that map to values in PyGObject."""
    HIGH = 0
    BACKGROUND = 1
    TIMEOUT = 2
    IDLE = 3

#############################################################
# NOTE: borrowed from quodlibet.util.thread module
#############################################################


# class Cancellable(object):
#     """Subset of Gio.Cancellable so it can be used as well"""
#
#     def __init__(self):
#         self._cancelled = False
#
#     def is_cancelled(self):
#         return self._cancelled
#
#     def reset(self):
#         self._cancelled = False
#
#     def cancel(self):
#         self._cancelled = True
#
#
# _pools = {}
# _prio_mapping = {
#     # Use this for high priority event sources.
#     Priority.HIGH: GLib.PRIORITY_HIGH,
#
#     # Use this for very low priority background tasks.
#     Priority.BACKGROUND: GLib.PRIORITY_LOW,
#
#     # In GLib this priority is used when adding timeout functions with GLib.timeout_add(). In GDK this priority is used for events from the X server.
#     Priority.TIMEOUT: GLib.PRIORITY_DEFAULT,
#
#     # In GLib this priority is used when adding idle functions with GLib.idle_add().
#     Priority.IDLE: GLib.PRIORITY_DEFAULT_IDLE,
# }

# Managing the Gobject main loop thread.

# _shared_loop_thread = None
# _loop_thread_lock = threading.RLock()
#
#
# def get_loop_thread():
#     """Get the shared main-loop thread.
#     """
#     global _shared_loop_thread
#     with _loop_thread_lock:
#         if not _shared_loop_thread:
#             # Start a new thread.
#             _shared_loop_thread = MainLoopThread()
#             _shared_loop_thread.start()
#         return _shared_loop_thread
#
#
# class MainLoopThread(threading.Thread):
#     """A daemon thread encapsulating a Gobject main loop.
#     """
#
#     def __init__(self):
#         super(MainLoopThread, self).__init__()
#         self.loop = GObject.MainLoop()
#         self.daemon = True
#
#     def run(self):
#         self.loop.run()

# NOTE: Borrowing a couple lines from python3-trepan
# source: https://github.com/mvaled/python3-trepan/blob/3c8ddf94cd12ca72985d82d2cd589f8551a538fd/trepan/lib/thread.py


def current_thread_name():
    return threading.currentThread().getName()


def id2thread_name(thread_id):
    return threading.Thread.getName(threading._active[thread_id])
