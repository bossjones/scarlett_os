#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_subprocess
----------------------------------
"""

# import ipdb

import os
import sys

import unittest

# import mock
import unittest.mock as mock

# import threading
import pytest


import scarlett_os
from scarlett_os.utility.gnome import trace, abort_on_exception, _IdleObject

from scarlett_os import player
from scarlett_os.player import get_loop_thread, MainLoopThread, ScarlettPlayer

# NOTE: We can't add this here, otherwise we won't be able to mock them
# from scarlett_os.internal.gi import GLib, GObject

from tests import common
import signal
import builtins

# TODO: Handle this error
#
# In [5]: ScarlettPlayer(path, False)
# Error: dot: can't open /home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot
# Out[5]: <player.ScarlettPlayer object at 0x7f62a9ab5d38 (uninitialized at 0x(nil))>

# TODO: Add a test for this
# In [3]: ScarlettPlayer(path)
# TypeError: __init__() missing 1 required positional argument: 'callback'


class TestScarlettPlayer(unittest.TestCase):

    def setUp(self):  # noqa: N802
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """
        # self.mockPlayer = mock.Mock(spec=scarlett_os.player.ScarlettPlayer)
        # self.mockIdleObject = mock.Mock(spec=scarlett_os.utility.gnome._IdleObject)
        pass

    # If spec is an object (rather than a list of strings) then __class__ returns the class of the spec object. This allows mocks to pass isinstance() tests.
    @mock.patch('scarlett_os.player.MainLoopThread', spec=scarlett_os.player.MainLoopThread, name='mock_MainLoopThread')
    @mock.patch('scarlett_os.player._loop_thread_lock', spec=scarlett_os.player._loop_thread_lock, name='mock_scarlett_player_loop_thread_lock')
    @mock.patch('scarlett_os.player.threading.RLock', spec=scarlett_os.player.threading.RLock, name='mock_threading_rlock')
    @mock.patch('scarlett_os.player.threading.Thread', spec=scarlett_os.player.threading.Thread, name='mock_thread_class')
    def test_get_loop_thread(self, mock_thread_class, mock_threading_rlock, mock_scarlett_player_loop_thread_lock, mock_MainLoopThread):
        mock_scarlett_player_loop_thread_lock.return_value = mock_threading_rlock.return_value

        mock_scarlett_player_loop_thread_lock.__enter__ = mock.Mock(name='mock_scarlett_player_loop_thread_lock_enter')
        mock_scarlett_player_loop_thread_lock.__exit__ = mock.Mock(name='mock_scarlett_player_loop_thread_lock_exit')
        mock_scarlett_player_loop_thread_lock.__exit__.return_value = False

        # MainLoopThread()
        mock_MainLoopThread = mock.Mock(spec=scarlett_os.player.MainLoopThread, name='mock_MainLoopThread')

        # actual call
        result = get_loop_thread()

        # tests
        mock_scarlett_player_loop_thread_lock.__enter__.assert_called_once_with()
        mock_scarlett_player_loop_thread_lock.__exit__.assert_called_once_with(None, None, None)
