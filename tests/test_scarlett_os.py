#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_scarlett_os
----------------------------------

Tests for `scarlett_os` module.
"""


import sys
import unittest
from contextlib import contextmanager
from click.testing import CliRunner

from scarlett_os import scarlett_os
from scarlett_os import cli



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
        from gi.repository import GObject
        from gi.repository import Gst
        from gi.repository import GLib
        from gi.repository import Gio

        assert GObject.pygobject_version == (3, 20, 0)
        assert Gst.version_string() == 'GStreamer 1.8.2'

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'scarlett_os.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output


if __name__ == '__main__':
    sys.exit(unittest.main())
