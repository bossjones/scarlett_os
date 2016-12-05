#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_subprocess
----------------------------------
"""

import os
import sys

import unittest

# import mock
import unittest.mock as mock

import threading

import scarlett_os
from scarlett_os.utility.gnome import trace, abort_on_exception, _IdleObject

import scarlett_os.player
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

    def test_get_loop_thread(self):
        # scarlett_os.player.ScarlettPlayer.__init__(
        #     self.mock, Mock(), {}, sock, (sentinel.host, sentinel.port),
        #     sentinel.timeout)
        # sock.setblocking.assert_called_once_with(False)
        pass
