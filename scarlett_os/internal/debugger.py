"""Debug module using ipython."""

import sys
import signal
import logging
import os
# import getpass
logger = logging.getLogger(__name__)


def set_gst_grapviz_tracing(enabled=True):
    # current_user = getpass.getuser()
    if enabled:
        # FIXME: If this breaks, you have to use a string explicitly for it to work.
        os.environ["GST_DEBUG_DUMP_DOT_DIR"] = "/home/pi/dev/bossjones-github/scarlett_os/_debug"  # noqa
        os.putenv('GST_DEBUG_DUMP_DIR_DIR', '/home/pi/dev/bossjones-github/scarlett_os/_debug')
    else:
        if os.environ.get('GST_DEBUG_DUMP_DOT_DIR'):
            del os.environ['GST_DEBUG_DUMP_DOT_DIR']


# source: http://pyrasite.readthedocs.io/en/latest/Payloads.html
# def create_call_graph():
#     import pycallgraph
#     pycallgraph.start_trace()
#     pycallgraph.make_dot_graph('callgraph.png')

def enable_remote_debugging():
    try:
        import pystuck
        pystuck.run_server()
    except ImportError:
        logger.error("No socket opened for debugging -> please install pystuck")


# source: https://github.com/kevinseelbach/generic_utils/blob/8b5636359fd248f5635160358fa237f9333f246f/src/generic_utils/debug_utils/__init__.py
def enable_thread_dump_signal(signum=signal.SIGUSR1, dump_file=sys.stderr):
    """Turns on the ability to dump all of the threads to
    Currently this is just a wrapper around the faulthandler module
    :param signum: The OS signal to listen for and when signalled the thread dump should be outputted to `dump_file`.
        The default is the SIGUSR1 signal
    :type signum: int
    :param dump_file: The dump_file to output the threaddump to upon the signal being sent to the process.
    :type dump_file: file
    """
    # Utilities for debugging a python application/process.
    # This is not specifically related testing, but related more to
    # just debugging of code and process which could be in production.
    import faulthandler
    faulthandler.register(signum, file=dump_file, all_threads=True, chain=True)


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
        logger.error("No socket opened for debugging -> please install rfoo")


# source: http://blender.stackexchange.com/questions/1879/is-it-possible-to-dump-an-objects-properties-and-methods
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

    # Module name actually exists, but pygments loads things in a strange manner
    from pygments.lexers import PythonLexer  # pylint: disable=no-name-in-module
    from pygments.formatters import Terminal256Formatter  # pylint: disable=no-name-in-module
    from pprint import pformat
    print(highlight(pformat(obj), PythonLexer(), Terminal256Formatter()))
