#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_subprocess
----------------------------------
"""

# import os
import sys


# import unittest
# import unittest.mock as mock
# from mock import call
# import unittest
import pytest
# from pytest_mock import mocker

# import mock
# import unittest.mock as mock

import scarlett_os
from scarlett_os.subprocess import check_pid
from scarlett_os.subprocess import Subprocess

# NOTE: We can't add this here, otherwise we won't be able to mock them
# from scarlett_os.internal.gi import GLib, GObject

# from tests import common
import signal
import builtins
import re
# new_callable: allows you to specify a different class,
# or callable object, that will be called to create the new object.
# By default MagicMock is used.


@pytest.fixture
def get_kill_mock(mocker):
    kill_mock = mocker.Mock(name="kill")
    yield kill_mock

# R0201 = Method could be a function Used when a method doesn't use its bound instance,
# and so could be written as a function.
# pylint: disable=R0201
# pylint: disable=C0111


class TestScarlettSubprocess(object):
    '''Units tests for Scarlett Subprocess, subclass of GObject.Gobject.'''

    # def test_speaker_init(self, mocker, monkeypatch):
    #        mock_time_logger = mocker.patch('scarlett_os.utility.thread.time_logger')
    #        mock_scarlett_player = mocker.patch('scarlett_os.speaker.player')
    #        mock_scarlett_subprocess = mocker.patch('scarlett_os.speaker.subprocess')

    # @mock.patch("os.kill", new=mock.Mock(side_effect=OSError))
    def test_check_pid_os_error(self, mocker):
        kill_mock = mocker.patch('scarlett_os.subprocess.os.kill', side_effect=OSError)
        # When OSError occurs, throw False
        assert not check_pid(4353634632623)
        # Verify that os.kill only called once
        assert kill_mock.call_count == 1

    # @mock.patch("os.kill", kill_mock)
    def test_check_pid(self, mocker):
        kill_mock = mocker.patch('scarlett_os.subprocess.os.kill')
        result = check_pid(123)
        assert kill_mock.called
        # NOTE: test against signal 0
        # sending the signal 0 to a given PID just checks if any
        # process with the given PID is running and you have the
        # permission to send a signal to it.
        kill_mock.assert_called_once_with(123, 0)
        assert result is True

    # @mock.patch('scarlett_os.subprocess.Subprocess.fork')
    # @mock.patch('scarlett_os.subprocess.logging.Logger.debug')
    # @mock.patch('scarlett_os.subprocess.Subprocess.check_command_type')
    # def test_subprocess_init(self, mock_check_command_type, mock_logging, mock_fork):
    def test_subprocess_init(self, mocker):
        test_result = '''
pi       tty7         2016-11-24 11:19 (:0)
pi       pts/5        2016-11-24 11:20 (10.0.2.2)
pi       pts/17       2016-11-24 11:20 (10.0.2.2)
'''

        mock_fork = \
            mocker.patch('scarlett_os.subprocess.Subprocess.fork')
        mock_logging = \
            mocker.patch('scarlett_os.subprocess.logging.Logger.debug')
        mock_check_command_type = \
            mocker.patch('scarlett_os.subprocess.Subprocess.check_command_type')  # noqa
        # NOTE: On purpose this is an invalid cmd. Should be of type array
        test_command = ['who']

        test_name = 'test_who'
        test_fork = False
        # test_return_tuple = (23241, None, None, None)

        # mock
        mock_check_command_type.return_value = True

        # command, name=None, fork=False
        s_test = scarlett_os.subprocess.Subprocess(test_command,
                                                   name=test_name,
                                                   fork=test_fork)

        # action
        assert s_test.check_command_type(test_command) is True
        mock_check_command_type.assert_called_with(['who'])
        assert not s_test.process
        assert not s_test.pid
        assert s_test.name == 'test_who'
        assert not s_test.forked
        assert s_test.stdout is True
        assert s_test.stderr is True
        assert s_test.stdout != False
        assert s_test.stderr != False

        mock_logging.assert_any_call("command: ['who']")
        mock_logging.assert_any_call("name: test_who")
        mock_logging.assert_any_call("forked: False")
        mock_logging.assert_any_call("process: None")
        mock_logging.assert_any_call("pid: None")
        mock_fork.assert_not_called()

    def test_subprocess_map_type_to_command(self, mocker):
        """Using the mock.patch decorator (removes the need to import builtins)"""

        mock_fork = \
            mocker.patch('scarlett_os.subprocess.Subprocess.fork')
        mock_logging = \
            mocker.patch('scarlett_os.subprocess.logging.Logger.debug')
        mock_check_command_type = \
            mocker.patch('scarlett_os.subprocess.Subprocess.check_command_type')  # noqa

        # NOTE: On purpose this is an invalid cmd. Should be of type array
        test_command = ["who", "-b"]
        test_name = 'test_who'
        test_fork = False

        # mock
        mock_check_command_type.return_value = True

        # create subprocess object
        s_test = scarlett_os.subprocess.Subprocess(test_command,
                                                   name=test_name,
                                                   fork=test_fork)
        map_output = s_test.map_type_to_command(test_command)

        # test
        assert isinstance(map_output, list)
        assert s_test.check_command_type(test_command)
        assert s_test.check_command_type(test_command) == mock_check_command_type.return_value

    def test_subprocess_check_command_type(self, mocker, monkeypatch):
        """Using the mock.patch decorator (removes the need to import builtins)"""

        test_command = ["who", "-b"]
        test_name = 'test_who'
        test_fork = False

        monkeypatch.setattr(Subprocess,
                            'map_type_to_command',
                            mocker.Mock(name='mock_map_type_to_command',
                                        return_value=int))

        monkeypatch.setattr(Subprocess,
                            'fork',
                            mocker.Mock())

        monkeypatch.setattr(scarlett_os.subprocess.logging.Logger,
                            'debug',
                            mocker.MagicMock())

        # Current thought, we aren't mocking from the correct context.
        # We're importing Subclass object,
        # but we're still trying to mock the remote object in the module instead of
        # in here.

        # Mock logger right off the bat
        #mocker.patch('scarlett_os.subprocess.logging.Logger.debug')

        # Create instance of Subprocess, disable all checks
        # sub = scarlett_os.subprocess.Subprocess(test_command,
        #                                         name=test_name,
        #                                         fork=test_fork,
        #                                         run_check_command=False)

        sub = Subprocess(test_command,
                         name=test_name,
                         fork=test_fork,
                         run_check_command=False)

        # import pdb;pdb.set_trace()

        # Mock instance member functions
        # mock_map_type_to_command = mocker.patch.object(sub, 'map_type_to_command', autospec=True)
        # mocker.patch.object(sub, 'fork')

        # Set mock return types
        # mock_map_type_to_command.return_value = int

        # action
        with pytest.raises(TypeError) as excinfo:
            sub.check_command_type(test_command)

        assert str(excinfo.value) == 'Variable types should return a list in python3.'
        # assert re.search('Variable types should return a list in python3.',
        #                  excinfo.value)

        # Assert TypeError inside types list
        mock_map_type_to_command.return_value = [int, int]

        with pytest.raises(TypeError) as excinfo:
            sub.check_command_type(test_command)

        assert str(excinfo.value) == 'Executables and arguments must be str objects. types'
        # assert re.search('Executables and arguments must be str objects. types',
        #                  excinfo.value)

    # @mock.patch('scarlett_os.subprocess.logging.Logger.debug')  # 2
    # def test_subprocess_fork(self, mock_logging):
    #     """Test fork class method process."""

    #     test_command = ["who", "-b"]
    #     test_name = 'test_who'
    #     test_fork = True
    #     pid = 7

    #     # mock
    #     with mock.patch('scarlett_os.subprocess.os.fork', mock.Mock(return_value=pid)) as mock_os_fork:
    #         with mock.patch('scarlett_os.subprocess.sys.exit', mock.Mock()) as mock_sys_exit:
    #             with mock.patch('scarlett_os.subprocess.os.chdir', mock.Mock()) as mock_os_chdir:
    #                 with mock.patch('scarlett_os.subprocess.os.setsid', mock.Mock()) as mock_os_setsid:
    #                     with mock.patch('scarlett_os.subprocess.os.umask', mock.Mock()) as mock_os_umask:

    #                         tfork1 = scarlett_os.subprocess.Subprocess(test_command,
    #                                                                    name=test_name,
    #                                                                    fork=test_fork)

    #                         assert mock_sys_exit.call_count == 2
    #                         assert tfork1.stdout == False
    #                         assert tfork1.stderr == False
    #                         assert mock_os_chdir.call_count == 1
    #                         assert mock_os_setsid.call_count == 1
    #                         assert mock_os_umask.call_count == 1
    #                         assert mock_os_fork.call_count == 2

    #                         mock_os_chdir.assert_called_once_with("/")

    # @mock.patch('scarlett_os.subprocess.logging.Logger.debug')  # 2
    # def test_subprocess_fork_exception(self, mock_logging):
    #     """Test fork class method process."""

    #     test_command = ["fake", "command"]
    #     test_name = 'fake_command'
    #     test_fork = True

    #     # mock
    #     with mock.patch('scarlett_os.subprocess.os.fork', mock.Mock(side_effect=OSError), create=True) as mock_os_fork:
    #         with mock.patch('scarlett_os.subprocess.sys.exit', mock.Mock()) as mock_sys_exit:
    #             with mock.patch('scarlett_os.subprocess.os.chdir', mock.Mock()) as mock_os_chdir:
    #                 with mock.patch('scarlett_os.subprocess.os.setsid', mock.Mock()) as mock_os_setsid:
    #                     with mock.patch('scarlett_os.subprocess.os.umask', mock.Mock()) as mock_os_umask:

    #                         tfork2 = scarlett_os.subprocess.Subprocess(test_command,
    #                                                                    name=test_name,
    #                                                                    fork=test_fork)

    #                         # NOTE: Bit of duplication we have going here.
    #                         assert mock_sys_exit.call_count == 2
    #                         assert tfork2.stdout == False
    #                         assert tfork2.stderr == False
    #                         assert mock_os_chdir.call_count == 1
    #                         assert mock_os_setsid.call_count == 1
    #                         assert mock_os_umask.call_count == 1
    #                         assert mock_os_fork.call_count == 2

    #                         mock_os_chdir.assert_called_once_with("/")

    # @mock.patch('scarlett_os.subprocess.logging.Logger.debug')
    # def test_subprocess_fork_pid0(self, mock_logging):
    #     """Test fork class method process."""

    #     test_command = ["who", "-b"]
    #     test_name = 'test_who'
    #     test_fork = True
    #     pid = 0

    #     # mock
    #     with mock.patch('scarlett_os.subprocess.os.fork', mock.Mock(return_value=pid)) as mock_os_fork:  # noqa
    #         with mock.patch('scarlett_os.subprocess.sys.exit', mock.Mock()) as mock_sys_exit:  # noqa
    #             with mock.patch('scarlett_os.subprocess.os.chdir', mock.Mock()) as mock_os_chdir:  # noqa
    #                 with mock.patch('scarlett_os.subprocess.os.setsid', mock.Mock()) as mock_os_setsid:  # noqa
    #                     with mock.patch('scarlett_os.subprocess.os.umask', mock.Mock()) as mock_os_umask:  # noqa

    #                         scarlett_os.subprocess.Subprocess(test_command,
    #                                                           name=test_name,
    #                                                           fork=test_fork)

    #                         assert mock_sys_exit.call_count == 0

    # @mock.patch('scarlett_os.subprocess.logging.Logger.error')
    # @mock.patch('scarlett_os.subprocess.logging.Logger.debug')
    # def test_subprocess_fork_pid0_exception(self, mock_logging_debug, mock_logging_error):
    #     """Test fork class method process."""

    #     test_command = ["who", "-b"]
    #     test_name = 'test_who'
    #     test_fork = True
    #     pid = 0

    #     # mock
    #     with mock.patch('scarlett_os.subprocess.os.fork', mock.Mock(side_effect=[pid, OSError]), create=True) as mock_os_fork:  # noqa
    #         with mock.patch('scarlett_os.subprocess.sys.exit', mock.Mock()) as mock_sys_exit:  # noqa
    #             with mock.patch('scarlett_os.subprocess.os.chdir', mock.Mock()) as mock_os_chdir:  # noqa
    #                 with mock.patch('scarlett_os.subprocess.os.setsid', mock.Mock()) as mock_os_setsid:  # noqa
    #                     with mock.patch('scarlett_os.subprocess.os.umask', mock.Mock()) as mock_os_umask:  # noqa
    #                         scarlett_os.subprocess.Subprocess(test_command,
    #                                                           name=test_name,
    #                                                           fork=test_fork)

    #                         mock_logging_error.assert_any_call("Error forking process second time")

    # @mock.patch('scarlett_os.subprocess.logging.Logger.debug')
    # def test_subprocess_fork_and_spawn_command(self, mock_logging_debug):
    #     """Test a full run connamd of Subprocess.run()"""

    #     test_command = ["who", "-b"]
    #     test_name = 'test_who'
    #     test_fork = False

    #     # mock
    #     with mock.patch('scarlett_os.subprocess.os.fork', mock.Mock(name='mock_os_fork')) as mock_os_fork:  # noqa
    #         with mock.patch('scarlett_os.subprocess.sys.exit', mock.Mock(name='mock_sys_exit')) as mock_sys_exit:  # noqa
    #             with mock.patch('scarlett_os.subprocess.os.chdir', mock.Mock(name='mock_os_chdir')) as mock_os_chdir:  # noqa
    #                 with mock.patch('scarlett_os.subprocess.os.setsid', mock.Mock(name='mock_os_setsid')) as mock_os_setsid:  # noqa
    #                     with mock.patch('scarlett_os.subprocess.os.umask', mock.Mock(name='mock_os_umask')) as mock_os_umask:  # noqa

    #                         # Import module locally for testing purposes
    #                         from scarlett_os.internal.gi import gi, GLib

    #                         # Save unpatched versions of the following so we can reset everything after tests finish
    #                         before_patch_gi_pid = gi._gi._glib.Pid
    #                         before_path_glib_spawn_async = GLib.spawn_async
    #                         before_path_child_watch_add = GLib.child_watch_add

    #                         test_pid = mock.Mock(spec=gi._gi._glib.Pid, return_value=23241, name='Mockgi._gi._glib.Pid')
    #                         test_pid.real = 23241
    #                         test_pid.close = mock.Mock(name='Mockgi._gi._glib.Pid.close')

    #                         # Mock function GLib function spawn_async
    #                         GLib.spawn_async = mock.create_autospec(GLib.spawn_async, return_value=(test_pid, None, None, None), name='MockGLib.spawn_async')

    #                         # Mock call to child_watch
    #                         GLib.child_watch_add = mock.create_autospec(GLib.child_watch_add)

    #                         # action
    #                         tfork1 = scarlett_os.subprocess.Subprocess(test_command,
    #                                                                    name=test_name,
    #                                                                    fork=test_fork)

    #                         with mock.patch('scarlett_os.subprocess.Subprocess.exited_cb', mock.Mock(name='mock_exited_cb', spec=scarlett_os.subprocess.Subprocess.exited_cb)) as mock_exited_cb:

    #                             with mock.patch('scarlett_os.subprocess.Subprocess.emit', mock.Mock(name='mock_emit', spec=scarlett_os.subprocess.Subprocess.emit)) as mock_emit:

    #                                 # action, kick off subprocess run
    #                                 tfork1.run()

    #                                 # assert
    #                                 mock_logging_debug.assert_any_call("command: {}".format(test_command))
    #                                 mock_logging_debug.assert_any_call("stdin: {}".format(None))
    #                                 mock_logging_debug.assert_any_call("stdout: {}".format(None))
    #                                 mock_logging_debug.assert_any_call("stderr: {}".format(None))

    #                                 assert tfork1.pid != 23241
    #                                 assert tfork1.stdin == None
    #                                 assert tfork1.stdout == None
    #                                 assert tfork1.stderr == None
    #                                 assert tfork1.forked == False
    #                                 assert mock_emit.call_count == 0

    #                                 GLib.spawn_async.assert_called_once_with(test_command,
    #                                                                          flags=GLib.SpawnFlags.SEARCH_PATH | GLib.SpawnFlags.DO_NOT_REAP_CHILD
    #                                                                          )

    #                                 GLib.child_watch_add.assert_called_once_with(GLib.PRIORITY_HIGH, test_pid, mock_exited_cb)

    #                                 # now unpatch all of these guys
    #                                 gi._gi._glib.Pid = before_patch_gi_pid
    #                                 GLib.spawn_async = before_path_glib_spawn_async
    #                                 GLib.child_watch_add = before_path_child_watch_add

    # # NOTE: Decorators get applied BOTTOM to TOP
    # def test_check_command_type_is_array_of_str(self):
    #     # source: http://stackoverflow.com/questions/28181867/how-do-a-mock-a-superclass-that-is-part-of-a-library
    #     with pytest.raises(Exception):
    #         Subprocess()  # Normal implementation raise Exception

    #     # Pay attention to return_value MUST be None for all __init__ methods
    #     with mock.patch("scarlett_os.subprocess.Subprocess.__init__", autospec=True, return_value=None) as mock_init:
    #         with pytest.raises(TypeError):
    #             Subprocess()  # Wrong argument: autospec=True let as to catch it
    #         s = Subprocess(['who'])  # Ok now it works
    #         mock_init.assert_called_with(mock.ANY, ['who'])  # Use autospec=True inject self as first argument -> use Any to discard it
    #         assert s.check_command_type(['who']) == True
