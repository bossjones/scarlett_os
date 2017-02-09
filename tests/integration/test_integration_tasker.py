#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_integration_mpris
----------------------------------
"""

import os
import sys
import signal
import pytest
import builtins
import threading

import unittest
import unittest.mock as mock

import pydbus
import scarlett_os
import scarlett_os.exceptions

from tests.integration.stubs import create_main_loop

from tests import PROJECT_ROOT
import time

from tests.integration.baseclass import IntegrationTestbaseMainloop

done = 0

from scarlett_os.internal import gi  # noqa
from scarlett_os.internal.gi import Gio  # noqa
from scarlett_os.internal.gi import GObject  # noqa
from scarlett_os.internal.gi import GLib

from scarlett_os import tasker


# @pytest.fixture
# def create_tasker_object(request):
#     # source: dbus-proxy
#     """
#     Create a Scarlett Tasker Object
#
#     """
#
#     tskr = tasker.ScarlettTasker()
#
#     def teardown():
#         tskr.clear()
#
#     # The finalizer is called after all of the tests that use the fixture.
#     # If you’ve used parameterized fixtures,
#     # the finalizer is called between instances of the parameterized fixture changes.
#     request.addfinalizer(teardown)
#
#     return tskr
#
#
# class MockTaskerTest:
#     def __init__(self, create_tasker_object):
#         self.recieved_signals = []
#         self.status = None
#         self.tasker = create_tasker_object
#         self.loop = GLib.MainLoop()
#
#         # Return return code for running shell out command
#         def cb(pid, status):
#             """
#             Set return code for emitter shell script.
#             """
#             self.status = status
#
#         # Append tuple to recieved_signals
#         def catchall_handler(*args, **kwargs):  # pragma: no cover
#             """
#             Catch all handler.
#             Catch and print information about all singals.
#             """
#             # unpack tuple to variables ( Taken from Tasker )
#             for i, v in enumerate(args):
#                 if isinstance(v, tuple):
#                     tuple_args = len(v)
#                     if tuple_args == 1:
#                         msg = v
#                     elif tuple_args == 2:
#                         msg, scarlett_sound = v
#                     elif tuple_args == 3:
#                         msg, scarlett_sound, command = v
#
#             self.recieved_signals.append(v)
#
#             print('--- [args] ---')
#             for arg in args:
#                 print("another arg through *arg : {}".format(arg))
#
#             print('--- [kargs] ---')
#             if kwargs is not None:
#                 for key, value in kwargs.items():
#                     print("{} = {}".format(key, value))
#
#             print("\n")
#
#             self.loop.quit()
#
#         self.tasker.prepare(catchall_handler, catchall_handler, catchall_handler)
#         self.tasker.configure()
#
#
# class TestScarlettTasker(object):
#
#     def test_ScarlettTasker_reset(self, service_on_outside, get_environment):
#
#         def player_cb(*args, **kwargs):
#             print('player_cb')
#
#         def command_cb(*args, **kwargs):
#             print('command_cb')
#
#         def connected_to_listener_cb(*args, **kwargs):
#             print('connected_to_listener_cb')
#
#         tskr = tasker.ScarlettTasker()
#
#         tskr.prepare(player_cb, command_cb, connected_to_listener_cb)
#         tskr.configure()
#
#         # MainLoop
#         loop = GLib.MainLoop()
#
#         ###############################################################################################################
#         # Send [ready] signal to dbus service
#         # FIXME: THIS IS THE CULPRIT
#         argv = [sys.executable, '-m', 'scarlett_os.emitter', '-s', 'ready']
#
#         # convert environment dict -> list of strings
#         env_dict_to_str = ['{}={}'.format(k, v) for k, v in get_environment.items()]
#
#         # Async background call. Send a signal to running process.
#         pid, stdin, stdout, stderr = GLib.spawn_async(
#             argv,
#             envp=env_dict_to_str,
#             working_directory=PROJECT_ROOT,
#             flags=GLib.SpawnFlags.DO_NOT_REAP_CHILD)
#
#         # Close file descriptor when finished running scarlett emitter
#         pid.close()
#
#         # NOTE: We give this PRIORITY_HIGH to ensure callback [cb] runs before dbus signal callback
#         id = GLib.child_watch_add(GLib.PRIORITY_HIGH, pid, cb)
#
#         # assert 0 is basically a break point which will allow you to step through your code in pytest when --pdb is provided.
#
#         # source: http://stackoverflow.com/questions/2678792/can-i-debug-with-python-debugger-when-using-py-test-somehow
#
#         # Taken from pygobject test
#         assert loop.get_context().find_source_by_id(id).priority == GLib.PRIORITY_HIGH
#
#         # More sleeps
#         time.sleep(1)
#
#         ###############################################################################################################
#
#         # Kick off mainloop
#         loop.run()
#
#         assert tskr._failed_signal_callback == player_cb
#         assert tskr._ready_signal_callback == player_cb
#         assert tskr._keyword_recognized_signal_callback == player_cb
#         assert tskr._command_recognized_signal_callback == command_cb
#         assert tskr._cancel_signal_callback == player_cb
#         assert tskr._connect_signal_callback == connected_to_listener_cb


class TestScarlettTasker(IntegrationTestbaseMainloop):
    """Test Tasker Signals for various on_* signal-handler methods
    """

    def test_initial_mode_callback(self, request, get_environment, monkeypatch, get_bus, run_emitter_signal):
        """Create a Controller object, call on_new_mode_online method and
        check that the callback fires initially when the sources are set up
        """
        # Append tuple to recieved_signals
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler. Catch and print information about all singals.
            """
            # unpack tuple to variables ( Taken from Tasker )
            for i, v in enumerate(args):
                if isinstance(v, tuple):
                    tuple_args = len(v)
                    if tuple_args == 1:
                        msg = v
                    elif tuple_args == 2:
                        msg, scarlett_sound = v
                    elif tuple_args == 3:
                        msg, scarlett_sound, command = v

            # Add value to list so we can assert later
            self.recieved_signals.append(v)

        self.setup_tasker(monkeypatch, get_bus)

        self.log.info("setting callback")
        # test_cb = mock.Mock(side_effect=self.quit_mainloop)

        self.tasker.prepare(catchall_handler, catchall_handler, catchall_handler)
        self.tasker.configure()
        # self.controller.on_new_mode_online(test_cb)

        # self.log.info("starting test-sources")
        # self.setup_video_sources(count=2)
        run_emitter_signal(request, get_environment)

        self.log.info("waiting for initial callback with"
                      "('  ScarlettListener is ready', 'pi-listening')")
        self.run_mainloop(timeout=5)
        # test_cb.assert_called_once_with(Controller.COMPOSITE_DUAL_EQUAL)

        assert self.recieved_signals[0] == ('  ScarlettListener is ready', 'pi-listening')
