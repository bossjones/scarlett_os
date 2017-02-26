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
from mock import call

import scarlett_os
from scarlett_os import tasker  # Module with our thing to test
from scarlett_os.utility import gnome  # Module with the decorator we need to replace

import time
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

# py.test -s --tb short --cov-config .coveragerc --cov scarlett_os tests --cov-report html --benchmark-skip --pdb --showlocals
# strace -s 40000 -vvtf python setup.py test > ./strace.out.strace 2>&1

#######################################################################################################################
# import os
# import sys
# import signal
# import pytest
# import builtins
# import threading
#
# import pydbus
# import scarlett_os
# import scarlett_os.exceptions
#
# import time
#
# from scarlett_os.internal import gi  # noqa
# from scarlett_os.internal.gi import Gio  # noqa
# from scarlett_os.internal.gi import GObject  # noqa
# from scarlett_os.internal.gi import GLib
#
# from scarlett_os import tasker
#
# # from scarlett_os.tasker import on_signal_recieved
# from scarlett_os.tasker import print_args
# from scarlett_os.tasker import print_keyword_args
# from scarlett_os.tasker import call_speaker
# from scarlett_os.tasker import call_espeak_subprocess
# # from scarlett_os.tasker import call_player
# from scarlett_os.tasker import SoundType
#
# from scarlett_os.internal.debugger import dump
#
# import scarlett_os.logger
#
#
# import pydbus
# from pydbus import SessionBus
#
# from scarlett_os.utility.dbus_runner import DBusRunner
#
# from scarlett_os.utility.generators import GIdleThread
# from scarlett_os.utility.generators import QueueEmpty
# from scarlett_os.utility.generators import QueueFull
# from scarlett_os.utility.generators import Queue
# # from scarlett_os.utility.generators import Queue
# #
# from scarlett_os.utility.gnome import abort_on_exception
#######################################################################################################################


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
        imp.reload(tasker)  # Reloads the tasker.py module which applies our patched decorator

    @mock.patch('scarlett_os.utility.dbus_runner.DBusRunner', autospec=True, name='mock_dbusrunner')
    @mock.patch('scarlett_os.tasker.TaskSignalHandler', spec=scarlett_os.tasker.TaskSignalHandler, name='mock_task_signal_handler')
    @mock.patch('scarlett_os.tasker.time.sleep', name='mock_time_sleep')
    @mock.patch('scarlett_os.tasker.logging.Logger.debug', name='mock_logger_debug')
    @mock.patch('scarlett_os.tasker._IdleObject', name='mock_idle_obj')
    @mock.patch('scarlett_os.utility.thread.time_logger', name='mock_time_logger')
    @mock.patch('scarlett_os.tasker.speaker', name='mock_scarlett_speaker')
    @mock.patch('scarlett_os.tasker.player', name='mock_scarlett_player')
    @mock.patch('scarlett_os.tasker.commands', name='mock_scarlett_commands')
    @mock.patch('scarlett_os.tasker.threading.RLock', spec=scarlett_os.tasker.threading.RLock, name='mock_threading_rlock')
    @mock.patch('scarlett_os.tasker.threading.Event', spec=scarlett_os.tasker.threading.Event, name='mock_threading_event')
    @mock.patch('scarlett_os.tasker.threading.Thread', spec=scarlett_os.tasker.threading.Thread, name='mock_thread_class')
    def test_tasker_init(self, mock_thread_class, mock_threading_event, mock_threading_rlock, mock_scarlett_commands, mock_scarlett_player, mock_scarlett_speaker, mock_time_logger, mock_idle_obj, mock_logger_debug, mock_time_sleep, mock_task_signal_handler, mock_dbusrunner):
        tskr = tasker.ScarlettTasker()

    @mock.patch('scarlett_os.utility.dbus_runner.DBusRunner', autospec=True, name='mock_dbusrunner')
    @mock.patch('scarlett_os.tasker.TaskSignalHandler', spec=scarlett_os.tasker.TaskSignalHandler, name='mock_task_signal_handler')
    @mock.patch('scarlett_os.tasker.time.sleep', name='mock_time_sleep')
    @mock.patch('scarlett_os.tasker.logging.Logger.debug', name='mock_logger_debug')
    @mock.patch('scarlett_os.tasker._IdleObject', name='mock_idle_obj')
    @mock.patch('scarlett_os.utility.thread.time_logger', name='mock_time_logger')
    @mock.patch('scarlett_os.tasker.speaker', name='mock_scarlett_speaker')
    @mock.patch('scarlett_os.tasker.player', name='mock_scarlett_player')
    @mock.patch('scarlett_os.tasker.commands', name='mock_scarlett_commands')
    @mock.patch('scarlett_os.tasker.threading.RLock', spec=scarlett_os.tasker.threading.RLock, name='mock_threading_rlock')
    @mock.patch('scarlett_os.tasker.threading.Event', spec=scarlett_os.tasker.threading.Event, name='mock_threading_event')
    @mock.patch('scarlett_os.tasker.threading.Thread', spec=scarlett_os.tasker.threading.Thread, name='mock_thread_class')
    def test_tasker_reset(self, mock_thread_class, mock_threading_event, mock_threading_rlock, mock_scarlett_commands, mock_scarlett_player, mock_scarlett_speaker, mock_time_logger, mock_idle_obj, mock_logger_debug, mock_time_sleep, mock_task_signal_handler, mock_dbusrunner):
        # dbus mocks
        _dr = mock_dbusrunner.get_instance()
        bus = _dr.get_session_bus()

        # handler mocks
        _handler = mock_task_signal_handler()
        tskr = tasker.ScarlettTasker()

        tskr.reset()

        self.assertEqual(_handler.clear.call_count, 1)
        self.assertIsNone(tskr._failed_signal_callback)
        self.assertIsNone(tskr._ready_signal_callback)
        self.assertIsNone(tskr._keyword_recognized_signal_callback)
        self.assertIsNone(tskr._command_recognized_signal_callback)
        self.assertIsNone(tskr._cancel_signal_callback)
        self.assertIsNone(tskr._connect_signal_callback)

    @mock.patch('scarlett_os.utility.dbus_runner.DBusRunner', autospec=True, name='mock_dbusrunner')
    @mock.patch('scarlett_os.tasker.TaskSignalHandler', spec=scarlett_os.tasker.TaskSignalHandler, name='mock_task_signal_handler')
    @mock.patch('scarlett_os.tasker.time.sleep', name='mock_time_sleep')
    @mock.patch('scarlett_os.tasker.logging.Logger.debug', name='mock_logger_debug')
    @mock.patch('scarlett_os.tasker._IdleObject', name='mock_idle_obj')
    @mock.patch('scarlett_os.utility.thread.time_logger', name='mock_time_logger')
    @mock.patch('scarlett_os.tasker.speaker', name='mock_scarlett_speaker')
    @mock.patch('scarlett_os.tasker.player', name='mock_scarlett_player')
    @mock.patch('scarlett_os.tasker.commands', name='mock_scarlett_commands')
    @mock.patch('scarlett_os.tasker.threading.RLock', spec=scarlett_os.tasker.threading.RLock, name='mock_threading_rlock')
    @mock.patch('scarlett_os.tasker.threading.Event', spec=scarlett_os.tasker.threading.Event, name='mock_threading_event')
    @mock.patch('scarlett_os.tasker.threading.Thread', spec=scarlett_os.tasker.threading.Thread, name='mock_thread_class')
    def test_tasker_prepare(self, mock_thread_class, mock_threading_event, mock_threading_rlock, mock_scarlett_commands, mock_scarlett_player, mock_scarlett_speaker, mock_time_logger, mock_idle_obj, mock_logger_debug, mock_time_sleep, mock_task_signal_handler, mock_dbusrunner):
        # dbus mocks
        _dr = mock_dbusrunner.get_instance()
        bus = _dr.get_session_bus()

        # handler mocks
        _handler = mock_task_signal_handler()
        tskr = tasker.ScarlettTasker()

        def on_signal_recieved(*args, **kwargs):
            print('on_signal_recieved')

        def connected_to_listener_cb(*args, **kwargs):
            print('connected_to_listener_cb')

        tskr.prepare(on_signal_recieved, on_signal_recieved, on_signal_recieved)

        self.assertEqual(_handler.clear.call_count, 1)
        self.assertIsNotNone(tskr._failed_signal_callback)
        self.assertIsNotNone(tskr._ready_signal_callback)
        self.assertIsNotNone(tskr._keyword_recognized_signal_callback)
        self.assertIsNotNone(tskr._command_recognized_signal_callback)
        self.assertIsNotNone(tskr._cancel_signal_callback)
        self.assertIsNotNone(tskr._connect_signal_callback)

    # @mock.patch('scarlett_os.utility.dbus_runner.DBusRunner', autospec=True, name='mock_dbusrunner')
    # # use autospec for TaskSignalHandler otherwise mocks don't work correctly
    # @mock.patch('scarlett_os.tasker.TaskSignalHandler', autospec=True, name='mock_task_signal_handler')
    # # @mock.patch('scarlett_os.tasker.TaskSignalHandler', spec=scarlett_os.tasker.TaskSignalHandler, name='mock_task_signal_handler')
    # @mock.patch('scarlett_os.tasker.time.sleep', name='mock_time_sleep')
    # @mock.patch('scarlett_os.tasker.logging.Logger.debug', name='mock_logger_debug')
    # @mock.patch('scarlett_os.tasker._IdleObject', name='mock_idle_obj')
    # @mock.patch('scarlett_os.utility.thread.time_logger', name='mock_time_logger')
    # @mock.patch('scarlett_os.tasker.speaker', name='mock_scarlett_speaker')
    # @mock.patch('scarlett_os.tasker.player', name='mock_scarlett_player')
    # @mock.patch('scarlett_os.tasker.commands', name='mock_scarlett_commands')
    # @mock.patch('scarlett_os.tasker.threading.RLock', spec=scarlett_os.tasker.threading.RLock, name='mock_threading_rlock')
    # @mock.patch('scarlett_os.tasker.threading.Event', spec=scarlett_os.tasker.threading.Event, name='mock_threading_event')
    # @mock.patch('scarlett_os.tasker.threading.Thread', spec=scarlett_os.tasker.threading.Thread, name='mock_thread_class')
    # def test_tasker_configure(self, mock_thread_class, mock_threading_event, mock_threading_rlock, mock_scarlett_commands, mock_scarlett_player, mock_scarlett_speaker, mock_time_logger, mock_idle_obj, mock_logger_debug, mock_time_sleep, mock_task_signal_handler, mock_dbusrunner):
    #     # dbus mocks
    #     # assert 0
    #     # tests/test_tasker.py:237: in test_tasker_configure
    #     #     tskr._handler.assert_has_calls(calls_to_connect, any_order=True)
    #     # /usr/lib/python3.5/unittest/mock.py:838: in assert_has_calls
    #     #     ) from cause
    #     # E   AssertionError: (('', <BoundArguments (args=(<MagicMock name='mock_dbusrunner.get_instance().get_session_bus()' id='140593350583240'>, 'SttFailedSignal', <function TestScarlettTasker.test_tasker_configure.<locals>.player_cb at 0x7fde70b7f158>))>), ('', <BoundArguments (args=(<MagicMock name='mock_dbusrunner.get_instance().get_session_bus()' id='140593350583240'>, 'ListenerReadySignal', <function TestScarlettTasker.test_tasker_configure.<locals>.player_cb at 0x7fde70b7f158>))>), ('', <BoundArguments (args=(<MagicMock name='mock_dbusrunner.get_instance().get_session_bus()' id='140593350583240'>, 'KeywordRecognizedSignal', <function TestScarlettTasker.test_tasker_configure.<locals>.player_cb at 0x7fde70b7f158>))>), ('', <BoundArguments (args=(<MagicMock name='mock_dbusrunner.get_instance().get_session_bus()' id='140593350583240'>, 'CommandRecognizedSignal', <function TestScarlettTasker.test_tasker_configure.<locals>.command_cb at 0x7fde70b7f1e0>))>), ('', <BoundArguments (args=(<MagicMock name='mock_dbusrunner.get_instance().get_session_bus()' id='140593350583240'>, 'ListenerCancelSignal', <function TestScarlettTasker.test_tasker_configure.<locals>.player_cb at 0x7fde70b7f158>))>), ('', <BoundArguments (args=(<MagicMock name='mock_dbusrunner.get_instance().get_session_bus()' id='140593350583240'>, 'ConnectedToListener', <function TestScarlettTasker.test_tasker_configure.<locals>.connected_to_listener_cb at 0x7fde70b7f268>))>)) not all found in call list
    #
    #     _dr = mock_dbusrunner.get_instance()
    #     bus = _dr.get_session_bus()
    #
    #     # # handler mocks
    #     _handler = mock_task_signal_handler()
    #     tskr = tasker.ScarlettTasker()
    #
    #     # import pdb;pdb.set_trace()
    #
    #     def player_cb(*args, **kwargs):
    #         print('player_cb')
    #
    #     def command_cb(*args, **kwargs):
    #         print('command_cb')
    #
    #     def connected_to_listener_cb(*args, **kwargs):
    #         print('connected_to_listener_cb')
    #
    #     tskr.prepare(player_cb, command_cb, connected_to_listener_cb)
    #     tskr.configure()
    #
    #     # _handler.MainLoop = mock.create_autospec(scarlett_os.tasker.TaskSignalHandler.connect, name='Mock_GObject.MainLoop')
    #
    #     self.assertEqual(_handler.connect.call_count, 6)
    #     calls_to_connect = []
    #     calls_to_connect.append(call.clear())
    #     calls_to_connect.append(call.connect(mock.ANY, "SttFailedSignal", player_cb))
    #     calls_to_connect.append(call.connect(mock.ANY, "ListenerReadySignal", player_cb))
    #     calls_to_connect.append(call.connect(mock.ANY, "KeywordRecognizedSignal", player_cb))
    #     calls_to_connect.append(call.connect(mock.ANY, "CommandRecognizedSignal", command_cb))
    #     calls_to_connect.append(call.connect(mock.ANY, "ListenerCancelSignal", player_cb))
    #     calls_to_connect.append(call.connect(mock.ANY, "ConnectedToListener", connected_to_listener_cb))
    #
    #     # calls_to_connect = [call(bus, "SttFailedSignal", player_cb),
    #     #                     call(bus, "ListenerReadySignal", player_cb),
    #     #                     call(bus, "KeywordRecognizedSignal", player_cb),
    #     #                     call(bus, "CommandRecognizedSignal", command_cb),
    #     #                     call(bus, "ListenerCancelSignal", player_cb),
    #     #                     call(bus, "ConnectedToListener", connected_to_listener_cb)
    #     #                     ]
    #     # assert 0
    #
    #     tskr._handler.assert_has_calls(calls_to_connect, any_order=False)
    #     # tskr._handler.connect.assert_any_call(bus, "SttFailedSignal", player_cb)
    #     # tskr._handler.connect.assert_any_call(bus, "ListenerReadySignal", player_cb)
    #     # tskr._handler.connect.assert_any_call(bus, "KeywordRecognizedSignal", player_cb)
    #     # tskr._handler.connect.assert_any_call(bus, "CommandRecognizedSignal", command_cb)
    #     # tskr._handler.connect.assert_any_call(bus, "ListenerCancelSignal", player_cb)
    #     # tskr._handler.connect.assert_any_call(bus, "ConnectedToListener", connected_to_listener_cb)
    #
    #     # _handler.connect. _mock_call_args_list = [
    #     #
    #     #      call(<MagicMock name='mock_dbusrunner._DBusRunner__instance.get_session_bus()' id='140448322930728'>, 'SttFailedSignal', <function TestScarlettTasker.test_tasker_configure.<locals>.player_cb at 0x7fbcac67b8c8>),
    #     #
    #     #      call(<MagicMock name='mock_dbusrunner._DBusRunner__instance.get_session_bus()' id='140448322930728'>, 'ListenerReadySignal', <function TestScarlettTasker.test_tasker_configure.<locals>.player_cb at 0x7fbcac67b8c8>),
    #     #
    #     #      call(<MagicMock name='mock_dbusrunner._DBusRunner__instance.get_session_bus()' id='140448322930728'>, 'KeywordRecognizedSignal', <function TestScarlettTasker.test_tasker_configure.<locals>.player_cb at 0x7fbcac67b8c8>),
    #     #
    #     #      call(<MagicMock name='mock_dbusrunner._DBusRunner__instance.get_session_bus()' id='140448322930728'>, 'CommandRecognizedSignal', <function TestScarlettTasker.test_tasker_configure.<locals>.command_cb at 0x7fbcac67b840>),
    #     #
    #     #      call(<MagicMock name='mock_dbusrunner._DBusRunner__instance.get_session_bus()' id='140448322930728'>, 'ListenerCancelSignal', <function TestScarlettTasker.test_tasker_configure.<locals>.player_cb at 0x7fbcac67b8c8>),
    #     #
    #     #      call(<MagicMock name='mock_dbusrunner._DBusRunner__instance.get_session_bus()' id='140448322930728'>, 'ConnectedToListener', <function TestScarlettTasker.test_tasker_configure.<locals>.connected_to_listener_cb at 0x7fbcac67b6a8>)
    #     #
    #     #  ]
    #
    #     # self._failed_signal_callback = player_cb
    #     # self._ready_signal_callback = player_cb
    #     # self._keyword_recognized_signal_callback = player_cb
    #     # self._command_recognized_signal_callback = command_cb
    #     # self._cancel_signal_callback = player_cb
    #     # self._connect_signal_callback = connected_to_listener_cb
    #
    #     # if self._failed_signal_callback:
    #     #     self._handler.connect(bus, "SttFailedSignal", self._failed_signal_callback)
    #     #
    #     # if self._ready_signal_callback:
    #     #     self._handler.connect(bus, "ListenerReadySignal", self._ready_signal_callback)
    #     #
    #     # if self._keyword_recognized_signal_callback:
    #     #     self._handler.connect(bus, "KeywordRecognizedSignal", self._keyword_recognized_signal_callback)
    #     #
    #     # if self._command_recognized_signal_callback:
    #     #     self._handler.connect(bus, "CommandRecognizedSignal", self._command_recognized_signal_callback)
    #     #
    #     # if self._cancel_signal_callback:
    #     #     self._handler.connect(bus, "ListenerCancelSignal", self._cancel_signal_callback)
    #     #
    #     # if self._connect_signal_callback:
    #     #     self._handler.connect(bus, "ConnectedToListener", self._connect_signal_callback)
    #
    #     # self._handler.connect(bus, "SttFailedSignal", self._failed_signal_callback)
    #     # self._handler.connect(bus, "SttFailedSignal", test_cb)
    #
    #     self.assertEqual(_handler.clear.call_count, 1)
    #     self.assertIsNotNone(tskr._failed_signal_callback)
    #     self.assertIsNotNone(tskr._ready_signal_callback)
    #     self.assertIsNotNone(tskr._keyword_recognized_signal_callback)
    #     self.assertIsNotNone(tskr._command_recognized_signal_callback)
    #     self.assertIsNotNone(tskr._cancel_signal_callback)
    #     self.assertIsNotNone(tskr._connect_signal_callback)


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


