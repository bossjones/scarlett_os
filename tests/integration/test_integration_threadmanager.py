#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_integration_listener
----------------------------------
"""

###########################################
# Borrowed from test_integration_player - START
###########################################
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

from tests.integration.baseclass import run_emitter_signal
from tests.integration.baseclass import IntegrationTestbaseMainloop

done = 0

from scarlett_os.internal import gi  # noqa
from scarlett_os.internal.gi import Gio  # noqa
from scarlett_os.internal.gi import GObject  # noqa
from scarlett_os.internal.gi import GLib

from scarlett_os.utility import threadmanager

to_complete = 2


@pytest.fixture
def tmanager(request):
    # create threadmanager
    tmanager = threadmanager.get_thread_manager(2)
    # yield it to calling function/test
    yield tmanager
    # when we get control again after test finishes, print this
    print('\n[teardown] test_ThreadManager, killing threadmanager ...')
    # then nuke object
    del tmanager


class TestThread(threadmanager.SuspendableThread):

    def do_run(self):
        for n in range(1000):
            time.sleep(0.01)
            self.emit('progress', n / 1000.0, '%s of 1000' % n)
            self.check_for_sleep()


class TestError(threadmanager.SuspendableThread):

    def do_run(self):
        for n in range(1000):
            time.sleep(0.01)
            if n == 100:
                raise AttributeError("This is a phony error")
            self.emit('progress', n / 1000.0, '%s of 1000' % n)
            self.check_for_sleep()


# run forever, we'll want this for listener thread in scarlett
class TestInterminable(threadmanager.SuspendableThread):

    def do_run(self):
        while 1:
            time.sleep(0.1)
            self.emit('progress', -1, 'Working interminably')
            self.check_for_sleep()


class TestThreadManager(object):

    def test_ThreadManager(self, monkeypatch, tmanager):
        tm = tmanager

        assert str(type(tm)) == "<class 'scarlett_os.utility.threadmanager.ThreadManager'>"

        assert tm.active_count == 0
        assert tm.completed_threads == 0
        assert tm.count == 0
        assert tm.max_concurrent_threads == 2
        assert tm.thread_queue == []
        assert tm.threads == []

        # for desc, thread in [
        #     ('Interminable 1', TestInterminable()),
        #     ('Linear 1', TestThread()),
        #     ('Linear 2', TestThread()),
        #     ('Interminable 2', TestInterminable()),
        #     ('Error 3', TestError())
        # ]:
        #     tm.add_thread(thread)
