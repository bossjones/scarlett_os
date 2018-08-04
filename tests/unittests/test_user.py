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

# source: https://github.com/YosaiProject/yosai/blob/master/test/isolated_tests/core/conf/conftest.py
# FIXME: Since we currently have an issue with mocks leaking into other tests,
# this fixture ensures that we isolate the patched object, stop mocks,
# and literally re-import modules to set environment back to normal.
# It's possible this will all get fixed when we upgrade to a later version of python past 3.5.2
@pytest.fixture(scope="function")
def user_unit_mocker_stopall(mocker):
    "Stop previous mocks, yield mocker plugin obj, then stopall mocks again"
    print("Called [setup]: mocker.stopall()")
    mocker.stopall()
    print("Called [setup]: imp.reload(user)")
    imp.reload(user)
    yield mocker
    print("Called [teardown]: mocker.stopall()")
    mocker.stopall()
    print("Called [setup]: imp.reload(user)")
    imp.reload(user)


# SOURCE: https://github.com/ansible/ansible/blob/370a7ace4b3c8ffb6187900f37499990f1b976a2/test/units/module_utils/basic/test_atomic_move.py
@pytest.fixture
def user_mocks(user_unit_mocker_stopall):
    environ = dict()
    mocks = {
        "environ": user_unit_mocker_stopall.patch(
            "scarlett_os.user.os.environ", environ
        ),
        "getlogin": user_unit_mocker_stopall.patch("scarlett_os.user.os.getlogin"),
        "getuid": user_unit_mocker_stopall.patch("scarlett_os.user.os.getuid"),
        "getpass": user_unit_mocker_stopall.patch("scarlett_os.user.getpass"),
    }

    mocks["getlogin"].return_value = "root"
    mocks["getuid"].return_value = 0
    mocks["getpass"].getuser.return_value = "root"

    mocks["environ"]["LOGNAME"] = "root"
    mocks["environ"]["USERNAME"] = "root"
    mocks["environ"]["USER"] = "root"
    mocks["environ"]["LNAME"] = "root"

    yield mocks


@pytest.mark.unittest
@pytest.mark.scarlettonly
@pytest.mark.scarlettonlyunittest
class TestUser(object):

    # pytest -s -p no:timeout -k test_get_user_name --pdb
    def test_get_user_name(self, user_mocks):
        assert scarlett_os.user.get_user_name() == "root"

    def test_get_user_home(self, user_mocks):
        assert scarlett_os.user.get_user_home() == "/root"

    def test_get_user_project_root_path(self, user_mocks):
        assert scarlett_os.user.get_user_project_root_path() == "/root/dev"

    def test_get_user_project_base_path(self, user_mocks):
        assert (
            scarlett_os.user.get_user_project_base_path()
            == "/root/dev/bossjones-github/scarlett_os"
        )


@pytest.mark.unittest
@pytest.mark.scarlettonly
@pytest.mark.scarlettonlyunittest
class TestUserOverrides(object):

    # pytest -s -p no:timeout -k test_get_user_name --pdb
    def test_get_user_name_override(self):
        assert scarlett_os.user.get_user_name("fake_user_name") == "fake_user_name"

    def test_get_user_home_override(self):
        assert (
            scarlett_os.user.get_user_home("/home/fake_user_name")
            == "/home/fake_user_name"
        )

    def test_get_user_project_root_path_override(self):

        assert (
            scarlett_os.user.get_user_project_root_path("/home/fake_user_name/dev")
            == "/home/fake_user_name/dev"
        )

    def test_get_user_project_base_path_override(self):
        assert (
            scarlett_os.user.get_user_project_base_path(
                "/home/fake_user_name/dev/bossjones-github/scarlett_os"
            )
            == "/home/fake_user_name/dev/bossjones-github/scarlett_os"
        )
