#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_threadmanager
----------------------------------
"""

import os
import sys
import time

import pytest
import unittest
import unittest.mock as mock
from mock import call

import scarlett_os
from scarlett_os.utility import threadmanager
from scarlett_os.utility import gnome  # Module with the decorator we need to replace

from scarlett_os.internal.gi import gi
from scarlett_os.internal.gi import GLib
from scarlett_os.internal.gi import GObject
from scarlett_os.internal.gi import Gio
import pydbus
from pydbus import SessionBus

# NOTE: We can't add this here, otherwise we won't be able to mock them
# from tests import common
import signal
import builtins
import scarlett_os.exceptions

import imp


# source: https://github.com/YosaiProject/yosai/blob/master/test/isolated_tests/core/conf/conftest.py
@pytest.fixture(scope='function')
def threadmanager_unit_mocker_stopall(mocker):
    "Stop previous mocks, yield mocker plugin obj, then stopall mocks again"
    print('Called [setup]: mocker.stopall()')
    mocker.stopall()
    print('Called [setup]: imp.reload(threadmanager)')
    imp.reload(threadmanager)
    yield mocker
    print('Called [teardown]: mocker.stopall()')
    mocker.stopall()
    print('Called [setup]: imp.reload(threadmanager)')
    imp.reload(threadmanager)


class MockSuspendableThreadButNotThreadSafeUnit(threadmanager.SuspendableThread, threadmanager.NotThreadSafe):  # pylint: disable=C0111

    def __init__(self):
        threadmanager.SuspendableThread.__init__(
            self,
            name='MockSuspendableThreadButNotThreadSafeUnit'
        )

    def do_run(self):
        for n in range(1000):  # pylint: disable=C0103
            time.sleep(0.01)
            self.emit('progress', n / 1000.0, '%s of 1000' % n)
            self.check_for_sleep()


@pytest.mark.unittest
class TestThreadManagerUnit(object):  # pylint: disable=C0111

    # def test_threadingmanager_init(self, threadmanager_kill_patches):
    def test_threadingmanager_init(self, threadmanager_unit_mocker_stopall):
        "Replace job of old setUp function in unittest"
        temp_mocker = threadmanager_unit_mocker_stopall
        #####################################################################################################################
        temp_mocker.patch('scarlett_os.utility.gnome.abort_on_exception', lambda x: x)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch('scarlett_os.internal.gi.gi', spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch('scarlett_os.internal.gi.GLib', spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch('scarlett_os.internal.gi.GObject', spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch('scarlett_os.internal.gi.Gio', spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch('pydbus.SessionBus', spec=True, create=True)
        #####################################################################################################################
        tm = threadmanager.ThreadManager.get_instance(2)

        assert tm.active_count == 0
        assert tm.completed_threads == 0
        assert tm.count == 0
        assert tm.max_concurrent_threads == 2
        assert tm.thread_queue == []
        assert tm.threads == []

    def test_threadingmanager_add_thread_assertion_error_init(self, threadmanager_unit_mocker_stopall):
        "test_threadingmanager_add_thread_assertion_error_init Replace job of old setUp function in unittest"
        temp_mocker = threadmanager_unit_mocker_stopall
        #####################################################################################################################
        temp_mocker.patch('scarlett_os.utility.gnome.abort_on_exception', lambda x: x)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch('scarlett_os.internal.gi.gi', spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch('scarlett_os.internal.gi.GLib', spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch('scarlett_os.internal.gi.GObject', spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch('scarlett_os.internal.gi.Gio', spec=True, create=True)
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        temp_mocker.patch('pydbus.SessionBus', spec=True, create=True)
        #####################################################################################################################

        temp_mocker.patch('scarlett_os.utility.threadmanager.time.sleep', name=__name__ + '_mock_time_sleep')
        temp_mocker.patch('scarlett_os.utility.threadmanager.logging.Logger.debug', name=__name__ + '_mock_logger_debug')
        temp_mocker.patch('scarlett_os.utility.threadmanager._IdleObject', name=__name__ + '_mock_idle_obj')
        temp_mocker.patch('scarlett_os.utility.threadmanager.threading.Thread', autospec=True, name=__name__ + '_mock_thread_class')

        tm = threadmanager.ThreadManager.get_instance(2)

        class NotASuspendableThreadObj:  # pylint: disable=C0111
            pass

        # assert NotASuspendableThreadExc
        for desc, thread in [
            ('NotASuspendableThreadObj 1', NotASuspendableThreadObj()),
        ]:
            with pytest.raises(scarlett_os.utility.threadmanager.NotASuspendableThreadExc) as excinfo:
                tm.add_thread(thread)

