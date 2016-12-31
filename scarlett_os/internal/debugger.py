"""Debug module using ipython."""

# from __future__ import with_statement, division

import logging
logger = logging.getLogger(__name__)


def init_debugger():
    import sys

    from IPython.core.debugger import Tracer  # noqa
    from IPython.core import ultratb

    sys.excepthook = ultratb.FormattedTB(mode='Verbose',
                                         color_scheme='Linux',
                                         call_pdb=True,
                                         ostream=sys.__stdout__)

# http://stackoverflow.com/questions/582056/getting-list-of-parameter-names-inside-python-function
# https://docs.python.org/3/library/inspect.html


def inspect_scarlett_module(scarlett_module):
    # func = lambda x, y: (x, y)
    num_args = scarlett_module.__code__.co_argcount
    name_args = scarlett_module.__code__.co_varnames
    pass


def init_rconsole_server():
    try:
        from rfoo.utils import rconsole
        rconsole.spawn_server()
    except ImportError:
        logger.debug("No socket opened for debugging -> please install rfoo")
