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

from scarlett_os.subprocess import check_pid


def raise_OSError(*x, **kw):
    raise OSError('Fail')


class TestScarlettSubprocess(unittest.TestCase):

    def setUp(self):
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """
        pass

    @mock.patch("os.kill", new=mock.Mock(side_effect=OSError))
    def test_check_pid(self):
        self.assertFalse(check_pid(4353634632623))
