#!/usr/bin/env python3
from __future__ import absolute_import, print_function, unicode_literals

import sys
import os


# source:
# http://blender.stackexchange.com/questions/1879/is-it-possible-to-dump-an-objects-properties-and-methods
def dump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))

def get_pprint():
    import pprint
    # global pretty print for debugging
    pp = pprint.PrettyPrinter(indent=4)
    return pp

def pprint_color(obj):
    # source: https://gist.github.com/EdwardBetts/0814484fdf7bbf808f6f
    from pygments import highlight

    # Module name actually exists, but pygments loads things in a strange
    # manner
    from pygments.lexers import PythonLexer  # pylint: disable=no-name-in-module
    from pygments.formatters import Terminal256Formatter  # pylint: disable=no-name-in-module
    from pprint import pformat
    print(highlight(pformat(obj), PythonLexer(), Terminal256Formatter()))

home = os.path.expanduser('~')
sys.path.insert(0, os.path.join(home, '.cache/fakegir'))

import gi
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gst
from gi.repository import Gio

import pdb
pdb.set_trace()

print(sys.path)
