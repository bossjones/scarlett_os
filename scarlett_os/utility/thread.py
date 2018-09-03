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

import os
import sys

import contextlib
import time

if os.environ.get("SCARLETT_DEBUG_MODE"):
    from scarlett_os.internal.debugger import init_debugger

    init_debugger()

import signal
import threading
import logging
import pprint

from scarlett_os.internal.gi import gi
from scarlett_os.internal.gi import GObject
from scarlett_os.internal.gi import GLib
from scarlett_os.internal.gi import Gst
from scarlett_os.internal.gi import Gio

import queue
from urllib.parse import quote

from scarlett_os.utility.gnome import trace
from scarlett_os.utility.gnome import abort_on_exception
from scarlett_os.utility.gnome import _IdleObject

from enum import IntEnum

# global pretty print for debugging
pp = pprint.PrettyPrinter(indent=4)

logger = logging.getLogger(__name__)


# Constants
QUEUE_SIZE = 10
BUFFER_SIZE = 10
SENTINEL = "__GSTDEC_SENTINEL__"


class Priority(IntEnum):
    """Priority constants that map to values in PyGObject."""

    HIGH = 0
    BACKGROUND = 1
    TIMEOUT = 2
    IDLE = 3


@contextlib.contextmanager
def time_logger(name, level=logging.DEBUG):
    """Time logger context manager. Shows how long it takes to run a particular method"""
    start = time.time()
    yield
    logger.log(level, "%s took %dms", name, (time.time() - start) * 1000)


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

# NOTE: From Pitivi
class Thread(threading.Thread, _IdleObject):
    """Event-powered thread."""

    __gsignals__ = {"done": (GObject.SIGNAL_RUN_LAST, None, ())}

    def __init__(self):
        threading.Thread.__init__(self)
        _IdleObject.__init__(self)

    def stop(self):
        """Stops the thread, do not override."""
        self.abort()
        self.emit("done")

    def run(self):
        """Runs the thread."""
        self.process()
        self.emit("done")

    def process(self):
        """Processes the thread.

        Implement this in subclasses.
        """
        raise NotImplementedError

    def abort(self):
        """Aborts the thread.

        Subclass have to implement this method !
        """
        pass


class ThreadManager:
    """
    Manages many FooThreads. This involves starting and stopping
    said threads, and respecting a maximum num of concurrent threads limit
    """

    def __init__(self, maxConcurrentThreads):
        self.maxConcurrentThreads = maxConcurrentThreads
        # stores all threads, running or stopped
        self.fooThreads = {}
        # the pending thread args are used as an index for the stopped threads
        self.pendingFooThreadArgs = []

    def _register_thread_completed(self, thread, *args):
        """
        Decrements the count of concurrent threads and starts any
        pending threads if there is space
        """
        del (self.fooThreads[args])
        running = len(self.fooThreads) - len(self.pendingFooThreadArgs)

        print(
            "{} completed. {} running, {} pending".format(
                thread, running, len(self.pendingFooThreadArgs)
            )
        )

        if running < self.maxConcurrentThreads:
            try:
                args = self.pendingFooThreadArgs.pop()
                print("Starting pending {}".format(self.fooThreads[args]))
                self.fooThreads[args].start()
            except IndexError:
                pass

    def make_thread(self, completedCb, progressCb, threadclass, *args):
        """
        Makes a thread with args. The thread will be started when there is
        a free slot
        """
        running = len(self.fooThreads) - len(self.pendingFooThreadArgs)

        # NOTE: Borrowed from pitivi
        # assert issubclass(threadclass, Thread)
        # self.log("Adding thread of type %r", threadclass)

        if args not in self.fooThreads:
            # threadclass eg ScarlettListenerI
            # OLD: thread = ScarlettListenerI(*args)
            thread = threadclass(*args)
            # signals run in the order connected. Connect the user completed
            # callback first incase they wish to do something
            # before we delete the thread
            thread.connect("completed", completedCb)
            thread.connect("completed", self._register_thread_completed, *args)
            thread.connect("progress", progressCb)
            # This is why we use args, not kwargs, because args are hashable
            self.fooThreads[args] = thread

            if running < self.maxConcurrentThreads:
                print("Starting {}".format(thread))
                self.fooThreads[args].start()
            else:
                print("Queuing {}".format(thread))
                self.pendingFooThreadArgs.append(args)

    def stop_all_threads(self, block=False, timeout=1):
        """
        Stops all threads. If block is True then actually wait for the thread
        to finish (may block the UI)
        """
        for thread in self.fooThreads.values():
            thread.cancel()
            thread.close(True)
            print("stop_all_threads: forced close")
            if block:
                if thread.isAlive():
                    thread.join(timeout=timeout)


def current_thread_name():
    return threading.currentThread().getName()


def id2thread_name(thread_id):
    return threading.Thread.getName(threading._active[thread_id])