class TestTaskSignalHandler(unittest.TestCase):

    def setUp(self):  # noqa: N802
        """
        TestTaskSignalHandler
        """
        self._handler = tasker.TaskSignalHandler()

        def kill_patches():  # Create a cleanup callback that undoes our patches
            mock.patch.stopall()  # Stops all patches started with start()
            imp.reload(tasker)  # Reload our UUT module which restores the original decorator
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

        imp.reload(tasker)  # Reloads the tasker.py module which applies our patched decorator

    def tearDown(self):
        del(self._handler)
        self._handler = None

    @mock.patch('scarlett_os.utility.dbus_runner.DBusRunner', autospec=True, name='mock_dbusrunner')
    def test_connect_then_disconnect(self, mock_dbusrunner):
        _dr = mock_dbusrunner.get_instance()
        bus = _dr.get_session_bus()

        def test_cb():
            print('test_cb')

        self._handler.connect(bus, "SttFailedSignal", test_cb)

        # assertions
        self.assertEqual(len(self._handler._ids), 1)

        bus.subscribe.assert_called_once_with(sender=None,
                                              iface="org.scarlett.Listener",
                                              signal="SttFailedSignal",
                                              object="/org/scarlett/Listener",
                                              arg0=None,
                                              flags=0,
                                              signal_fired=test_cb)

        # Disconnect then test again
        self._handler.disconnect(bus, "SttFailedSignal")

        self.assertEqual(len(self._handler._ids), 0)

    @mock.patch('scarlett_os.utility.dbus_runner.DBusRunner', autospec=True, name='mock_dbusrunner')
    def test_connect_then_clear(self, mock_dbusrunner):
        _dr = mock_dbusrunner.get_instance()
        bus = _dr.get_session_bus()

        def test_cb():
            print('test_cb')

        self._handler.connect(bus, "SttFailedSignal", test_cb)

        # Disconnect then test again
        self._handler.clear()

        self.assertEqual(len(self._handler._ids), 0)


class TestSpeakerType(unittest.TestCase):

    def setUp(self):  # noqa: N802
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """
        pass

    def test_speakertype_speaker_to_array(self):
        self.assertEqual(type(tasker.SpeakerType.speaker_to_array('It is now, 05:34 PM')), list)
        self.assertEqual(tasker.SpeakerType.speaker_to_array('It is now, 05:34 PM'), ['It is now, 05:34 PM'])
