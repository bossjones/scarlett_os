#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_player
----------------------------------
"""

# import ipdb

import os
import sys

import unittest

# import mock
import unittest.mock as mock

import threading
import pytest


import scarlett_os
from scarlett_os.utility.gnome import trace
from scarlett_os.utility.gnome import abort_on_exception
from scarlett_os.utility.gnome import _IdleObject

from scarlett_os import player
from scarlett_os.player import get_loop_thread, MainLoopThread, ScarlettPlayer

# NOTE: We can't add this here, otherwise we won't be able to mock them
# from scarlett_os.internal.gi import GLib, GObject

from tests import common
import signal
import builtins

import scarlett_os.exceptions

# from scarlett_os.exceptions import (IncompleteGStreamerError, MetadataMissingError, NoStreamError, FileReadError, UnknownTypeError, InvalidUri, UriReadError)

# TODO: Handle this error
#
# In [5]: ScarlettPlayer(path, False)
# Error: dot: can't open /home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot
# Out[5]: <player.ScarlettPlayer object at 0x7f62a9ab5d38 (uninitialized at 0x(nil))>

# TODO: Add a test for this
# In [3]: ScarlettPlayer(path)
# TypeError: __init__() missing 1 required positional argument: 'callback'

import imp

# source: https://github.com/YosaiProject/yosai/blob/master/test/isolated_tests/core/conf/conftest.py
@pytest.fixture(scope='function')
def player_unit_mocker_stopall(mocker):
    "Stop previous mocks, yield mocker plugin obj, then stopall mocks again"
    print('Called [setup]: mocker.stopall()')
    mocker.stopall()
    print('Called [setup]: imp.reload(player)')
    imp.reload(player)
    yield mocker
    print('Called [teardown]: mocker.stopall()')
    mocker.stopall()
    print('Called [setup]: imp.reload(player)')
    imp.reload(player)


# pylint: disable=R0201
# pylint: disable=C0111
# pylint: disable=C0123
# pylint: disable=C0103
# pylint: disable=W0212
# pylint: disable=W0621
# pylint: disable=W0612
@pytest.mark.unittest
class TestScarlettPlayer(object):

    def test_get_loop_thread(self, player_unit_mocker_stopall):
        "Replace job of old setUp function in unittest"
        temp_mocker = player_unit_mocker_stopall

        temp_mocker.patch('threading.Semaphore', return_value=temp_mocker.MagicMock())
        mock_MainLoopThread = temp_mocker.patch('scarlett_os.player.MainLoopThread', spec=scarlett_os.player.MainLoopThread, name='mock_MainLoopThread')
        mock_scarlett_player_loop_thread_lock = temp_mocker.patch('scarlett_os.player._loop_thread_lock', spec=scarlett_os.player._loop_thread_lock, name='mock_scarlett_player_loop_thread_lock')
        mock_threading_rlock = temp_mocker.patch('scarlett_os.player.threading.RLock', spec=scarlett_os.player.threading.RLock, name='mock_threading_rlock')
        temp_mocker.patch('scarlett_os.player.threading.Thread', spec=scarlett_os.player.threading.Thread, name='mock_thread_class')

        mock_scarlett_player_loop_thread_lock.return_value = mock_threading_rlock.return_value

        mock_scarlett_player_loop_thread_lock.__enter__ = temp_mocker.MagicMock(name='mock_scarlett_player_loop_thread_lock_enter')
        mock_scarlett_player_loop_thread_lock.__exit__ = temp_mocker.MagicMock(name='mock_scarlett_player_loop_thread_lock_exit')
        mock_scarlett_player_loop_thread_lock.__exit__.return_value = False

        # actual call
        result = get_loop_thread()

        # tests
        mock_scarlett_player_loop_thread_lock.__enter__.assert_called_once_with()
        mock_scarlett_player_loop_thread_lock.__exit__.assert_called_once_with(None, None, None)

    def test_MainLoopThread(self, player_unit_mocker_stopall):
        temp_mocker = player_unit_mocker_stopall
        temp_mocker.patch('scarlett_os.player.threading.Thread', spec=scarlett_os.player.threading.Thread, name='mock_thread_class')
        # Import module locally for testing purposes
        from scarlett_os.internal.gi import gi, GObject

        mock_GObject_MainLoop = temp_mocker.patch.object(__name__, 'GObject.MainLoop', autospec=True)

        # Mock function GLib function spawn_async
        # GObject.MainLoop = temp_mocker.create_autospec(GObject.spawn_async, name='Mock_GObject.MainLoop')

        test_MainLoopThread = MainLoopThread()
        test_MainLoopThread.start()

        assert mock_GObject_MainLoop.called
        assert test_MainLoopThread.loop.run.called
        assert test_MainLoopThread.daemon == True

    def test_ScarlettPlayer_init_fail_no_args(self):
        # No args
        # TODO: Turn this into a side_effect
        with pytest.raises(TypeError):
            p = ScarlettPlayer()

        with pytest.raises(TypeError):
            p = ScarlettPlayer(False)

        with pytest.raises(TypeError):
            p = ScarlettPlayer(False, False)

    def test_ScarlettPlayer_init_fail_bad_uri(self):

        path = 'blahgrdughdfg'
        with pytest.raises(scarlett_os.exceptions.UriReadError):
            player.ScarlettPlayer(path, False, False)

    def test_ScarlettPlayer_init_isReadable_raises_exception_UriReadError(self):
        path = 'blahgrdughdfg'
        with mock.patch('scarlett_os.player.isReadable', mock.Mock(return_value=False)) as mock_isReadable:  # noqa
            with pytest.raises(scarlett_os.exceptions.UriReadError):
                p = player.ScarlettPlayer(path, False, False)
        assert mock_isReadable.call_count == 1

    def test_ScarlettPlayer_init_uri_is_valid_raises_exception_InvalidUri(self):
        path = 'blahgrdughdfg'
        with mock.patch('scarlett_os.player.uri_is_valid', mock.Mock(return_value=False)) as mock_uri_is_valid:  # noqa
            with pytest.raises(scarlett_os.exceptions.InvalidUri):
                p = player.ScarlettPlayer(path, False, False)

    @mock.patch('scarlett_os.player.Gst.ElementFactory.make', return_value=None, spec=scarlett_os.player.Gst.ElementFactory.make, name='mock_gst_elementfactory_make')
    def test_ScarlettPlayer_init_missing_gst_elements(self, mock_gst_elementfactory_make):
        path = '/home/pi/dev/bossjones-github/scarlett_os/static/sounds/pi-listening.wav'
        with pytest.raises(scarlett_os.exceptions.IncompleteGStreamerError):
            p = player.ScarlettPlayer(path, False, False)

    # @mock.patch('scarlett_os.player.compat.bytes.decode', return_value=u'/home/pi/dev/bossjones-github/scarlett_os/static/sounds/pi-listening.wav', name='mock_str_decode')
    # def test_ScarlettPlayer_init_fail_uri_is_valid(self, mock_str_decode):
    #     path = b'/home/pi/dev/bossjones-github/scarlett_os/static/sounds/pi-listening.wav'
    #     with pytest.raises(scarlett_os.exceptions.InvalidUri):
    #         player.ScarlettPlayer(path, False, False)

    def test_ScarlettPlayer_init_fail_invalid_path(self):

        # fd_unused, path = tempfile.mkstemp(suffix=".wav")
        #
        # try:
        #     # run test
        #     result = s_path.isReadable(path)
        #
        #     # tests
        #     self.assertTrue(result)
        # finally:
        #     os.remove(path)
        #
        # with pytest.raises(TypeError):
        #     ScarlettPlayer()
        pass

    # NOTE: While trying to get this working, I found myself needing to go back over basic python class design principals.
    # NOTE: I am not 100% sure if the scarlett player as it is currently implemented is actually testable or not.
    # @mock.patch('scarlett_os.player.GObject.MainLoop', spec=scarlett_os.player.GObject.MainLoop, name='mock_gobject_mainloop')
    # @mock.patch('scarlett_os.player.Gst.Pipeline.new', spec=scarlett_os.player.Gst.Pipeline.new, name='mock_player_gst_pipeline_new')
    # @mock.patch('scarlett_os.player.threading.Semaphore', spec=scarlett_os.player.threading.Semaphore, name='mock_threading_semaphore')
    # @mock.patch('scarlett_os.player.MainLoopThread', spec=scarlett_os.player.MainLoopThread, name='mock_MainLoopThread')
    # @mock.patch('scarlett_os.player._loop_thread_lock', spec=scarlett_os.player._loop_thread_lock, name='mock_scarlett_player_loop_thread_lock')
    # @mock.patch('scarlett_os.player.threading.RLock', spec=scarlett_os.player.threading.RLock, name='mock_threading_rlock')
    # @mock.patch('scarlett_os.player.threading.Thread', spec=scarlett_os.player.threading.Thread, name='mock_thread_class')
    # def test_ScarlettPlayer_init_pipline_calls(self, mock_thread_class, mock_threading_rlock, mock_scarlett_player_loop_thread_lock, mock_MainLoopThread):
    #     # NOTE: Currently this works like an integration test
    #     threading.Semaphore = mock.MagicMock()
    #
    #     # # mock everything
    #     mock_scarlett_player_loop_thread_lock.return_value = mock_threading_rlock.return_value
    #     mock_scarlett_player_loop_thread_lock.__enter__ = mock.Mock(name='mock_scarlett_player_loop_thread_lock_enter')
    #     mock_scarlett_player_loop_thread_lock.__exit__ = mock.Mock(name='mock_scarlett_player_loop_thread_lock_exit')
    #     mock_scarlett_player_loop_thread_lock.__exit__.return_value = False
    #     #
    #     # mock_threading_semaphore.__enter__ = mock.Mock(name='mock_threading_semaphore_enter')
    #     # mock_threading_semaphore.__exit__ = mock.Mock(name='mock_threading_semaphore_exit', return_value=False)
    #     #
    #     # mock_MainLoopThread = mock.Mock(spec=scarlett_os.player.MainLoopThread, name='mock_MainLoopThread')  # noqa
    #     # mock_MainLoopThread.loop = mock_gobject_mainloop.return_value
    #     #
    #     path = '/home/pi/dev/bossjones-github/scarlett_os/static/sounds/pi-listening.wav'
    #     # # import pdb;pdb.set_trace()  # noqa
    #     p = player.ScarlettPlayer(path, False, False)
    #     #
    #     # self.assertEqual(type(p), ScarlettPlayer)
    #     threading.Semaphore.assert_called_once_with(0)
    #     #
    #     #
    #     pass

    # DO THIS NEXT
    # @mock.patch('scarlett_os.player.threading.Semaphore', spec=scarlett_os.player.threading.Semaphore, name='mock_threading_semaphore')
    # @mock.patch('scarlett_os.player.threading.Thread', spec=scarlett_os.player.threading.Thread, name='mock_thread_class')
    # def test_ScarlettPlayer_init_fail_no_args(self, mock_thread_class, mock_threading_semaphore):
    #     # Import module locally for testing purposes
    #     # from scarlett_os.internal.gi import gi, GObject, Gst
    #     #
    #     # mock_gobject = mock.Mock(spec=scarlett_os.player.GObject, name='mock_gobject')
    #     # mock_gst = mock.Mock(spec=scarlett_os.player.Gst, name='mock_gst')
    #     #
    #     # # # Mock function GLib function spawn_async
    #     # # GObject.MainLoop = mock.create_autospec(GObject.spawn_async, name='Mock_GObject.MainLoop')
    #     # #
    #     # # test_MainLoopThread = MainLoopThread()
    #     # # test_MainLoopThread.start()
    #     # #
    #     # # self.assertTrue(GObject.MainLoop.called)
    #     # # self.assertEqual(test_MainLoopThread.daemon, True)
    #
    #     with pytest.raises(TypeError):
    #         # E TypeError: __init__() missing 3 required positional arguments: 'path', 'handle_error', and 'callback'
    #         ScarlettPlayer()
