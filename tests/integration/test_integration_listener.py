#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_integration_listener
----------------------------------
"""

##########################################
# Original imports
##########################################
# import os
# import sys
# import signal
# import pytest
# import builtins
# import threading
#
# import unittest
# import unittest.mock as mock
#
# import pydbus
# import scarlett_os
# import scarlett_os.exceptions
#
# from tests.integration.stubs import create_main_loop
#
# from tests import PROJECT_ROOT
# import time
#
# from tests.integration.baseclass import run_emitter_signal
# from tests.integration.baseclass import IntegrationTestbaseMainloop
#
# done = 0
#
# from scarlett_os.internal import gi  # noqa
# from scarlett_os.internal.gi import Gio  # noqa
# from scarlett_os.internal.gi import GObject  # noqa
# from scarlett_os.internal.gi import GLib
#
# from scarlett_os import listener
#
#
###########################################

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
            print('timeout reached, let close out SuspendableMainLoopThread')
            with _loop_thread_lock:
                print('attempting to terminate')
                _shared_loop_thread.terminate()
                print('attempting to join')
                _shared_loop_thread.join(2)

        _shared_loop_thread = None
        _loop_thread_lock = threading.RLock()

        with _loop_thread_lock:
            if not _shared_loop_thread:
                # Start a new thread.
                _shared_loop_thread = listener.SuspendableMainLoopThread()
                _shared_loop_thread.start()

        inst = C()
        inst.connect("my_signal", my_signal_handler_cb, 1, 2, 3)

        inst.emit("my_signal", 42)
        assert inst.arg == 42

        # Create a timeout that checks how many tasks have been completed. When 2 have finished, kill threads and finish.
        GLib.timeout_add_seconds(10, quit)


class TestScarlettListener(object):

    def test_ScarlettListenerI_init(self, monkeypatch):
        # we want to use pulsesink by default but in docker we might
        # not have a pulseaudio server running
        # test using fakesink in this usecase
        # monkeypatch.setattr(listener.ScarlettListenerI, 'DEFAULT_SINK', 'fakesink')

        # listener_data = []

        # Run listener
        # wavefile = [
        #     '/home/pi/dev/bossjones-github/scarlett_os/static/sounds/pi-listening.wav']
        # for path in wavefile:
        #     path = os.path.abspath(os.path.expanduser(path))
        #     with listener.ScarlettListenerI(path, False is False as f:
        #         listener_data.append(f)

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

        # # Test audio info
        # assert listener_data[0].channels == 2
        # assert listener_data[0].samplerate == 44100
        # assert listener_data[0].duration == 2.5
        #
        # # Check values of elements
        # assert str(type(listener_data[0].source)) == "<class '__gi__.GstURIDecodeBin'>"
        # assert str(type(listener_data[0].queueA)) == "<class '__gi__.GstQueue'>"
        # assert str(type(listener_data[0].queueB)) == "<class '__gi__.GstQueue'>"
        # assert str(type(listener_data[0].appsink)) == "<class '__gi__.GstAppSink'>"
        # assert str(type(listener_data[0].audioconvert)) == "<class '__gi__.GstAudioConvert'>"
        # assert str(type(listener_data[0].splitter)) == "<class '__gi__.GstTee'>"
        # assert str(type(listener_data[0].pulsesink)) == "<class '__gi__.GstFakeSink'>"
        # # assert str(type(listener_data[0].queueB_sink_pad)) == "<class 'gi.overrides.Gst.Pad'>"
        #
        # # Means pipeline was setup correct and ran without error
        # assert listener_data[0].read_exc is None
        # assert listener_data[0].dot_exc is None
        # assert listener_data[0].handle_error is False
        #
        # # Test
        # assert listener_data[0].got_caps is True
        # assert listener_data[0].running is False
        # assert listener_data[0].finished is True
