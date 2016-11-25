#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_subprocess
----------------------------------
"""

import os
import sys

import unittest

# import mock
import unittest.mock as mock

import scarlett_os
from scarlett_os.subprocess import check_pid
from scarlett_os.internal.gi import GLib, GObject

from tests import common


# self.res = generator_subprocess.Subprocess(
#                 self._command, name='speaker_tmp', fork=False).run()
#             generator_subprocess.check_pid(int(self.res))


# new_callable: allows you to specify a different class, or callable object, that will be called to create the new object. By default MagicMock is used.

def raise_OSError(*x, **kw):
    raise OSError('Fail')


class MockSubprocess(GObject.GObject):

    def __init__(self):
        GObject.GObject.__init__(self, common.create_scarlett_os_subprocess_mock())


# class MockedPipeline(pipeline.Pipeline):
#
#     def __init__(self):
#         pipeline.Pipeline.__init__(self, common.create_pitivi_mock())
#         self.state_calls = {}
#         self._timeline = mock.MagicMock()


class TestScarlettSubprocess(unittest.TestCase):

    def setUp(self):
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """

        # spec: This can be either a list of strings or an existing object (a class or instance) that acts as the specification for the mock object. If you pass in an object then a list of strings is formed by calling dir on the object (excluding unsupported magic attributes and methods). Accessing any attribute not in this list will raise an AttributeError.
        self.mock = mock.Mock(spec=scarlett_os.subprocess.Subprocess)

    @mock.patch("os.kill", new=mock.Mock(side_effect=OSError))
    def test_check_pid(self):
        self.assertFalse(check_pid(4353634632623))

    # ME: def __init__(self, command, name=None, fork=False):
    # THEM: def __init__(self, host, port, protocol, protocol_kwargs=None,
    #             max_connections=5, timeout=30):
    #    self.protocol = protocol
    #    self.protocol_kwargs = protocol_kwargs or {}
    #    self.max_connections = max_connections
    #    self.timeout = timeout
    #    self.server_socket = self.create_server_socket(host, port)

    #    self.register_server_socket(self.server_socket.fileno())

    # NOTE: Decorators get applied BOTTOM to TOP
    @mock.patch("scarlett_os.internal.gi.GLib.spawn_async")
    def test_check_command_type_not_str(self, mock_glib_spawn_async):
        # test_pid, test_stdin, test_stdout, test_stderr = GLib.spawn_async(test_command,
        #                                                                   flags=GLib.SpawnFlags.SEARCH_PATH | GLib.SpawnFlags.DO_NOT_REAP_CHILD
        #                                                                   )
        #
        # Out[11]: (23241, None, None, None)
        #
        # In [12]:  07:29:39 up 20:10,  3 users,  load average: 0.11, 0.08, 0.02
        # USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
        # In [12]:
        #
        # In [12]:

        test_result = '''
pi       tty7         2016-11-24 11:19 (:0)
pi       pts/5        2016-11-24 11:20 (10.0.2.2)
pi       pts/17       2016-11-24 11:20 (10.0.2.2)
'''
        # NOTE: On purpose this is an invalid cmd. Should be of type array
        test_command = 'who'
        test_name = None
        test_fork = False
        test_return_tuple = (23241, None, None, None)

        # command, name=None, fork=False
        s_test = scarlett_os.subprocess.Subprocess(test_command, test_name, test_fork)

        # action
        s_test.spawn_command()

        # assert
        mock_glib_spawn_async.assert_called_once_with(test_command,
                                                      flags=GLib.SpawnFlags.SEARCH_PATH | GLib.SpawnFlags.DO_NOT_REAP_CHILD)

        pass

    # NOTE: Decorators get applied BOTTOM to TOP
    @mock.patch("scarlett_os.internal.gi.GLib.spawn_async")
    @mock.patch("scarlett_os.subprocess.Subprocess.check_command_type")
    def test_spawn_command(self, mock_glib_spawn_async, mock_check_command_type):
        # test_pid, test_stdin, test_stdout, test_stderr = GLib.spawn_async(test_command,
        #                                                                   flags=GLib.SpawnFlags.SEARCH_PATH | GLib.SpawnFlags.DO_NOT_REAP_CHILD
        #                                                                   )
        #
        # Out[11]: (23241, None, None, None)
        #
        # In [12]:  07:29:39 up 20:10,  3 users,  load average: 0.11, 0.08, 0.02
        # USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
        # In [12]:
        #
        # In [12]:

        test_result = '''
pi       tty7         2016-11-24 11:19 (:0)
pi       pts/5        2016-11-24 11:20 (10.0.2.2)
pi       pts/17       2016-11-24 11:20 (10.0.2.2)
'''
        test_command = ['who']
        test_name = None
        test_fork = False
        test_return_tuple = (23241, None, None, None)

        # mock
        mock_check_command_type.return_value = True

        # action
        # command, name=None, fork=False
        s_test = scarlett_os.subprocess.Subprocess(test_command, test_name, test_fork)
        s_test.spawn_command()

        # assert
        self.assertEquals(s_test.check_command_type(test_command), True)
        self.assertEquals(mock_glib_spawn_async.call_count, 1)

        # scarlett_os.subprocess.Subprocess.__init__(
        #     self.mock, mock.sentinel.command)
        # self.mock.create_server_socket.assert_called_once_with(
        #     mock.sentinel.host, mock.sentinel.port)
        pass


# In [2]: import os
#
# In [3]: import sys
#
# In [4]: import unittest
#
# In [5]: import unittest.mock as mock
#
# In [6]: import scarlett_os
#
# In [7]: from scarlett_os.subprocess import check_pid
#
# In [8]: mock = mock.Mock(spec=scarlett_os.subprocess.Subprocess)
#
# In [9]: mock
# Out[9]: <Mock spec='Subprocess' id='139701201134816'>
#
# In [10]:

# In [14]: import unittest.mock as mock
#
# In [15]: m = mock.Mock(spec=scarlett_os.subprocess.Subprocess)
#
# In [16]: scarlett_os.subprocess.Subprocess.__init__(m, mock.sentinel.command)
# ---------------------------------------------------------------------------
# TypeError                                 Traceback (most recent call last)
# <ipython-input-16-73c79a1e2b20> in <module>()
# ----> 1 scarlett_os.subprocess.Subprocess.__init__(m, mock.sentinel.command)
#
# /home/pi/dev/bossjones-github/scarlett_os/scarlett_os/subprocess.py in __init__(self, command, name, fork)
#      45         """Create instance of Subprocess."""
#      46
# ---> 47         GObject.GObject.__init__(self)
#      48
#      49         self.process = None
#
# TypeError: descriptor '__init__' requires a 'gi._gobject.GObject' object but received a 'Mock'
#
# In [17]:
