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

from tests import PROJECT_ROOT
import time

done = 0

from scarlett_os.internal import gi  # noqa
from scarlett_os.internal.gi import Gio  # noqa
from scarlett_os.internal.gi import GObject  # noqa
from scarlett_os.internal.gi import GLib


class TestScarlettEndToEnd(object):

    def test_setup_mpris(self, service_on_outside):
        pass

    @pytest.mark.flaky(reruns=3)
    def test_mpris_player_and_tasker(self, service_on_outside, service_tasker, service_receiver, get_environment, get_bus):

        # Return dbus obj
        bus = get_bus

        # Sleep to give time for connection to be established
        time.sleep(1)

        # Return dbus proxy object
        ss = bus.get("org.scarlett", object_path='/org/scarlett/Listener')

        # wait till we get proxy object
        time.sleep(0.5)

        # Catch tuples find from dbus signal
        self.recieved_signals = []

        # Return return code for running shell out command
        def cb(pid, status):
            """
            Set return code for emitter shell script.
            """
            self.status = status

        # Append tuple to recieved_signals
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler.
            Catch and print information about all singals.
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

            self.recieved_signals.append(v)

            print('--- [args] ---')
            for arg in args:
                print("another arg through *arg : {}".format(arg))

            print('--- [kargs] ---')
            if kwargs is not None:
                for key, value in kwargs.items():
                    print("{} = {}".format(key, value))

            print("\n")

            # Run Mainloop
            # 1. Run: [spawn_async]
            # 2. Run: [dbus ]
            loop.quit()

        # import pdb;pdb.set_trace()

        # The only main loop supported by pydbus is GLib.MainLoop.
        self.status = None

        # MainLoop
        loop = GLib.MainLoop()

        print("Running main gui loop in thread: {}".format(threading.current_thread()))
        print("Are we in main thread?: {}".format(threading.main_thread()))

        ss_rdy_signal = bus.subscribe(sender=None,
                                      iface="org.scarlett.Listener",
                                      signal="ListenerReadySignal",
                                      object="/org/scarlett/Listener",
                                      arg0=None,
                                      flags=0,
                                      signal_fired=catchall_handler)

        print('[ss_rdy_signal] - created')

        # Give it a second
        time.sleep(0.5)

        # Send [ready] signal to dbus service
        # FIXME: THIS IS THE CULPRIT
        argv = [sys.executable, '-m', 'scarlett_os.emitter', '-s', 'ready']

        # convert environment dict -> list of strings
        env_dict_to_str = ['{}={}'.format(k, v) for k, v in get_environment.items()]

        # Async background call. Send a signal to running process.
        pid, stdin, stdout, stderr = GLib.spawn_async(
            argv,
            envp=env_dict_to_str,
            working_directory=PROJECT_ROOT,
            flags=GLib.SpawnFlags.DO_NOT_REAP_CHILD)

        # Close file descriptor when finished running scarlett emitter
        pid.close()

        # NOTE: We give this PRIORITY_HIGH to ensure callback [cb] runs before dbus signal callback
        id = GLib.child_watch_add(GLib.PRIORITY_HIGH, pid, cb)

        # assert 0 is basically a break point which will allow you to step through your code in pytest when --pdb is provided.

        # source: http://stackoverflow.com/questions/2678792/can-i-debug-with-python-debugger-when-using-py-test-somehow

        # Taken from pygobject test
        assert loop.get_context().find_source_by_id(id).priority == GLib.PRIORITY_HIGH

        # More sleeps
        time.sleep(1)

        # import pdb;pdb.set_trace()

        # Kick off mainloop
        loop.run()

        # TEST: Verify that shell return code is 0
        assert self.status == 0

        # TEST: Assert we got READY signal
        assert self.recieved_signals[0] == ('  ScarlettListener is ready', 'pi-listening')

        # Disconnect dbus signal
        ss_rdy_signal.disconnect()
