#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_integration_listener
----------------------------------
"""

###########################################
# Borrowed from test_integration_player - START
###########################################
import os
import sys
import signal
import pytest
import builtins
import threading

import unittest
import unittest.mock as mock

import pydbus
import scarlett_os
import scarlett_os.exceptions

from tests.integration.stubs import create_main_loop

from tests import PROJECT_ROOT
import time

from tests.integration.baseclass import run_emitter_signal
from tests.integration.baseclass import IntegrationTestbaseMainloop

done = 0

from scarlett_os.internal import gi  # noqa
from scarlett_os.internal.gi import Gio  # noqa
from scarlett_os.internal.gi import GObject  # noqa
from scarlett_os.internal.gi import GLib

from scarlett_os import listener
from scarlett_os.utility import threadmanager


###########################################
# Borrowed from test_integration_player - END
###########################################

# source: test_signal.py in pygobject
class C(GObject.GObject):
    """Test class for verifying callbacks."""
    __gsignals__ = {'my_signal': (GObject.SignalFlags.RUN_FIRST, None,
                                  (GObject.TYPE_INT,))}

    def do_my_signal(self, arg):
        self.arg = arg


class TestSuspendableMainLoopThread(object):

    def test_SuspendableMainLoopThread(self, monkeypatch):

        def my_signal_handler_cb(*args):
            assert len(args) == 5
            assert isinstance(args[0], C)
            assert args[0] == inst

            assert isinstance(args[1], int)
            assert args[1] == 42

            assert args[2:] == (1, 2, 3)

        def quit(*args):
            print('timeout reached, lets close out SuspendableMainLoopThread in [test_SuspendableMainLoopThread]')
            with _loop_thread_lock:
                print('SuspendableMainLoopThread attempting to terminate in [test_SuspendableMainLoopThread]')
                _shared_loop_thread.terminate()
                print('SuspendableMainLoopThread attempting to join in [test_SuspendableMainLoopThread]')
                _shared_loop_thread.join(2)

        _shared_loop_thread = None
        _loop_thread_lock = threading.RLock()

        with _loop_thread_lock:
            print('SuspendableMainLoopThread _loop_thread_lock acquired in [test_SuspendableMainLoopThread]')
            if not _shared_loop_thread:
                print('SuspendableMainLoopThread if not _shared_loop_thread in [test_SuspendableMainLoopThread]')
                # Start a new thread.
                _shared_loop_thread = listener.SuspendableMainLoopThread()
                # get MainLoop
                _shared_loop_thread.get_loop()
                # start thread
                _shared_loop_thread.start()
                # this should simply return
                _shared_loop_thread.do_run()
                # FIXME: This is still returning a Mock
                # assert str(type(_shared_loop_thread.get_loop())) == "<class 'gi.overrides.GLib.MainLoop'>"

        inst = C()
        inst.connect("my_signal", my_signal_handler_cb, 1, 2, 3)

        inst.emit("my_signal", 42)
        assert inst.arg == 42

        # Create a timeout that checks how many
        # tasks have been completed. When 2 have finished,
        # kill threads and finish.
        GLib.timeout_add_seconds(10, quit, _shared_loop_thread, _loop_thread_lock)

    # def test_terminate_SuspendableMainLoopThread(self, monkeypatch):

    #     def my_signal_handler_cb(*args):

    #         with pytest.raises(threadmanager.Terminated):
    #             _shared_loop_thread.terminate()

    #     def quit(*args):
    #         print('timeout reached, let close out SuspendableMainLoopThread')
    #         with _loop_thread_lock:
    #             print('attempting to terminate')
    #             _shared_loop_thread.terminate()
    #             print('attempting to join')
    #             _shared_loop_thread.join(2)

    #     _shared_loop_thread = None
    #     _loop_thread_lock = threading.RLock()

    #     with _loop_thread_lock:
    #         if not _shared_loop_thread:
    #             # Start a new thread.
    #             _shared_loop_thread = listener.SuspendableMainLoopThread()
    #             # get MainLoop
    #             _shared_loop_thread.get_loop()
    #             # start thread
    #             _shared_loop_thread.start()
    #             # this should simply return
    #             _shared_loop_thread.do_run()

    #     inst = C()
    #     inst.connect("my_signal", my_signal_handler_cb, 1, 2, 3)

    #     inst.emit("my_signal", 42)

    #     # Create a timeout that checks how many
    #     # tasks have been completed. When 2 have finished,
    #     # kill threads and finish.
    #     GLib.timeout_add_seconds(10, quit)

class TestScarlettListener(object):

    def test_ScarlettListenerI_init(self, monkeypatch):

        sl = listener.ScarlettListenerI('scarlett_listener')

        assert sl.running is False
        assert sl.finished is False
        assert sl.read_exc is None
        assert sl.dot_exc is None
        assert sl.running is False
        assert sl.cancelled is False
        assert sl.name == 'scarlett_listener'
        assert sl._message == 'This is the ScarlettListenerI'
        assert sl.config is None
        assert sl.override_parse == ''
        assert sl.failed == 0
        assert sl.kw_found == 0
        assert sl.debug is False
        assert sl.create_dot is True
        assert sl.terminate is False
        assert sl._status_ready == "  ScarlettListener is ready"
        assert sl._status_kw_match == "  ScarlettListener caught a keyword match"
        assert sl._status_cmd_match == "  ScarlettListener caught a command match"
        assert sl._status_stt_failed == "  ScarlettListener hit Max STT failures"
        assert sl._status_cmd_start == "  ScarlettListener emitting start command"
        assert sl._status_cmd_fin == "  ScarlettListener Emitting Command run finish"
        assert sl._status_cmd_cancel == "  ScarlettListener cancel speech Recognition"
        assert sl.bus is None
        assert sl.bus_message_element_handler_id is None
        assert sl.bus_message_error_handler_id is None
        assert sl.bus_message_eos_handler_id is None
        assert sl.bus_message_state_changed_handler_id is None
        assert sl.pipeline is None
        assert sl.start_time == 0
        assert sl.state == "stopped"
        assert sl.buffer_count == 0
        assert sl.byte_count == 0
        assert sl.kw_to_find == ['scarlett', 'SCARLETT']
