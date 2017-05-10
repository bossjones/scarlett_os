# from __future__ import absolute_import, unicode_literals

import unittest
import sys
import pytest

import scarlett_os
from scarlett_os.compat import text_type, PY2
from scarlett_os.internal.gi import Gst, GLib, GObject
# from scarlett_os.utility.gnome import *

from scarlett_os.utility.gnome import gdecode, escape, unescape

# FIXME: Convert to pytest
# FIXME: 5/10/2017
class TestScarlettUtilityGnome(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gdecode(self):
        if PY2:
            self.assertTrue(isinstance(gdecode(b"foo"), text_type))
        else:
            self.assertTrue(isinstance(gdecode(u"foo"), text_type))

    def test_escape_empty(self):
        self.failUnlessEqual(escape(""), "")

    def test_roundtrip(self):
            for s in ["foo&amp;", "<&>", "&", "&amp;", "<&testing&amp;>amp;"]:
                esc = escape(s)
                self.failIfEqual(s, esc)
                self.failUnlessEqual(s, unescape(esc))

    def test_unescape_empty(self):
        self.failUnlessEqual(unescape(""), "")
