# -*- coding: utf-8 -*-

from __future__ import absolute_import
import sys
from .tools import package as ts_package
from .tools import verify as ts_verify

from scarlett_os.const import (__version__,
                               PROJECT_EMAIL,
                               PROJECT_AUTHOR)


__author__ = PROJECT_AUTHOR
__email__ = PROJECT_EMAIL

# source: timeside
ts_verify.check_python3_installed()

# Check Availability of Gstreamer python bindings
ts_package.check_gi()

# Clean-up
del ts_package
del absolute_import

# Import psutil
try:
    from psutil import __version__ as psutil_version
except ImportError:
    print('PSutil library not found. ScarlettOS cannot start.')
    sys.exit(1)
