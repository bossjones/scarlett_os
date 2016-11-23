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


# class NewDateToday(datetime.date):
#     @classmethod
#     def today(cls):
#         return cls(2010, 1, 1)
# # datetime.date = NewDateToday


# datetime.datetime

# datetime.datetime(2016, 11, 23, 17, 11, 7, 332981)
@freeze_time("2016-11-23")
class TestScarlettCommand(unittest.TestCase):

    def setUp(self):
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """
        pass

    def test_command_not_tuple(self):
        self.assertEqual(Command.check_cmd('blah'), '__SCARLETT_NO_OP__')

    def test_get_current_time(self):
        with freeze_time("2016-11-23 17:34:39"):
            self.assertEqual(TimeCommand.get_current_time(), 'It is now, 05:34 PM')

    def test_get_current_date(self):
        with freeze_time("2016-11-23 17:34:39"):
            self.assertEqual(TimeCommand.get_current_date(), "Today's date is, Wednesday, November 23, 2016")
