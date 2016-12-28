#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_tasker
----------------------------------
"""

import os
import sys

import pytest
import unittest
import unittest.mock as mock

import scarlett_os

from scarlett_os.internal.gi import gi
from scarlett_os.internal.gi import GLib
from scarlett_os.internal.gi import GObject

from scarlett_os import tasker  # Module with our thing to test
from scarlett_os.utility import gnome  # Module with the decorator we need to replace

# NOTE: We can't add this here, otherwise we won't be able to mock them
# from tests import common
import signal
import builtins
import scarlett_os.exceptions

import imp  # Library to help us reload our tasker module


class TestScarlettTasker(unittest.TestCase):

    def setUp(self):  # noqa: N802
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """
        # source: http://stackoverflow.com/questions/7667567/can-i-patch-a-python-decorator-before-it-wraps-a-function
        # Do cleanup first so it is ready if an exception is raised
        def kill_patches():  # Create a cleanup callback that undoes our patches
            mock.patch.stopall()  # Stops all patches started with start()
            imp.reload(tasker)  # Reload our UUT module which restores the original decorator
        self.addCleanup(kill_patches)  # We want to make sure this is run so we do this in addCleanup instead of tearDown

        # Now patch the decorator where the decorator is being imported from
        mock_abort_on_exception = mock.patch('scarlett_os.utility.gnome.abort_on_exception', lambda x: x).start()  # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_gi = mock.patch('scarlett_os.internal.gi.gi', spec=True).start()  # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()

        mock_glib = mock.patch('scarlett_os.internal.gi.GLib', spec=True).start()  # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()

        mock_gobject = mock.patch('scarlett_os.internal.gi.GObject', spec=True).start()  # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()

        # HINT: if you're patching a decor with params use something like:
        # lambda *x, **y: lambda f: f
        imp.reload(tasker)  # Reloads the uut.py module which applies our patched decorator

    def tearDown(self):
        pass

    # from scarlett_os.utility.gnome import abort_on_exception
    # from scarlett_os.utility.gnome import _IdleObject
    #
    # from scarlett_os.utility import thread as s_thread
    # from scarlett_os import player
    # from scarlett_os import speaker
    # from scarlett_os import commands
    #
    # from pydbus import SessionBus

    # # TODO: Write some better tests going forward
    # @mock.patch('scarlett_os.listener.SessionBus', name='mock_pydbus_session_dbus')
    # @mock.patch('scarlett_os.listener.Gst', name='mock_gst')
    # @mock.patch('scarlett_os.listener.GObject', name='mock_gobject')
    # def test_listener_init_fail(self, mock_gobject, mock_gst, mock_pydbus_session_dbus):
    #     with pytest.raises(IndexError) as excinfo:
    #         sl = listener.ScarlettListenerI()
    #
    #     assert 'tuple index out of range' in str(excinfo.value)

    @mock.patch('scarlett_os.tasker._IdleObject', name='mock_idle_obj')
    @mock.patch('scarlett_os.tasker.GLib', autospec=True, create=True, name='mock_glib')
    @mock.patch('scarlett_os.tasker.GObject', name='mock_gobject')
    @mock.patch('scarlett_os.tasker.SessionBus', name='mock_scarlett_pydbus_sessionbus')
    @mock.patch('scarlett_os.utility.thread.time_logger', name='mock_time_logger')
    @mock.patch('scarlett_os.tasker.speaker', name='mock_scarlett_speaker')
    @mock.patch('scarlett_os.tasker.player', name='mock_scarlett_player')
    @mock.patch('scarlett_os.tasker.commands', name='mock_scarlett_commands')
    @mock.patch('scarlett_os.tasker.threading.RLock', spec=scarlett_os.tasker.threading.RLock, name='mock_threading_rlock')
    @mock.patch('scarlett_os.tasker.threading.Event', spec=scarlett_os.tasker.threading.Event, name='mock_threading_event')
    @mock.patch('scarlett_os.tasker.threading.Thread', spec=scarlett_os.tasker.threading.Thread, name='mock_thread_class')
    def test_tasker_init(self, mock_thread_class, mock_threading_event, mock_threading_rlock, mock_scarlett_commands, mock_scarlett_player, mock_scarlett_speaker, mock_time_logger, mock_scarlett_pydbus_sessionbus, mock_gobject, mock_glib, mock_idle_obj):
        # from scarlett_os.internal.gi import gi, GLib
        # mock_glib.MainLoop = mock.MagicMock('scarlett_os.tasker.GLib.MainLoop', name='Mock_GLib.MainLoop')
        # mock_scarlett_pydbus_sessionbus
        # # # with SessionBus() as bus:
        # # bus = SessionBus()
        # # ss = bus.get("org.scarlett", object_path='/org/scarlett/Listener')  # NOQA
        # # time.sleep(1)

        # @mock.patch('scarlett_os.player.MainLoopThread', spec=scarlett_os.player.MainLoopThread, name='mock_MainLoopThread')
        # @mock.patch('scarlett_os.player._loop_thread_lock', spec=scarlett_os.player._loop_thread_lock, name='mock_scarlett_player_loop_thread_lock')
        # @mock.patch('scarlett_os.player.threading.RLock', spec=scarlett_os.player.threading.RLock, name='mock_threading_rlock')
        # @mock.patch('scarlett_os.player.threading.Thread', spec=scarlett_os.player.threading.Thread, name='mock_thread_class')
        # def test_get_loop_thread(self, mock_thread_class, mock_threading_rlock, mock_scarlett_player_loop_thread_lock, mock_MainLoopThread):
        #     mock_scarlett_player_loop_thread_lock.return_value = mock_threading_rlock.return_value
        #
        #     mock_scarlett_player_loop_thread_lock.__enter__ = mock.Mock(name='mock_scarlett_player_loop_thread_lock_enter')
        #     mock_scarlett_player_loop_thread_lock.__exit__ = mock.Mock(name='mock_scarlett_player_loop_thread_lock_exit')
        #     mock_scarlett_player_loop_thread_lock.__exit__.return_value = False
        #
        #     # MainLoopThread()
        #     mock_MainLoopThread = mock.Mock(spec=scarlett_os.player.MainLoopThread, name='mock_MainLoopThread')

        #
        with pytest.raises(TypeError) as excinfo:
            tskr = tasker.ScarlettTasker()
        #
        assert 'ScarlettListener(org.scarlett, /org/scarlett/Listener)>: unknown signal name: aborted' in str(excinfo.value)
