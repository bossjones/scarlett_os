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

import imp  # Library to help us reload our tasker module


class MockSuspendableThreadButNotThreadSafe(threadmanager.SuspendableThread, threadmanager.NotThreadSafe):

    def __init__(self):
        threadmanager.SuspendableThread.__init__(
            self,
            name='MockSuspendableThreadButNotThreadSafe'
        )

    def do_run(self):
        for n in range(1000):
            time.sleep(0.01)
            self.emit('progress', n / 1000.0, '%s of 1000' % n)
            self.check_for_sleep()


class TestThreadManager(unittest.TestCase):

    def setUp(self):  # noqa: N802
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """
        # source: http://stackoverflow.com/questions/7667567/can-i-patch-a-python-decorator-before-it-wraps-a-function
        # Do cleanup first so it is ready if an exception is raised
        def kill_patches():  # Create a cleanup callback that undoes our patches
            mock.patch.stopall()  # Stops all patches started with start()
            imp.reload(threadmanager)  # Reload our UUT module which restores the original decorator
        self.addCleanup(kill_patches)  # We want to make sure this is run so we do this in addCleanup instead of tearDown

        self.old_glib_exception_error = GLib.GError
        # Now patch the decorator where the decorator is being imported from
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_abort_on_exception = mock.patch('scarlett_os.utility.gnome.abort_on_exception', lambda x: x).start()
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_gi = mock.patch('scarlett_os.internal.gi.gi', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_glib = mock.patch('scarlett_os.internal.gi.GLib', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_gobject = mock.patch('scarlett_os.internal.gi.GObject', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_gio = mock.patch('scarlett_os.internal.gi.Gio', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_pydbus_SessionBus = mock.patch('pydbus.SessionBus', spec=True, create=True).start()

        # mock_pydbus_SessionBus.return_value

        # mock_time = mock.patch('time.sleep', spec=True, create=True).start()  # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        # mock_pydbus.get.side_effect = Exception('GDBus.Error:org.freedesktop.DBus.Error.ServiceUnknown: The name org.scarlett was not provided by any .service files')

        # Exception Thrown from [/home/pi/.virtualenvs/scarlett_os/lib/python3.5/site-packages/pydbus/proxy.py] on line [40] via function [get]
        # Exception type Error:
        # GDBus.Error:org.freedesktop.DBus.Error.ServiceUnknown: The name
        # org.scarlett was not provided by any .service files

        # HINT: if you're patching a decor with params use something like:
        # lambda *x, **y: lambda f: f
        imp.reload(threadmanager)  # Reloads the tasker.py module which applies our patched decorator

    def test_threadingmanager_init(self):
        tm = threadmanager.get_thread_manager(2)

        self.assertEqual(tm.active_count, 0)
        self.assertEqual(tm.completed_threads, 0)
        self.assertEqual(tm.count, 0)
        self.assertEqual(tm.max_concurrent_threads, 2)
        self.assertEqual(tm.thread_queue, [])
        self.assertEqual(tm.threads, [])

        del tm

    @mock.patch('scarlett_os.utility.threadmanager.time.sleep', name='mock_time_sleep')
    @mock.patch('scarlett_os.utility.threadmanager.logging.Logger.debug', name='mock_logger_debug')
    @mock.patch('scarlett_os.utility.threadmanager._IdleObject', name='mock_idle_obj')
    @mock.patch('scarlett_os.utility.threadmanager.threading.Thread', spec=scarlett_os.utility.threadmanager.threading.Thread, name='mock_thread_class')
    def test_threadingmanager_add_thread_assertion_error_init(self, mock_thread_class, mock_idle_obj, mock_logger_debug, mock_time_sleep):
        tm = threadmanager.get_thread_manager(2)

        # import pdb;pdb.set_trace()
        class NotASuspendableThreadObj:
            pass

        # NotASuspendableThreadObj = mock.Mock()
        # not_suspendable_obj = NotASuspendableThreadObj()
        # not_suspendable_obj.check_for_sleep = mock.MagicMock(side_effect=scarlett_os.utility.threadmanager.NotASuspendableThreadExc)
        # not_suspendable_obj.name = 'NotASuspendableThreadObj'

        # assert NotASuspendableThreadExc
        for desc, thread in [
            ('NotASuspendableThreadObj 1', NotASuspendableThreadObj()),
        ]:
            # with self.assertRaises(TypeError):
            with self.assertRaises(scarlett_os.utility.threadmanager.NotASuspendableThreadExc):
                tm.add_thread(thread)

        # # assert NotThreadSafeExc
        # for desc, thread in [
        #     ('NotThreadSafeObj 1', MockSuspendableThreadButNotThreadSafe()),
        # ]:
        #     with self.assertRaises(TypeError):
        #         with self.assertRaises(scarlett_os.utility.threadmanager.NotThreadSafeExc):
        #             tm.add_thread(thread)

        del tm
