#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dbus_utils
----------------------------------
"""

import imp  # Library to help us reload our tasker module
import unittest
import unittest.mock as mock

import pydbus
from pydbus import SessionBus
import pytest

import scarlett_os
from scarlett_os.utility import dbus_utils


@pytest.fixture(scope="function")
def dbus_utils_mocker_stopall(mocker):
    "Stop previous mocks, yield mocker plugin obj, then stopall mocks again"
    print("Called [setup]: mocker.stopall()")
    mocker.stopall()
    print("Called [setup]: imp.reload(dbus_utils)")
    imp.reload(dbus_utils)
    yield mocker
    print("Called [teardown]: mocker.stopall()")
    mocker.stopall()
    print("Called [setup]: imp.reload(dbus_utils)")
    imp.reload(dbus_utils)


class TestDbusSignalHandler(object):
    def test_connect_then_disconnect(self, dbus_utils_mocker_stopall):
        mock_dbusrunner = dbus_utils_mocker_stopall.MagicMock(
            name="mock_dbusrunner", spec=scarlett_os.utility.dbus_runner.DBusRunner
        )
        dbus_utils_mocker_stopall.patch.object(
            scarlett_os.utility.dbus_runner, "DBusRunner", mock_dbusrunner
        )

        # create handler
        _handler = dbus_utils.DbusSignalHandler()

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

        # tear down
        del (_handler)
        _handler = None

    def test_connect_then_clear(self, dbus_utils_mocker_stopall):
        mock_dbusrunner = dbus_utils_mocker_stopall.MagicMock(
            name="mock_dbusrunner", spec=scarlett_os.utility.dbus_runner.DBusRunner
        )
        dbus_utils_mocker_stopall.patch.object(
            scarlett_os.utility.dbus_runner, "DBusRunner", mock_dbusrunner
        )

        # create handler
        _handler = dbus_utils.DbusSignalHandler()

        _dr = mock_dbusrunner.get_instance()
        bus = _dr.get_session_bus()

        def test_cb():
            print("test_cb")

        _handler.connect(bus, "SttFailedSignal", test_cb)

        # Disconnect then test again
        _handler.clear()

        assert len(_handler._ids) == 0

        # tear down
        del (_handler)
        _handler = None
