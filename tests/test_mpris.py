#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_mpris
----------------------------------
"""

import os
import sys
import pytest
# import unittest

from scarlett_os.internal.gi import GLib
from scarlett_os.internal.gi import Gio
from scarlett_os.internal.gi import GObject

DBUS_SESSION_BUS_ADDRESS = os.getenv("DBUS_SESSION_BUS_ADDRESS")

@pytest.fixture(scope='module')
def bus():
    from pydbus import SessionBus
    bus = SessionBus()
    print('\n[initalize] pydbus.SessionBus ...')
    bus.own_name(name='org.scarlett')
    bus.dbus
    yield bus
    print('\n[teardown] pydbus.SessionBus ...')
    del bus._dbus
    print("ran: del bus._dbus")
    del bus
    print("ran: del bus")

@pytest.fixture(scope='module')
@pytest.mark.unittest
# @pytest.mark.unittest
def sl(bus):
    from scarlett_os.mpris import ScarlettListener
    sl = ScarlettListener(bus=bus.con, path='/org/scarlett/Listener')
    print('\n[initalize] scarlett_os.mpris.ScarlettListener ...')
    yield sl
    print('\n[teardown] scarlett_os.mpris.ScarlettListener ...')
    del sl
    print("ran: del sl")


class TestScarlettListener(object):

    # def setUp(self):
    #     """
    #     Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
    #     """
    #     self.sl = ScarlettListener(bus=bus.con, path='/org/scarlett/Listener')

    # NOTE: Added 1/4/2017
    # def tearDown(self):
    #     del self.sl

    def test_scarlett_listener_interfaces(self, sl):
        assert sl.__repr__() == '<ScarlettListener(org.scarlett, /org/scarlett/Listener)>'
        assert sl.LISTENER_IFACE == 'org.scarlett.Listener'
        assert sl.LISTENER_PLAYER_IFACE == 'org.scarlett.Listener.Player'
        assert sl.LISTENER_TRACKLIST_IFACE == 'org.scarlett.Listener.TrackList'
        assert sl.LISTENER_PLAYLISTS_IFACE == 'org.scarlett.Listener.Playlists'
        assert sl.LISTENER_EVENTS_IFACE == 'org.scarlett.Listener.event'
        assert isinstance(sl.bus_conn, Gio.DBusConnection)
        assert sl.path == '/org/scarlett/Listener'

        # NOTE: these are all private. We need a getter function
        # self.assertTrue(type(sl.dbus_stack), list)
        # self.assertEqual(sl._message, 'This is the DBusServer')
        # self.assertEqual(sl._status_ready, '  ScarlettListener is ready')
        # self.assertEqual(sl._status_kw_match, "  ScarlettListener caught a keyword match")
        # self.assertEqual(sl._status_cmd_match, "  ScarlettListener caught a command match")
        # self.assertEqual(sl._status_stt_failed, "  ScarlettListener hit Max STT failures")
        # self.assertEqual(sl._status_cmd_start, "  ScarlettListener emitting start command")
        # self.assertEqual(sl._status_cmd_fin, "  ScarlettListener Emitting Command run finish")
        # self.assertEqual(sl._status_cmd_cancel, "  ScarlettListener cancel speech Recognition")

    def test_scarlett_listener_emit_methods(self):
        assert sl.emitKeywordRecognizedSignal() == 'pi-listening'
        assert sl.emitCommandRecognizedSignal('what time is it') == 'pi-response'
        assert sl.emitSttFailedSignal() == 'pi-response2'  # SCARLETT_FAILED
        assert sl.emitListenerCancelSignal() == 'pi-cancel'  # SCARLETT_CANCEL
        assert sl.emitListenerReadySignal() == 'pi-listening'  # SCARLETT_LISTENING
        assert sl.emitConnectedToListener('fake_plugin') == ' fake_plugin is connected to ScarlettListener'
        assert sl.emitListenerMessage() == 'This is the DBusServer'
