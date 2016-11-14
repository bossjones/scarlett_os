# -*- coding: utf-8 -*-

"""ScarlettOS compatibility."""

import itertools
import sys

from six.moves import configparser

PY2 = sys.version_info[0] == 2
PY3 = not PY2


if PY2:
    pass
elif PY3:
    import os
    import random  # NOQA
    import re
    import unicodedata
    import threading
    import subprocess  # NOQA


    map = itertools.imap if sys.version_info < (3,) else map

    import errno
    from os import environ as environ
    import pprint
    pp = pprint.PrettyPrinter(indent=4)

    from scarlett_os.internal import debugger

    import builtins
    builtins
    from urllib.parse import urlparse, urlunparse, quote_plus, unquote_plus, \
        urlsplit
    urlparse, quote_plus, unquote_plus, urlunparse, urlsplit
    from urllib.request import pathname2url, url2pathname
    pathname2url, url2pathname
    from urllib.request import urlopen, build_opener
    urlopen, build_opener
    import contextlib
    import time
    import textwrap  # NOQA
    import logging
    from functools import reduce, wraps
    import traceback

    logger = logging.getLogger(__name__)

    reduce
    from operator import floordiv
    floordiv

    xrange = range
    long = int
    unichr = chr

    text_type = str
    string_types = (str,)
    integer_types = (int,)
    number_types = (int, float)

    iteritems = lambda d: iter(d.items())  # NOQA
    itervalues = lambda d: iter(d.values())  # NOQA

    import builtins
    exec_ = getattr(builtins, "exec")

    def reraise(tp, value, tb):
        raise tp(value).with_traceback(tb)

    _FSCODING = "utf-8"
