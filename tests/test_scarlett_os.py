#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_scarlett_os
----------------------------------

Tests for `scarlett_os` module.
"""


import sys
import unittest
import pytest
import click
from contextlib import contextmanager
from click.testing import CliRunner

from scarlett_os import scarlett_os
from scarlett_os import cli

import platform
ubuntu_version = platform.platform().split('-')
import pprint
pp = pprint.PrettyPrinter(indent=4)


# from IPython.core.debugger import Tracer  # NOQA
# from IPython.core import ultratb
# import traceback
#
# import logging
# logger = logging.getLogger('scarlettlogger')
# # from pydbus import SessionBus
# # from pydbus.green import sleep
#
# sys.excepthook = ultratb.FormattedTB(mode='Verbose',
#                                      color_scheme='Linux',
#                                      call_pdb=True,
#                                      ostream=sys.__stdout__)

# @pytest.fixture
# def runner():
#     """
#     Click's test helper.
#     """
#     return CliRunner()


# @pytest.fixture
# def ubuntu_version():
#     """ubuntu_version."""
#     return ubuntu_version


class TestScarlett_os(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    def test_gstreamer_versions(self):
        import gi
        gi.require_version('Gst', '1.0')
        from gi.repository import GObject, Gst, GLib, Gio  # NOQA
        Gst.init(None)
        Gst.debug_set_active(True)
        Gst.debug_set_default_threshold(1)

        pp.pprint(ubuntu_version)

        if ubuntu_version[8] is 'trusty':
            assert GObject.pygobject_version == (3, 22, 0)
        else:
            assert GObject.pygobject_version == (3, 20, 0)
        assert Gst.version_string() == 'GStreamer 1.8.2'

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'scarlett_os.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        print(help_result.output)
        assert 'dbus_server|listener|tasker|check_all_services' in help_result.output


if __name__ == '__main__':
    sys.exit(unittest.main())
