#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cli
----------------------------------

Tests for `test_cli` module.
"""


from contextlib import contextmanager
import importlib
import pprint
import sys
import unittest

import click
from click.testing import CliRunner
import pytest

import scarlett_os
from scarlett_os.scripts.cli import main_group
from scarlett_os.tools import verify

ubuntu_version = verify.get_current_os()
pp = pprint.PrettyPrinter(indent=4)


# pylint: disable=C0111
# pylint: disable=R0201
# pylint: disable=C0103
@pytest.mark.scarlettonly
@pytest.mark.scarlettonlyunittest
class TestScarlettCli(object):

    def test_command_line_interface_help(self):
        runner = CliRunner()
        result = runner.invoke(main_group)
        assert result.exit_code == 0
        assert 'main_group' in result.output
        assert 'This is the command line interface to ScarlettOS' in result.output
        help_result = runner.invoke(main_group, ['--help'])
        assert help_result.exit_code == 0
        print(help_result.output)
        assert 'dbus_server|listener|tasker|check_all_services' in help_result.output
