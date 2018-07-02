#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_user
----------------------------------

Tests for `scarlett_os` module.
"""

# import ipdb

# import mock
import builtins
import imp
import os
import signal
import sys
import unittest
import unittest.mock as mock

# import threading
import pytest

import scarlett_os
from scarlett_os import user  # Module with our thing to test

@pytest.mark.unittest
@pytest.mark.scarlettonly
@pytest.mark.scarlettonlyunittest
class TestUser(object):

    # pytest -s -p no:timeout -k test_get_user_name --pdb
    def test_get_user_name(self, mocker):

        mocker.stopall()

        # mock
        os_environ_mock = mocker.MagicMock(name=__name__ + "_os_environ_mock")
        expected_name = 'fake_user_name'
        os_environ_mock.get.return_value = expected_name

        mocker.patch('scarlett_os.user.os.environ', os_environ_mock)

        assert scarlett_os.user.get_user_name() == "fake_user_name"

        mocker.stopall()
