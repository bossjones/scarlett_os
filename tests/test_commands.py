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

    def test_check_cmd(self):
        c = Command
        with mock.patch('scarlett_os.commands.Command.check_cmd', return_value='It is now, 05:34 PM'):
            self.assertEqual(c.check_cmd(command_tuple=(' ScarlettListener caught a command match', 'pi-response', 'what time is it',)), 'It is now, 05:34 PM')
