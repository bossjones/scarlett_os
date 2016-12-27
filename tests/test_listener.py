#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_listener
----------------------------------
"""

import os
import sys

import unittest
import unittest.mock as mock

import threading
import pytest

import scarlett_os
from scarlett_os.utility.gnome import trace
from scarlett_os.utility.gnome import abort_on_exception
from scarlett_os.utility.gnome import _IdleObject

from scarlett_os import listener
from scarlett_os.listener import get_loop_thread
from scarlett_os.listener import MainLoopThread

from tests import common
import signal
import builtins
import queue

import scarlett_os.exceptions


class TestScarlettListener(unittest.TestCase):

    def setUp(self):  # noqa: N802
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """
        pass

    def tearDown(self):
        pass

    # TODO: Write some better tests going forward
    @mock.patch('scarlett_os.listener.SessionBus', name='mock_pydbus_session_dbus')
    @mock.patch('scarlett_os.listener.Gst', name='mock_gst')
    @mock.patch('scarlett_os.listener.GObject', name='mock_gobject')
    def test_listener_init(self, mock_gobject, mock_gst, mock_pydbus_session_dbus):
        sl = listener.ScarlettListenerI('scarlett_listener')

        self.assertEqual(sl.running, False)
        self.assertEqual(sl.finished, False)
        self.assertEqual(type(sl.ready_sem), threading.Semaphore)
        self.assertEqual(type(sl.queue), queue.Queue)
        self.assertEqual(sl.read_exc, None)
        self.assertEqual(sl.dot_exc, None)
        self.assertEqual(sl.running, False)
        self.assertEqual(sl.cancelled, False)
        self.assertEqual(sl.name, 'scarlett_listener')
        self.assertEqual(sl._message, 'This is the ScarlettListenerI')
        self.assertEqual(sl.config, None)
        self.assertEqual(sl.override_parse, '')
        self.assertEqual(sl.failed, 0)
        self.assertEqual(sl.kw_found, 0)
        self.assertEqual(sl.debug, False)
        self.assertEqual(sl.create_dot, True)
        self.assertEqual(sl.terminate, False)
        self.assertEqual(sl._status_ready, "  ScarlettListener is ready")
        self.assertEqual(sl._status_kw_match, "  ScarlettListener caught a keyword match")
        self.assertEqual(sl._status_cmd_match, "  ScarlettListener caught a command match")
        self.assertEqual(sl._status_stt_failed, "  ScarlettListener hit Max STT failures")
        self.assertEqual(sl._status_cmd_start, "  ScarlettListener emitting start command")
        self.assertEqual(sl._status_cmd_fin, "  ScarlettListener Emitting Command run finish")
        self.assertEqual(sl._status_cmd_cancel, "  ScarlettListener cancel speech Recognition")
        self.assertEqual(sl.bus, None)
        self.assertEqual(sl.bus_message_element_handler_id, None)
        self.assertEqual(sl.bus_message_error_handler_id, None)
        self.assertEqual(sl.bus_message_eos_handler_id, None)
        self.assertEqual(sl.bus_message_state_changed_handler_id, None)
        self.assertEqual(sl.pipeline, None)
        self.assertEqual(sl.start_time, 0)
        self.assertEqual(sl.state, "stopped")
        self.assertEqual(sl.buffer_count, 0)
        self.assertEqual(sl.byte_count, 0)
        self.assertEqual(sl.kw_to_find, ['scarlett', 'SCARLETT'])

    # TODO: Write some better tests going forward
    @mock.patch('scarlett_os.listener.SessionBus', name='mock_pydbus_session_dbus')
    @mock.patch('scarlett_os.listener.Gst', name='mock_gst')
    @mock.patch('scarlett_os.listener.GObject', name='mock_gobject')
    def test_listener_init_fail(self, mock_gobject, mock_gst, mock_pydbus_session_dbus):
        with pytest.raises(IndexError) as excinfo:
            sl = listener.ScarlettListenerI()

        assert 'tuple index out of range' in str(excinfo.value)
