# from __future__ import absolute_import, unicode_literals

import sys
import unittest

import pytest

import scarlett_os
from scarlett_os.compat import PY2, text_type
from scarlett_os.internal.gi import GLib, GObject, Gst
from scarlett_os.utility.gnome import escape, gdecode, unescape


class TestScarlettUtilityGnome(object):
    def test_gdecode(self):
        if PY2:
            assert isinstance(gdecode(b"foo"), text_type)
        else:
            assert isinstance(gdecode(u"foo"), text_type)

    def test_escape_empty(self):
        assert escape("") == ""

    def test_roundtrip(self):
        for s in ["foo&amp;", "<&>", "&", "&amp;", "<&testing&amp;>amp;"]:
            esc = escape(s)
            assert s != esc
            assert s == unescape(esc)

    def test_unescape_empty(self):
        assert unescape("") == ""
