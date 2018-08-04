#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_scarlett_os
----------------------------------

Tests for `scarlett_os` module.
"""

from contextlib import contextmanager
import importlib
import pprint
import re
import sys
import unittest

import click
from click.testing import CliRunner
import pytest

import scarlett_os
from scarlett_os.internal.gi import GLib, GObject, Gst
from scarlett_os.scripts.cli import main_group
from scarlett_os.tools import verify

ubuntu_version = verify.get_current_os()
pp = pprint.PrettyPrinter(indent=4)


@pytest.mark.unittest
@pytest.mark.scarlettonly
@pytest.mark.scarlettonlyunittest
class TestScarlett_os(object):
    def test_imports_something(self):
        assert importlib.util.find_spec("platform") is not None
        assert importlib.util.find_spec("scarlett_os.logger") is not None
        assert importlib.util.find_spec("logging") is not None
        pp.pprint(dir(scarlett_os))
        print(scarlett_os.__name__)
        print(scarlett_os.__package__)
        print(scarlett_os.__file__)

    def test_gstreamer_versions(self):
        Gst.init(None)
        pp.pprint(ubuntu_version)
        # ubuntu 16.04 says:
        # ['Linux', '4.4.0', '38', 'generic', 'x86_64', 'with', 'Ubuntu', '16.04', 'xenial']
        # travis says
        # ['Linux', '4.4.0', '38', 'generic', 'x86_64', 'with', 'debian', 'jessie', 'sid']
        # docker says:
        # ['Linux', '4.4.17', 'boot2docker', 'x86_64', 'with', 'debian', 'stretch', 'sid']

        if (
            "trusty" in ubuntu_version
            or "jessie" in ubuntu_version
            or "stretch" in ubuntu_version
        ):
            # assert GObject.pygobject_version == (3, 22, 0)
            assert GObject.pygobject_version[0] == 3
            assert GObject.pygobject_version[1] >= 22
            assert GObject.pygobject_version[2] >= 0
        else:
            # assert GObject.pygobject_version == (3, 20, 0)
            assert GObject.pygobject_version[0] == 3
            assert GObject.pygobject_version[1] >= 20
            assert GObject.pygobject_version[2] >= 0

        # Verify Gstremaer 1.8.2 or 1.8.3
        gst_version_string = Gst.version_string()
        m = re.search("(GStreamer 1.8.2|GStreamer 1.8.3)", gst_version_string)
        # If we get a string match on either of these versions then we have
        # 1.8.2/1.8.3, else None
        assert m
