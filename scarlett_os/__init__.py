# -*- coding: utf-8 -*-
"""Main Module for scarlett_os."""

# For the first problem, it is proposed that parentheses be permitted to enclose multiple
# names, thus allowing Python's standard mechanisms for multi-line values to apply.
# For the second problem, it is proposed that all import statements be absolute by default
# (searching sys.path only) with special syntax (leading dots) for accessing package-relative imports.

from __future__ import absolute_import
# import os
import sys
from scarlett_os.tools import package as ts_package
from scarlett_os.tools import verify as ts_verify

from scarlett_os.const import (__version__,
                               PROJECT_EMAIL,
                               PROJECT_AUTHOR)


__author__ = PROJECT_AUTHOR
__email__ = PROJECT_EMAIL

# source: timeside
ts_verify.check_python3_installed()

# SCARLETT_ROOT_DIR = os.path.abspath(__file__)

# FIXME: I think we need to set GST_DEBUG_DUMP_DOT_DIR here before we call anything gi related. 7/3/2018
# FIXME: More proof we need to set the env vars earlier
#######################################################################################
# SOURCE: https://blogs.gnome.org/uraeus/2009/10/11/writing-code-that-does-nothing/
# I have a small question to the more python savvy people out there though. I have been trying to set a environment variable for Transmageddon in python, but so far it doesn’t seem to work. If I in the shell do:
# export GST_DEBUG_DUMP_DOT_DIR= "/tmp"
# that works fine. But if I in my python code do
# os.environ["GST_DEBUG_DUMP_DOT_DIR"] = "/tmp"
# os.putenv('GST_DEBUG_DUMP_DIR_DIR', '/tmp')
# neither of them seem to have any effect. Anyone got a clue to what I am doing wrong?
# Edit: Turns out I was setting the environment variables to late in my file, I needed to do it before import gst was called :) Thanks Edward.
#######################################################################################


# Check Availability of Gstreamer python bindings
ts_package.check_gi()

# Clean-up
del ts_package
del absolute_import

try:
    from psutil import __version__ as psutil_version
except ImportError:
    print('PSutil library not found. ScarlettOS cannot start.')
    sys.exit(1)
