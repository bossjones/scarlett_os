#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dbus_utils
----------------------------------
"""

import pytest
import unittest
import unittest.mock as mock
from scarlett_os.utility import dbus_utils

import pydbus
from pydbus import SessionBus
import imp  # Library to help us reload our tasker module

# FIXME: Convert to pytest
# FIXME: 5/10/2017
class TestDbusSignalHandler(unittest.TestCase):

    def setUp(self):  # noqa: N802
        """
        TestDbusSignalHandler
        """
        self._handler = dbus_utils.DbusSignalHandler()

        def kill_patches():  # Create a cleanup callback that undoes our patches
            mock.patch.stopall()  # Stops all patches started with start()
            imp.reload(dbus_utils)  # Reload our UUT module which restores the original decorator
        self.addCleanup(kill_patches)  # We want to make sure this is run so we do this in addCleanup instead of tearDown

        imp.reload(dbus_utils)  # Reloads the tasker.py module which applies our patched decorator

    def tearDown(self):
        del(self._handler)
        self._handler = None

    @mock.patch('scarlett_os.utility.dbus_runner.DBusRunner', autospec=True, name='mock_dbusrunner')
    def test_connect_then_disconnect(self, mock_dbusrunner):
        _dr = mock_dbusrunner.get_instance()
        bus = _dr.get_session_bus()

        def test_cb():
            print('test_cb')

        self._handler.connect(bus, "SttFailedSignal", test_cb)

        # assertions
        self.assertEqual(len(self._handler._ids), 1)

        bus.subscribe.assert_called_once_with(sender=None,
                                              iface="org.scarlett.Listener",
                                              signal="SttFailedSignal",
                                              object="/org/scarlett/Listener",
                                              arg0=None,
                                              flags=0,
                                              signal_fired=test_cb)

        # Disconnect then test again
        self._handler.disconnect(bus, "SttFailedSignal")

        self.assertEqual(len(self._handler._ids), 0)

    @mock.patch('scarlett_os.utility.dbus_runner.DBusRunner', autospec=True, name='mock_dbusrunner')
    def test_connect_then_clear(self, mock_dbusrunner):
        _dr = mock_dbusrunner.get_instance()
        bus = _dr.get_session_bus()

        def test_cb():
            print('test_cb')

        self._handler.connect(bus, "SttFailedSignal", test_cb)

        # Disconnect then test again
        self._handler.clear()

        self.assertEqual(len(self._handler._ids), 0)
