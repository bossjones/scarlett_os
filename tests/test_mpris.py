#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_mpris
----------------------------------
"""

import os
import sys
import unittest

from scarlett_os.internal.gi import GLib
from scarlett_os.internal.gi import Gio
from scarlett_os.internal.gi import GObject

from pydbus import SessionBus
from scarlett_os.mpris import ScarlettListener

bus = SessionBus()
bus.own_name(name='org.scarlett')


DBUS_SESSION_BUS_ADDRESS = os.getenv("DBUS_SESSION_BUS_ADDRESS")


class TestScarlettListener(unittest.TestCase):

    def setUp(self):
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """
        self.sl = ScarlettListener(bus=bus.con, path='/org/scarlett/Listener')

    def test_scarlett_listener_interfaces(self):
        self.assertEqual(self.sl.__repr__(), '<ScarlettListener(org.scarlett, /org/scarlett/Listener)>')
        self.assertEqual(self.sl.LISTENER_IFACE, 'org.scarlett.Listener')
        self.assertEqual(self.sl.LISTENER_PLAYER_IFACE, 'org.scarlett.Listener.Player')
        self.assertEqual(self.sl.LISTENER_TRACKLIST_IFACE, 'org.scarlett.Listener.TrackList')
        self.assertEqual(self.sl.LISTENER_PLAYLISTS_IFACE, 'org.scarlett.Listener.Playlists')
        self.assertEqual(self.sl.LISTENER_EVENTS_IFACE, 'org.scarlett.Listener.event')
        self.assertTrue(isinstance(self.sl.bus_conn, Gio.DBusConnection))
        self.assertEqual(self.sl.path, '/org/scarlett/Listener')

        # NOTE: these are all private. We need a getter function
        # self.assertTrue(type(self.sl.dbus_stack), list)
        # self.assertEqual(self.sl._message, 'This is the DBusServer')
        # self.assertEqual(self.sl._status_ready, '  ScarlettListener is ready')
        # self.assertEqual(self.sl._status_kw_match, "  ScarlettListener caught a keyword match")
        # self.assertEqual(self.sl._status_cmd_match, "  ScarlettListener caught a command match")
        # self.assertEqual(self.sl._status_stt_failed, "  ScarlettListener hit Max STT failures")
        # self.assertEqual(self.sl._status_cmd_start, "  ScarlettListener emitting start command")
        # self.assertEqual(self.sl._status_cmd_fin, "  ScarlettListener Emitting Command run finish")
        # self.assertEqual(self.sl._status_cmd_cancel, "  ScarlettListener cancel speech Recognition")

    def test_scarlett_listener_emit_methods(self):
        self.assertEqual(self.sl.emitKeywordRecognizedSignal(), 'pi-listening')
        self.assertEqual(self.sl.emitCommandRecognizedSignal('what time is it'), 'pi-response')
        self.assertEqual(self.sl.emitSttFailedSignal(), 'pi-response2')  # SCARLETT_FAILED
        self.assertEqual(self.sl.emitListenerCancelSignal(), 'pi-cancel')  # SCARLETT_CANCEL
        self.assertEqual(self.sl.emitListenerReadySignal(), 'pi-listening')  # SCARLETT_LISTENING
        self.assertEqual(self.sl.emitConnectedToListener('fake_plugin'), ' fake_plugin is connected to ScarlettListener')
        self.assertEqual(self.sl.emitListenerMessage(), 'This is the DBusServer')
