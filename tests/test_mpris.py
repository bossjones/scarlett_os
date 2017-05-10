#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_mpris
----------------------------------
"""

import os
import sys
import time
import pytest
import threading

from scarlett_os.internal.gi import GLib
from scarlett_os.internal.gi import Gio
from scarlett_os.internal.gi import GObject

DBUS_SESSION_BUS_ADDRESS = os.getenv("DBUS_SESSION_BUS_ADDRESS")

RUN_TIMEOUT = 5

# from pydbus import SessionBus
# bus = SessionBus()
# # TODO: own_name() is deprecated, use request_name() instead.
# bus.own_name(name='org.scarlett')
# sl = ScarlettListener(bus=bus.con, path='/org/scarlett/Listener')
# loop.run()

# def sigint_handler(*args):
#     """Exit on Ctrl+C"""

#     # Unregister handler, next Ctrl-C will kill app
#     # TODO: figure out if this is really needed or not
#     signal.signal(signal.SIGINT, signal.SIG_DFL)

#     sl.Quit()

# signal.signal(signal.SIGINT, sigint_handler)


@pytest.fixture(scope='function')
def main_loop():
    loop = GLib.MainLoop()
    timeout = GLib.Timeout(RUN_TIMEOUT)
    timeout.set_callback(lambda loop: loop.quit(), loop)
    timeout.attach()
    return loop


# https://github.com/Mirantis/ceph-lcm/blob/1b95e76503d9869da4bf4e91e24c848d3f683624/tests/controller/test_mainloop.py
# @pytest.fixture(scope='function')
# def main_loop_threading():
#     thread = threading.Thread(target=mainloop.main)
#     thread.start()
#
#     return thread
#
#
# def test_shutdown_callback(main_loop_threading):
#     time.sleep(.5)
#
#     assert main_loop_threading.is_alive()
#     mainloop.shutdown_callback()
#
#     time.sleep(.5)
#     assert not main_loop_threading.is_alive()


@pytest.fixture(scope='module')
def bus():
    from pydbus import SessionBus
    bus = SessionBus()
    time.sleep(.5)
    print('\n[initalize] pydbus.SessionBus ...')
    bus.own_name(name='org.scarlett')
    # bus.dbus
    time.sleep(.5)
    yield bus
    print('\n[teardown] pydbus.SessionBus ...')
    # del bus._dbus
    print("ran: del bus._dbus")
    del bus
    print("ran: del bus")


# from __main__
# from pydbus import SessionBus
# bus = SessionBus()
# # TODO: own_name() is deprecated, use request_name() instead.
# bus.own_name(name='org.scarlett')
# sl = ScarlettListener(bus=bus.con, path='/org/scarlett/Listener')
# loop.run()

@pytest.fixture(scope='module')
def sl(bus):
    # FIXME: 5/7/2017. I don't think we cleaned this guy up 100% correctly. Investigate.
    from scarlett_os.mpris import ScarlettListener
    sl = ScarlettListener(bus=bus.con, path='/org/scarlett/Listener')
    print('\n[initalize] scarlett_os.mpris.ScarlettListener ...')
    time.sleep(.5)
    yield sl
    print('\n[teardown] scarlett_os.mpris.ScarlettListener ...')
    del sl
    print("ran: del sl")


@pytest.mark.unittest
@pytest.mark.wonky
@pytest.mark.scarlettonly
@pytest.mark.scarlettonlyunittest
class TestScarlettListener(object):

    def test_scarlett_listener_interfaces(self, sl, main_loop):
        assert sl.__repr__() == '<ScarlettListener(org.scarlett, /org/scarlett/Listener)>'
        assert sl.LISTENER_IFACE == 'org.scarlett.Listener'
        assert sl.LISTENER_PLAYER_IFACE == 'org.scarlett.Listener.Player'
        assert sl.LISTENER_TRACKLIST_IFACE == 'org.scarlett.Listener.TrackList'
        assert sl.LISTENER_PLAYLISTS_IFACE == 'org.scarlett.Listener.Playlists'
        assert sl.LISTENER_EVENTS_IFACE == 'org.scarlett.Listener.event'
        assert isinstance(sl.bus_conn, Gio.DBusConnection)
        assert sl.path == '/org/scarlett/Listener'

    def test_scarlett_listener_emit_methods(self, sl, main_loop):
        assert hasattr(sl, 'emitKeywordRecognizedSignal')
        assert hasattr(sl, 'emitCommandRecognizedSignal')
        assert hasattr(sl, 'emitSttFailedSignal')
        assert hasattr(sl, 'emitListenerCancelSignal')
        assert hasattr(sl, 'emitListenerReadySignal')
        assert hasattr(sl, 'emitConnectedToListener')
        assert hasattr(sl, 'emitListenerMessage')

        # NOTE: These guys don't work because you don't have a real GLib mainloop running
        # assert sl.emitKeywordRecognizedSignal() == 'pi-listening'
        # assert sl.emitCommandRecognizedSignal('what time is it') == 'pi-response'
        # assert sl.emitSttFailedSignal() == 'pi-response2'  # SCARLETT_FAILED
        # assert sl.emitListenerCancelSignal() == 'pi-cancel'  # SCARLETT_CANCEL
        # assert sl.emitListenerReadySignal() == 'pi-listening'  # SCARLETT_LISTENING
        # assert sl.emitConnectedToListener('fake_plugin') == ' fake_plugin is connected to ScarlettListener'
        # assert sl.emitListenerMessage() == 'This is the DBusServer'
