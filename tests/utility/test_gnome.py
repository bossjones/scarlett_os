from __future__ import absolute_import, unicode_literals

import sys
import unittest
import pytest

import scarlett_os
from scarlett_os.compat import text_type, PY2
from scarlett_os.internal.gi import Gst, GLib, GObject
# from scarlett_os.utility.gnome import *

from scarlett_os.utility import gnome


class TestScarlettUtilityGnome(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gdecode(self):
        if PY2:
            self.assertTrue(isinstance(gnome.gdecode(b"foo"), text_type))
        else:
            self.assertTrue(isinstance(gnome.gdecode(u"foo"), text_type))
