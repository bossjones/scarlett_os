#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_tasker
----------------------------------
"""

import os
import sys

import pytest
import unittest
import unittest.mock as mock

import scarlett_os

from scarlett_os.internal.gi import gi
from scarlett_os.internal.gi import GLib
from scarlett_os.internal.gi import GObject
import pydbus
# from pydbus import SessionBus

from scarlett_os import tasker  # Module with our thing to test
from scarlett_os.utility import gnome  # Module with the decorator we need to replace

# NOTE: We can't add this here, otherwise we won't be able to mock them
# from tests import common
import signal
import builtins
import scarlett_os.exceptions

import imp  # Library to help us reload our tasker module


class TestScarlettTasker(unittest.TestCase):

    def setUp(self):  # noqa: N802
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """
        # source: http://stackoverflow.com/questions/7667567/can-i-patch-a-python-decorator-before-it-wraps-a-function
        # Do cleanup first so it is ready if an exception is raised
        def kill_patches():  # Create a cleanup callback that undoes our patches
            mock.patch.stopall()  # Stops all patches started with start()
            imp.reload(tasker)  # Reload our UUT module which restores the original decorator
        self.addCleanup(kill_patches)  # We want to make sure this is run so we do this in addCleanup instead of tearDown

        self.old_glib_exception_error = GLib.GError
        # Now patch the decorator where the decorator is being imported from
        mock_abort_on_exception = mock.patch('scarlett_os.utility.gnome.abort_on_exception', lambda x: x).start()  # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_gi = mock.patch('scarlett_os.internal.gi.gi', spec=True).start()  # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()

        mock_glib = mock.patch('scarlett_os.internal.gi.GLib', spec=True).start()  # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()

        mock_gobject = mock.patch('scarlett_os.internal.gi.GObject', spec=True).start()  # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()

        mock_gio = mock.patch('scarlett_os.internal.gi.Gio', spec=True).start()  # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()

        # mock_pydbus = mock.patch('pydbus.bus.SessionBus', spec=True).start()  # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()

        # mock_pydbus.get.side_effect = Exception('GDBus.Error:org.freedesktop.DBus.Error.ServiceUnknown: The name org.scarlett was not provided by any .service files')

        # Exception Thrown from [/home/pi/.virtualenvs/scarlett_os/lib/python3.5/site-packages/pydbus/proxy.py] on line [40] via function [get]
        # Exception type Error: GDBus.Error:org.freedesktop.DBus.Error.ServiceUnknown: The name org.scarlett was not provided by any .service files

        # HINT: if you're patching a decor with params use something like:
        # lambda *x, **y: lambda f: f
        imp.reload(tasker)  # Reloads the tasker.py module which applies our patched decorator

    def tearDown(self):
        pass

    @mock.patch('scarlett_os.tasker._IdleObject', name='mock_idle_obj')
    @mock.patch('scarlett_os.utility.thread.time_logger', name='mock_time_logger')
    @mock.patch('scarlett_os.tasker.speaker', name='mock_scarlett_speaker')
    @mock.patch('scarlett_os.tasker.player', name='mock_scarlett_player')
    @mock.patch('scarlett_os.tasker.commands', name='mock_scarlett_commands')
    @mock.patch('scarlett_os.tasker.threading.RLock', spec=scarlett_os.tasker.threading.RLock, name='mock_threading_rlock')
    @mock.patch('scarlett_os.tasker.threading.Event', spec=scarlett_os.tasker.threading.Event, name='mock_threading_event')
    @mock.patch('scarlett_os.tasker.threading.Thread', spec=scarlett_os.tasker.threading.Thread, name='mock_thread_class')
    def test_tasker_init(self, mock_thread_class, mock_threading_event, mock_threading_rlock, mock_scarlett_commands, mock_scarlett_player, mock_scarlett_speaker, mock_time_logger, mock_idle_obj):
        # python3 -m scarlett_os.tasker
        #
        # /home/pi/dev/bossjones-github/scarlett_os/scarlett_os/tasker.py:106: PyGIDeprecationWarning: GObject.MainContext is deprecated; use GLib.MainContext instead
        #   context = GObject.MainContext.default()
        # Exception Thrown from [/home/pi/.virtualenvs/scarlett_os/lib/python3.5/site-packages/pydbus/proxy.py] on line [40] via function [get]
        # Exception type Error: GDBus.Error:org.freedesktop.DBus.Error.ServiceUnknown: The name org.scarlett was not provided by any .service files

        with pytest.raises(self.old_glib_exception_error) as excinfo:
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> traceback >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # tests/test_tasker.py:113: in test_tasker_init
            #     tskr = tasker.ScarlettTasker()
            # scarlett_os/tasker.py:113: in __init__
            #     ss = bus.get("org.scarlett", object_path='/org/scarlett/Listener')  # NOQA
            # /home/pi/.virtualenvs/scarlett_os/lib/python3.5/site-packages/pydbus/proxy.py:40: in get
            #     0, self.timeout, None).unpack()[0]
            # E   GLib.GError: g-io-error-quark: Timeout was reached (24)
            tskr = tasker.ScarlettTasker()

        # NOTE: This is because we can't talk to dbus service on ("org.scarlett", object_path='/org/scarlett/Listener'
        assert 'g-io-error-quark: Timeout was reached (24)' in str(excinfo.value)


class TestSoundType(unittest.TestCase):

    def setUp(self):  # noqa: N802
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """
        pass

    def test_soundtype_get_path(self):
        path_to_sound = '/home/pi/dev/bossjones-github/scarlett_os/static/sounds'
        self.assertEqual(tasker.STATIC_SOUNDS_PATH, path_to_sound)
        self.assertEqual(type(tasker.SoundType.get_path('pi-cancel')), list)
        self.assertEqual(tasker.SoundType.get_path('pi-cancel'), ["{}/pi-cancel.wav".format(path_to_sound)])
        self.assertEqual(tasker.SoundType.get_path('pi-listening'), ["{}/pi-listening.wav".format(path_to_sound)])
        self.assertEqual(tasker.SoundType.get_path('pi-response'), ["{}/pi-response.wav".format(path_to_sound)])
        self.assertEqual(tasker.SoundType.get_path('pi-response2'), ["{}/pi-response2.wav".format(path_to_sound)])


class TestSpeakerType(unittest.TestCase):

    def setUp(self):  # noqa: N802
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """
        pass

    def test_speakertype_speaker_to_array(self):
        self.assertEqual(type(tasker.SpeakerType.speaker_to_array('It is now, 05:34 PM')), list)
        self.assertEqual(tasker.SpeakerType.speaker_to_array('It is now, 05:34 PM'), ['It is now, 05:34 PM'])
