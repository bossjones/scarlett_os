#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_listener
----------------------------------
"""

import os
import sys

import pytest
import unittest
import unittest.mock as mock
from mock import call

import scarlett_os
from scarlett_os import listener  # Module with our thing to test
from scarlett_os.utility import gnome  # Module with the decorator we need to replace

import time
from scarlett_os.internal.gi import gi
from scarlett_os.internal.gi import GLib
from scarlett_os.internal.gi import GObject
from scarlett_os.internal.gi import Gio
import pydbus
from pydbus import SessionBus

# NOTE: We can't add this here, otherwise we won't be able to mock them
# from tests import common
import signal
import builtins
import scarlett_os.exceptions

import imp  # Library to help us reload our tasker module


class TestScarlettListener(unittest.TestCase):

    def setUp(self):  # noqa: N802
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """
        # source: http://stackoverflow.com/questions/7667567/can-i-patch-a-python-decorator-before-it-wraps-a-function
        # Do cleanup first so it is ready if an exception is raised
        def kill_patches():  # Create a cleanup callback that undoes our patches
            mock.patch.stopall()  # Stops all patches started with start()
            imp.reload(listener)  # Reload our UUT module which restores the original decorator
        self.addCleanup(kill_patches)  # We want to make sure this is run so we do this in addCleanup instead of tearDown

        self.old_glib_exception_error = GLib.GError
        # Now patch the decorator where the decorator is being imported from
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_abort_on_exception = mock.patch('scarlett_os.utility.gnome.abort_on_exception', lambda x: x).start()
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_gi = mock.patch('scarlett_os.internal.gi.gi', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_glib = mock.patch('scarlett_os.internal.gi.GLib', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_gobject = mock.patch('scarlett_os.internal.gi.GObject', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_gio = mock.patch('scarlett_os.internal.gi.Gio', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_pydbus_SessionBus = mock.patch('pydbus.SessionBus', spec=True, create=True).start()

        imp.reload(listener)  # Reloads the listener.py module which applies our patched decorator

    def tearDown(self):
        # del(self._handler)
        # self._handler = None
        pass

    # STOLE THIS FROM TASKER, USE IT TO FIX LISTENER
    @mock.patch('scarlett_os.utility.dbus_runner.DBusRunner', autospec=True, name='mock_dbusrunner')
    @mock.patch('scarlett_os.utility.dbus_utils.DbusSignalHandler', spec=scarlett_os.utility.dbus_utils.DbusSignalHandler, name='mock_listener_signal_handler')
    @mock.patch('scarlett_os.listener.time.sleep', name='mock_time_sleep')
    @mock.patch('scarlett_os.listener.logging.Logger.debug', name='mock_logger_debug')
    @mock.patch('scarlett_os.listener._IdleObject', name='mock_idle_obj')
    @mock.patch('scarlett_os.listener.ThreadManager', name='mock_thread_manager')
    @mock.patch('scarlett_os.listener.threading.RLock', spec=scarlett_os.listener.threading.RLock, name='mock_threading_rlock')
    @mock.patch('scarlett_os.listener.threading.Event', spec=scarlett_os.listener.threading.Event, name='mock_threading_event')
    @mock.patch('scarlett_os.listener.threading.Thread', spec=scarlett_os.listener.threading.Thread, name='mock_thread_class')
    def test_listener_init(self, mock_thread_class, mock_threading_event, mock_threading_rlock, mock_thread_manager, mock_idle_obj, mock_logger_debug, mock_time_sleep, mock_listener_signal_handler, mock_dbusrunner):
        sl = listener.ScarlettListenerI('scarlett_listener')

        self.assertEqual(sl.running, False)
        self.assertEqual(sl.finished, False)
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

    # # TODO: Write some better tests going forward
    # @mock.patch('scarlett_os.listener.SessionBus', name='mock_pydbus_session_dbus')
    # @mock.patch('scarlett_os.listener.Gst', name='mock_gst')
    # @mock.patch('scarlett_os.listener.GObject', name='mock_gobject')
    # def test_listener_init(self, mock_gobject, mock_gst, mock_pydbus_session_dbus):
    #     sl = listener.ScarlettListenerI('scarlett_listener')
    #
    #     self.assertEqual(sl.running, False)
    #     self.assertEqual(sl.finished, False)
    #     self.assertEqual(type(sl.ready_sem), threading.Semaphore)
    #     self.assertEqual(type(sl.queue), queue.Queue)
    #     self.assertEqual(sl.read_exc, None)
    #     self.assertEqual(sl.dot_exc, None)
    #     self.assertEqual(sl.running, False)
    #     self.assertEqual(sl.cancelled, False)
    #     self.assertEqual(sl.name, 'scarlett_listener')
    #     self.assertEqual(sl._message, 'This is the ScarlettListenerI')
    #     self.assertEqual(sl.config, None)
    #     self.assertEqual(sl.override_parse, '')
    #     self.assertEqual(sl.failed, 0)
    #     self.assertEqual(sl.kw_found, 0)
    #     self.assertEqual(sl.debug, False)
    #     self.assertEqual(sl.create_dot, True)
    #     self.assertEqual(sl.terminate, False)
    #     self.assertEqual(sl._status_ready, "  ScarlettListener is ready")
    #     self.assertEqual(sl._status_kw_match, "  ScarlettListener caught a keyword match")
    #     self.assertEqual(sl._status_cmd_match, "  ScarlettListener caught a command match")
    #     self.assertEqual(sl._status_stt_failed, "  ScarlettListener hit Max STT failures")
    #     self.assertEqual(sl._status_cmd_start, "  ScarlettListener emitting start command")
    #     self.assertEqual(sl._status_cmd_fin, "  ScarlettListener Emitting Command run finish")
    #     self.assertEqual(sl._status_cmd_cancel, "  ScarlettListener cancel speech Recognition")
    #     self.assertEqual(sl.bus, None)
    #     self.assertEqual(sl.bus_message_element_handler_id, None)
    #     self.assertEqual(sl.bus_message_error_handler_id, None)
    #     self.assertEqual(sl.bus_message_eos_handler_id, None)
    #     self.assertEqual(sl.bus_message_state_changed_handler_id, None)
    #     self.assertEqual(sl.pipeline, None)
    #     self.assertEqual(sl.start_time, 0)
    #     self.assertEqual(sl.state, "stopped")
    #     self.assertEqual(sl.buffer_count, 0)
    #     self.assertEqual(sl.byte_count, 0)
    #     self.assertEqual(sl.kw_to_find, ['scarlett', 'SCARLETT'])
    #
    # # TODO: Write some better tests going forward
    # @mock.patch('scarlett_os.listener.SessionBus', name='mock_pydbus_session_dbus')
    # @mock.patch('scarlett_os.listener.Gst', name='mock_gst')
    # @mock.patch('scarlett_os.listener.GObject', name='mock_gobject')
    # def test_listener_init_fail(self, mock_gobject, mock_gst, mock_pydbus_session_dbus):
    #     name = "Thread #1337"
    #     sl = listener.ScarlettListenerI(name)
    #
    #     # with pytest.raises(IndexError) as excinfo:
    #     #     sl = listener.ScarlettListenerI(name)
    #     #
    #     # assert 'tuple index out of range' in str(excinfo.value)
