#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_player
----------------------------------
"""

# import ipdb

# import mock
import builtins
import imp
import os
import signal
import sys
import unittest
import unittest.mock as mock

# import threading
import pytest

import scarlett_os
from scarlett_os import player
import scarlett_os.exceptions
from scarlett_os.utility.gnome import _IdleObject, abort_on_exception, trace
from tests import common
from scarlett_os.user import get_user_project_base_path


# DISABLED 5/8/2017 LETS TRY TO DO EVERYTHING FROM player # from scarlett_os.player import get_loop_thread, MainLoopThread, ScarlettPlayer

# NOTE: We can't add this here, otherwise we won't be able to mock them
# from scarlett_os.internal.gi import GLib, GObject


# from scarlett_os.exceptions import (IncompleteGStreamerError, MetadataMissingError, NoStreamError, FileReadError, UnknownTypeError, InvalidUri, UriReadError)

# TODO: Handle this error
#
# In [5]: ScarlettPlayer(path, False)
# Error: dot: can't open /home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot
# Out[5]: <player.ScarlettPlayer object at 0x7f62a9ab5d38 (uninitialized at 0x(nil))>

# TODO: Add a test for this
# In [3]: ScarlettPlayer(path)
# TypeError: __init__() missing 1 required positional argument: 'callback'


# source: https://github.com/YosaiProject/yosai/blob/master/test/isolated_tests/core/conf/conftest.py
@pytest.fixture(scope="function")
def player_unit_mocker_stopall(mocker):
    print("Called [setup]: mocker.stopall()")
    mocker.stopall()
    print("Called [setup]: imp.reload(player)")
    imp.reload(player)
    yield mocker
    print("Called [teardown]: mocker.stopall()")
    mocker.stopall()
    print("Called [setup]: imp.reload(player)")
    imp.reload(player)


# pylint: disable=R0201
# pylint: disable=C0111
# pylint: disable=C0123
# pylint: disable=C0103
# pylint: disable=W0212
# pylint: disable=W0621
# pylint: disable=W0612
@pytest.mark.scarlettonly
@pytest.mark.unittest
@pytest.mark.scarlettonlyunittest
class TestScarlettPlayer(object):
    def test_get_loop_thread(self, player_unit_mocker_stopall):
        "Replace job of old setUp function in unittest"
        temp_mocker = player_unit_mocker_stopall

        # FYI This is what we need?
        # def testContextManagerMocking(self):
        #     mock = Mock()
        #     mock.__enter__ = Mock()
        #     mock.__exit__ = Mock()
        #     mock.__exit__.return_value = False
        #     with mock as m:
        #         self.assertEqual(m, mock.__enter__.return_value)
        #     mock.__enter__.assert_called_with()
        #     mock.__exit__.assert_called_with(None, None, None)

        mock_rlock = temp_mocker.MagicMock(name="mock_rlock")
        mock_rlock.__enter__ = temp_mocker.MagicMock(name="mock_rlock_enter")
        mock_rlock.__exit__ = temp_mocker.MagicMock(name="mock_rlock_exit")
        mock_rlock.__exit__.return_value = False

        mock_scarlett_player_loop_thread_lock = temp_mocker.MagicMock(
            name="mock_scarlett_player_loop_thread_lock"
        )
        mock_scarlett_player_loop_thread_lock.return_value = mock_rlock.return_value

        # NOTE: Instead of autospec=True you can pass autospec=some_object to use an arbitrary object as the spec instead of the one being replaced.
        # CREATE mock objects
        mock_semaphore = temp_mocker.MagicMock(
            name="mock_semaphore",
            return_value=temp_mocker.Mock(name="mock_semaphore_return_val"),
        )
        mock_MainLoopThread = temp_mocker.MagicMock(
            name="mock_MainLoopThread", autospec=scarlett_os.player.MainLoopThread
        )

        # set mock attributes
        mock_thread_class = temp_mocker.MagicMock(
            name="mock_thread_class", spec=scarlett_os.player.threading.Thread
        )

        # patch everything
        temp_mocker.patch.object(
            scarlett_os.player.threading, "Semaphore", mock_semaphore
        )
        temp_mocker.patch.object(
            scarlett_os.player, "MainLoopThread", mock_MainLoopThread
        )
        temp_mocker.patch.object(
            scarlett_os.player,
            "_loop_thread_lock",
            mock_scarlett_player_loop_thread_lock,
        )

        # actual call
        result = player.get_loop_thread()

        # tests
        mock_scarlett_player_loop_thread_lock.__enter__.assert_called_once_with()
        mock_scarlett_player_loop_thread_lock.__exit__.assert_called_once_with(
            None, None, None
        )

    def test_MainLoopThread(self, player_unit_mocker_stopall):
        temp_mocker = player_unit_mocker_stopall
        # CREATE mock objects
        mock_thread_class = temp_mocker.MagicMock(
            name="mock_thread_class", spec=scarlett_os.player.threading.Thread
        )

        mock_GObject_MainLoop = temp_mocker.MagicMock(
            name="mock_GObject_MainLoop", spec=scarlett_os.player.GObject.MainLoop
        )
        # mock_GObject_MainLoop.name = 'mock_gobject_mainloop #1'
        mock_GLib_MainLoop = temp_mocker.MagicMock(
            name="mock_GLib_MainLoop", spec=scarlett_os.player.GLib.MainLoop
        )

        test_MainLoopThread = player.MainLoopThread()

        assert not mock_GLib_MainLoop.called
        assert test_MainLoopThread.daemon is True

    def test_ScarlettPlayer_init_fail_no_args(self):
        # No args
        # TODO: Turn this into a side_effect
        with pytest.raises(TypeError):
            p = player.ScarlettPlayer()

        with pytest.raises(TypeError):
            p = player.ScarlettPlayer(False)

        with pytest.raises(TypeError):
            p = player.ScarlettPlayer(False, False)

    def test_ScarlettPlayer_init_fail_bad_uri(self):

        path = "blahgrdughdfg"
        with pytest.raises(scarlett_os.exceptions.UriReadError):
            player.ScarlettPlayer(path, False, False)

    def test_ScarlettPlayer_init_isReadable_raises_exception_UriReadError(self):
        path = "blahgrdughdfg"
        with mock.patch(
            "scarlett_os.player.isReadable", mock.Mock(return_value=False)
        ) as mock_isReadable:  # noqa
            with pytest.raises(scarlett_os.exceptions.UriReadError):
                p = player.ScarlettPlayer(path, False, False)
        assert mock_isReadable.call_count == 1

    def test_ScarlettPlayer_init_uri_is_valid_raises_exception_InvalidUri(self):
        path = "blahgrdughdfg"
        with mock.patch(
            "scarlett_os.player.uri_is_valid", mock.Mock(return_value=False)
        ) as mock_uri_is_valid:  # noqa
            with pytest.raises(scarlett_os.exceptions.InvalidUri):
                p = player.ScarlettPlayer(path, False, False)

    @mock.patch(
        "scarlett_os.player.Gst.ElementFactory.make",
        return_value=None,
        spec=scarlett_os.player.Gst.ElementFactory.make,
        name="mock_gst_elementfactory_make",
    )
    def test_ScarlettPlayer_init_missing_gst_elements(
        self, mock_gst_elementfactory_make
    ):
        path = os.path.join(
            get_user_project_base_path() + "/static/sounds", "pi-listening.wav"
        )
        with pytest.raises(scarlett_os.exceptions.IncompleteGStreamerError):
            p = player.ScarlettPlayer(path, False, False)
