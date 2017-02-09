#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Contains the Base class for integration tests using the classic xunit-style setup.
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

# from tests.integration.stubs import create_main_loop

from tests import PROJECT_ROOT
import time

import logging

done = 0

from scarlett_os.internal import gi  # noqa
from scarlett_os.internal.gi import Gio  # noqa
from scarlett_os.internal.gi import GObject  # noqa
from scarlett_os.internal.gi import GLib

from scarlett_os import tasker
# classic xunit-style setup
# source: http://doc.pytest.org/en/latest/xunit_setup.html

# from scarlett_os.utility.dbus_runner import DBusRunner


def run_emitter_signal(request, get_environment, sig_name='ready'):
    print("Setting up emitter")
    print("[Emit]: {}".format(sig_name))

    # Return return code for running shell out command
    def cb(pid, status):
        """
        Set return code for emitter shell script.
        """
        print('status code: {}'.format(status))

    # Send [ready] signal to dbus service
    # FIXME: THIS IS THE CULPRIT
    argv = [sys.executable, '-m', 'scarlett_os.emitter', '-s', sig_name]

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


@pytest.mark.usefixtures("service_on_outside", "get_environment", "get_bus")
class IntegrationTestbase(object):
    """Base class for integration tests."""
    # Tests are not allowed to have an __init__ method
    # Python shells, the underscore (_) means the result of the last evaluated expression in the shell:
    # source: http://stackoverflow.com/questions/5787277/python-underscore-as-a-function-parameter
    # [Method and function level setup/teardown]
    def setup_method(self, _):
        """Set up called automatically before every test_XXXX method."""
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)
        logging.basicConfig(
            format="%(filename)s:%(lineno)d (%(funcName)s): %(message)s")

        self.recieved_signals = []
        self.status = None
        self.tasker = None

    def setup_tasker(self, monkeypatch, get_bus):
        """Create ScarlettTasker object and call setup_controller."""
        monkeypatch.setattr("scarlett_os.utility.dbus_runner.SessionBus", lambda: get_bus)
        time.sleep(1)
        self.log.info("setting up Controller")
        self.tasker = tasker.ScarlettTasker()

    def setup_mpris(self, service_on_outside):
        self.log.info("Setting up mpris dbus server")

    def teardown_method(self, _):
        """Tear down called automatically after every test_XXXX method."""
        self.recieved_signals = []
        self.status = None
        self.tasker = None


# @pytest.mark.usefixtures("service_on_outside", "get_environment", "get_bus")
class IntegrationTestbaseMainloop(IntegrationTestbase):
    """Base class for integration tests that require a GLib-Mainloop.
    Used for Tests that register and wait for signals.
    """

    # Method and function level setup/teardown
    def setup_method(self, method):
        """Set up called automatically before every test_XXXX method."""
        super(IntegrationTestbaseMainloop, self).setup_method(method)
        self.mainloop = GLib.MainLoop()
        self.quit_count = 0

    def run_mainloop(self, timeout=5):
        """Start the MainLoop, set Quit-Counter to Zero"""
        self.quit_count = 0
        GLib.timeout_add_seconds(timeout, self.quit_mainloop)
        self.mainloop.run()

    def quit_mainloop(self, *_):
        """Quit the MainLoop, set Quit-Counter to Zero"""
        self.mainloop.quit()
        self.quit_count = 0

    def quit_mainloop_after(self, call_count):
        """Increment Quit-Counter, if it reaches call_count,
        Quit the MainLoop"""
        self.quit_count += 1
        if self.quit_count == call_count:
            self.quit_mainloop()
