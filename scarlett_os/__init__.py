# -*- coding: utf-8 -*-
"""Main Module for scarlett_os."""

# For the first problem, it is proposed that parentheses be permitted to enclose multiple
# names, thus allowing Python's standard mechanisms for multi-line values to apply.
# For the second problem, it is proposed that all import statements be absolute by default
# (searching sys.path only) with special syntax (leading dots) for accessing package-relative imports.

from __future__ import absolute_import
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

# FIXME: I think we need to set GST_DEBUG_DUMP_DOT_DIR here before we call anything gi related. 7/3/2018

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
