# -*- coding: utf-8 -*-

"""ScarlettOS compatibility."""

import itertools
import sys

# from six.moves import configparser

# PY2 = sys.version_info[0] == 2
# PY3 = not PY2

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


if PY2:
    pass
elif PY3:
    import os
    import random  # noqa
    import re
    import unicodedata
    import threading

    # NOTE: from mopidy
    import configparser  # noqa
    import queue  # noqa

    import subprocess  # noqa

    map = itertools.imap if sys.version_info < (3,) else map

    import errno
    from os import environ as environ
    import pprint
    pp = pprint.PrettyPrinter(indent=4)

    # from scarlett_os.internal import debugger

    import builtins
    builtins
    import urllib  # noqa
    from urllib.parse import urlparse, urlunparse, quote_plus, unquote_plus, \
        urlsplit
    urlparse, quote_plus, unquote_plus, urlunparse, urlsplit
    from urllib.request import pathname2url, url2pathname
    pathname2url, url2pathname
    from urllib.request import urlopen, build_opener
    urlopen, build_opener
    import contextlib
    import time
    import textwrap  # noqa
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

    # NOTE: From https://github.com/mopidy/mopidy/blob/develop/mopidy/compat.py
    input = input
    intern = sys.intern

    # NOTE: everything else missing
    # http://nipy.org/dipy/devel/python3.html
    iteritems = lambda d: iter(d.items())  # noqa
    itervalues = lambda d: iter(d.values())  # noqa

    # def itervalues(dct, **kwargs):
    #     return iter(dct.values(**kwargs))

    import builtins
    exec_ = getattr(builtins, "exec")

    def reraise(tp, value, tb):
        raise tp(value).with_traceback(tb)

    _FSCODING = "utf-8"
