#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_commands
----------------------------------
"""

import datetime
import imp
import os
import sys
import unittest
import unittest.mock as mock

from freezegun import freeze_time
import pytest

import scarlett_os
from scarlett_os import commands


# from scarlett_os.commands import Command, TimeCommand, NO_OP


# source: https://github.com/YosaiProject/yosai/blob/master/test/isolated_tests/core/conf/conftest.py
@pytest.fixture(scope="function")
def commands_unit_mocker_stopall(mocker):
    "Stop previous mocks, yield mocker plugin obj, then stopall mocks again"
    print("Called [setup]: mocker.stopall()")
    mocker.stopall()
    print("Called [setup]: imp.reload(commands)")
    imp.reload(commands)
    yield mocker
    print("Called [teardown]: mocker.stopall()")
    mocker.stopall()
    print("Called [setup]: imp.reload(commands)")
    imp.reload(commands)


@pytest.mark.scarlettonly
@pytest.mark.scarlettonlyunittest
@freeze_time("2016-11-23")
class TestScarlettCommand(object):
    def test_command_check_cmd_not_tuple(self):
        assert commands.Command.check_cmd("blah") == commands.NO_OP

    def test_get_current_time(self):
        # t = TimeCommand
        with freeze_time("2016-11-23 17:34:39"):
            assert commands.TimeCommand.get_current_time() == "It is now, 05:34 PM"

    def test_get_current_date(self):
        # t = TimeCommand
        with freeze_time("2016-11-23 17:34:39"):
            assert (
                commands.TimeCommand.get_current_date()
                == "Today's date is, Wednesday, November 23, 2016"
            )

    def test_check_cmd(self, commands_unit_mocker_stopall):
        # c = Command
        temp_mocker = commands_unit_mocker_stopall

        mock_check_cmd = temp_mocker.MagicMock(
            name="mock_check_cmd", return_value="It is now, 05:34 PM"
        )

        temp_mocker.patch("scarlett_os.commands.Command.check_cmd", mock_check_cmd)

        # with mock.patch('scarlett_os.commands.Command.check_cmd', return_value='It is now, 05:34 PM'):
        assert (
            commands.Command.check_cmd(
                command_tuple=(
                    " ScarlettListener caught a command match",
                    "pi-response",
                    "what time is it",
                )
            )
            == "It is now, 05:34 PM"
        )
