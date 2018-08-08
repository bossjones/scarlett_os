#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_tasker
----------------------------------
"""

# NOTE: We can't add this here, otherwise we won't be able to mock them
# from tests import common
import builtins
import imp
import os
import signal
import sys
import time
import unittest
import unittest.mock as mock

from mock import call
import pydbus
from pydbus import SessionBus
import pytest

import scarlett_os
from scarlett_os import tasker  # Module with our thing to test
import scarlett_os.exceptions
from scarlett_os.internal.gi import Gio, GLib, GObject, gi
from scarlett_os.utility import gnome  # Module with the decorator we need to replace


# source: https://github.com/YosaiProject/yosai/blob/master/test/isolated_tests/core/conf/conftest.py
@pytest.fixture(scope="function")
def tasker_unit_mocker_stopall(mocker):
    "Stop previous mocks, yield mocker plugin obj, then stopall mocks again"
    print("Called [setup]: mocker.stopall()")
    mocker.stopall()
    print("Called [setup]: imp.reload(tasker)")
    imp.reload(tasker)
    yield mocker
    print("Called [teardown]: mocker.stopall()")
    mocker.stopall()
    print("Called [setup]: imp.reload(tasker)")
    imp.reload(tasker)


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
class TestScarlettTasker(object):
    def test_tasker_init(self, tasker_unit_mocker_stopall):
        "Replace job of old setUp function in unittest"
        temp_mocker = tasker_unit_mocker_stopall
        #####################################################################################################################
        # TODO: Turn this block into a fixture
        #####################################################################################################################
        temp_mocker.patch("scarlett_os.utility.gnome.abort_on_exception", lambda x: x)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.gi", spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.GLib", spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.GObject", spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.Gio", spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("pydbus.SessionBus", spec=True, create=True)
        #####################################################################################################################

        temp_mocker.patch(
            "scarlett_os.utility.dbus_runner.DBusRunner",
            autospec=True,
            name="mock_dbusrunner",
        )
        temp_mocker.patch(
            "scarlett_os.tasker.TaskSignalHandler",
            spec=scarlett_os.tasker.TaskSignalHandler,
            name="mock_task_signal_handler",
        )
        temp_mocker.patch("scarlett_os.tasker.time.sleep", name="mock_time_sleep")
        temp_mocker.patch(
            "scarlett_os.tasker.logging.Logger.debug", name="mock_logger_debug"
        )
        temp_mocker.patch("scarlett_os.tasker._IdleObject", name="mock_idle_obj")
        temp_mocker.patch(
            "scarlett_os.utility.thread.time_logger", name="mock_time_logger"
        )
        temp_mocker.patch("scarlett_os.tasker.speaker", name="mock_scarlett_speaker")
        temp_mocker.patch("scarlett_os.tasker.player", name="mock_scarlett_player")
        temp_mocker.patch("scarlett_os.tasker.commands", name="mock_scarlett_commands")
        temp_mocker.patch(
            "scarlett_os.tasker.threading.RLock",
            spec=scarlett_os.tasker.threading.RLock,
            name="mock_threading_rlock",
        )
        temp_mocker.patch(
            "scarlett_os.tasker.threading.Event",
            spec=scarlett_os.tasker.threading.Event,
            name="mock_threading_event",
        )
        temp_mocker.patch(
            "scarlett_os.tasker.threading.Thread",
            spec=scarlett_os.tasker.threading.Thread,
            name="mock_thread_class",
        )

        tskr = tasker.ScarlettTasker()

    def test_tasker_reset(self, tasker_unit_mocker_stopall):
        temp_mocker = tasker_unit_mocker_stopall
        #####################################################################################################################
        # TODO: Turn this block into a fixture
        #####################################################################################################################
        temp_mocker.patch("scarlett_os.utility.gnome.abort_on_exception", lambda x: x)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.gi", spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.GLib", spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.GObject", spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.Gio", spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("pydbus.SessionBus", spec=True, create=True)
        #####################################################################################################################

        mock_dbusrunner = temp_mocker.patch(
            "scarlett_os.utility.dbus_runner.DBusRunner",
            autospec=True,
            name="mock_dbusrunner",
        )
        mock_task_signal_handler = temp_mocker.patch(
            "scarlett_os.tasker.TaskSignalHandler",
            spec=scarlett_os.tasker.TaskSignalHandler,
            name="mock_task_signal_handler",
        )
        temp_mocker.patch("scarlett_os.tasker.time.sleep", name="mock_time_sleep")
        temp_mocker.patch(
            "scarlett_os.tasker.logging.Logger.debug", name="mock_logger_debug"
        )
        temp_mocker.patch("scarlett_os.tasker._IdleObject", name="mock_idle_obj")
        temp_mocker.patch(
            "scarlett_os.utility.thread.time_logger", name="mock_time_logger"
        )
        temp_mocker.patch("scarlett_os.tasker.speaker", name="mock_scarlett_speaker")
        temp_mocker.patch("scarlett_os.tasker.player", name="mock_scarlett_player")
        temp_mocker.patch("scarlett_os.tasker.commands", name="mock_scarlett_commands")
        temp_mocker.patch(
            "scarlett_os.tasker.threading.RLock",
            spec=scarlett_os.tasker.threading.RLock,
            name="mock_threading_rlock",
        )
        temp_mocker.patch(
            "scarlett_os.tasker.threading.Event",
            spec=scarlett_os.tasker.threading.Event,
            name="mock_threading_event",
        )
        temp_mocker.patch(
            "scarlett_os.tasker.threading.Thread",
            spec=scarlett_os.tasker.threading.Thread,
            name="mock_thread_class",
        )

        # dbus mocks
        _dr = mock_dbusrunner.get_instance()
        bus = _dr.get_session_bus()

        # handler mocks
        _handler = mock_task_signal_handler()
        tskr = tasker.ScarlettTasker()

        tskr.reset()

        assert _handler.clear.call_count == 1
        assert tskr._failed_signal_callback is None
        assert tskr._ready_signal_callback is None
        assert tskr._keyword_recognized_signal_callback is None
        assert tskr._command_recognized_signal_callback is None
        assert tskr._cancel_signal_callback is None
        assert tskr._connect_signal_callback is None

    def test_tasker_prepare(self, tasker_unit_mocker_stopall):
        temp_mocker = tasker_unit_mocker_stopall
        #####################################################################################################################
        # TODO: Turn this block into a fixture
        #####################################################################################################################
        temp_mocker.patch("scarlett_os.utility.gnome.abort_on_exception", lambda x: x)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.gi", spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.GLib", spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.GObject", spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.Gio", spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("pydbus.SessionBus", spec=True, create=True)
        #####################################################################################################################

        mock_dbusrunner = temp_mocker.patch(
            "scarlett_os.utility.dbus_runner.DBusRunner",
            autospec=True,
            name="mock_dbusrunner",
        )
        mock_task_signal_handler = temp_mocker.patch(
            "scarlett_os.tasker.TaskSignalHandler",
            spec=scarlett_os.tasker.TaskSignalHandler,
            name="mock_task_signal_handler",
        )
        temp_mocker.patch("scarlett_os.tasker.time.sleep", name="mock_time_sleep")
        temp_mocker.patch(
            "scarlett_os.tasker.logging.Logger.debug", name="mock_logger_debug"
        )
        temp_mocker.patch("scarlett_os.tasker._IdleObject", name="mock_idle_obj")
        temp_mocker.patch(
            "scarlett_os.utility.thread.time_logger", name="mock_time_logger"
        )
        temp_mocker.patch("scarlett_os.tasker.speaker", name="mock_scarlett_speaker")
        temp_mocker.patch("scarlett_os.tasker.player", name="mock_scarlett_player")
        temp_mocker.patch("scarlett_os.tasker.commands", name="mock_scarlett_commands")
        temp_mocker.patch(
            "scarlett_os.tasker.threading.RLock",
            spec=scarlett_os.tasker.threading.RLock,
            name="mock_threading_rlock",
        )
        temp_mocker.patch(
            "scarlett_os.tasker.threading.Event",
            spec=scarlett_os.tasker.threading.Event,
            name="mock_threading_event",
        )
        temp_mocker.patch(
            "scarlett_os.tasker.threading.Thread",
            spec=scarlett_os.tasker.threading.Thread,
            name="mock_thread_class",
        )

        # dbus mocks
        _dr = mock_dbusrunner.get_instance()
        bus = _dr.get_session_bus()

        # handler mocks
        _handler = mock_task_signal_handler()
        tskr = tasker.ScarlettTasker()

        def on_signal_recieved(*args, **kwargs):
            print("on_signal_recieved")

        def connected_to_listener_cb(*args, **kwargs):
            print("connected_to_listener_cb")

        tskr.prepare(on_signal_recieved, on_signal_recieved, on_signal_recieved)

        assert _handler.clear.call_count == 1
        assert tskr._failed_signal_callback is not None
        assert tskr._ready_signal_callback is not None
        assert tskr._keyword_recognized_signal_callback is not None
        assert tskr._command_recognized_signal_callback is not None
        assert tskr._cancel_signal_callback is not None
        assert tskr._connect_signal_callback is not None


@pytest.mark.unittest
class TestSoundType(object):
    def test_soundtype_get_path(self):
        path_to_sound = "/home/pi/dev/bossjones-github/scarlett_os/scarlett_os/data/sounds"
        assert tasker.STATIC_SOUNDS_PATH == path_to_sound
        assert type(tasker.SoundType.get_path("pi-cancel")) == list
        assert tasker.SoundType.get_path("pi-cancel") == [
            "{}/pi-cancel.wav".format(path_to_sound)
        ]
        assert tasker.SoundType.get_path("pi-listening") == [
            "{}/pi-listening.wav".format(path_to_sound)
        ]
        assert tasker.SoundType.get_path("pi-response") == [
            "{}/pi-response.wav".format(path_to_sound)
        ]
        assert tasker.SoundType.get_path("pi-response2") == [
            "{}/pi-response2.wav".format(path_to_sound)
        ]


@pytest.mark.unittest
class TestTaskSignalHandler(object):
    def test_connect_then_disconnect(self, tasker_unit_mocker_stopall):
        temp_mocker = tasker_unit_mocker_stopall
        ###################################################################################################################
        _handler = tasker.TaskSignalHandler()
        _old_glib_exception_error = GLib.GError
        # Now patch the decorator where the decorator is being imported from
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.utility.gnome.abort_on_exception", lambda x: x)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.gi", spec=True, create=True)

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.GLib", spec=True, create=True)

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.GObject", spec=True, create=True)

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.Gio", spec=True, create=True)

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("pydbus.SessionBus", spec=True, create=True)
        ###################################################################################################################
        mock_dbusrunner = temp_mocker.patch(
            "scarlett_os.utility.dbus_runner.DBusRunner",
            autospec=True,
            name="mock_dbusrunner",
        )

        _dr = mock_dbusrunner.get_instance()
        bus = _dr.get_session_bus()

        def test_cb():
            print("test_cb")

        _handler.connect(bus, "SttFailedSignal", test_cb)

        # assertions
        assert len(_handler._ids) == 1

        bus.subscribe.assert_called_once_with(
            sender=None,
            iface="org.scarlett.Listener",
            signal="SttFailedSignal",
            object="/org/scarlett/Listener",
            arg0=None,
            flags=0,
            signal_fired=test_cb,
        )

        # Disconnect then test again
        _handler.disconnect(bus, "SttFailedSignal")

        assert len(_handler._ids) == 0

    def test_connect_then_clear(self, tasker_unit_mocker_stopall):
        temp_mocker = tasker_unit_mocker_stopall
        ###################################################################################################################
        _handler = tasker.TaskSignalHandler()
        # Now patch the decorator where the decorator is being imported from
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.utility.gnome.abort_on_exception", lambda x: x)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.gi", spec=True, create=True)

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.GLib", spec=True, create=True)

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.GObject", spec=True, create=True)

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("scarlett_os.internal.gi.Gio", spec=True, create=True)

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch("pydbus.SessionBus", spec=True, create=True)
        ###################################################################################################################
        mock_dbusrunner = temp_mocker.patch(
            "scarlett_os.utility.dbus_runner.DBusRunner",
            autospec=True,
            name="mock_dbusrunner",
        )

        _dr = mock_dbusrunner.get_instance()
        bus = _dr.get_session_bus()

        def test_cb():
            print("test_cb")

        _handler.connect(bus, "SttFailedSignal", test_cb)

        # Disconnect then test again
        _handler.clear()

        assert len(_handler._ids) == 0


@pytest.mark.unittest
class TestSpeakerType(object):
    def test_speakertype_speaker_to_array(self):
        assert type(tasker.SpeakerType.speaker_to_array("It is now, 05:34 PM")) == list
        assert tasker.SpeakerType.speaker_to_array("It is now, 05:34 PM") == [
            "It is now, 05:34 PM"
        ]
