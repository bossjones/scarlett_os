#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_mpris
----------------------------------
"""

import os
import sys

from freezegun import freeze_time
import datetime
import unittest

# import mock
import unittest.mock as mock

from scarlett_os.commands import Command, TimeCommand, NO_OP


@freeze_time("2016-11-23")
class TestScarlettCommand(unittest.TestCase):

    def setUp(self):
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """
        pass

    # @mock.patch('scarlett_os.commands.NO_OP', '__SCARLETT_NO_OP__')
    # def test_constant_no_op(self):
    #     pass

    def test_command_check_cmd_not_tuple(self):
            self.assertEqual(Command.check_cmd('blah'), NO_OP)

    def test_get_current_time(self):
        t = TimeCommand
        with freeze_time("2016-11-23 17:34:39"):
            self.assertEqual(t.get_current_time(), 'It is now, 05:34 PM')

    def test_get_current_date(self):
        t = TimeCommand
        with freeze_time("2016-11-23 17:34:39"):
            self.assertEqual(t.get_current_date(), "Today's date is, Wednesday, November 23, 2016")

    # # source: http://stackoverflow.com/questions/23257470/how-to-mock-python-static-methods-and-class-methods
    # @mock.patch('scarlett_os.commands.Command.check_cmd')
    # def test_check_cmd(self, mock_check_cmd):
    #     mock_check_cmd.return_value = 'It is now, 05:34 PM'
    #     mock_check_cmd.assert_called()
    #     # c = Command
    #     # with freeze_time("2016-11-23 17:34:39"):
    #     #     self.assertEqual(c.check_cmd(command_tuple=(' ScarlettListener caught a command match', 'pi-response', 'what time is it',)), 'It is now, 05:34 PM')

    # @mock.patch('scarlett_os.commands.Command.check_cmd')
    # @mock.patch('scarlett_os.commands.Command')
    # def test_class(self, mock_command):
    #
    #     class NewScarlettCmd(object):
    #
    #         def check_cmd(self):
    #             return 'It is now, 05:34 PM'
    #
    #     new_cmd = NewScarlettCmd
    #     new_cmd
    #     mock_command.return_value = NewScarlettCmd
    #     self.assertEquals(check_cmd(), 'It is now, 05:34 PM')
