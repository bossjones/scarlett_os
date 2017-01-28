"""Debug module using ipython."""

import sys
import signal
import logging
import os
logger = logging.getLogger(__name__)


def set_gst_grapviz_tracing(enabled=True):
    if enabled:
        os.environ[
            "GST_DEBUG_DUMP_DOT_DIR"] = "/home/pi/dev/bossjones-github/scarlett_os/_debug"  # noqa
        os.putenv('GST_DEBUG_DUMP_DIR_DIR',
                  '/home/pi/dev/bossjones-github/scarlett_os/_debug')
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

# example dump
# In [3]: dump(_p)
# obj.__bytes__ = <bound method PurePath.__bytes__ of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.__class__ = <class 'pathlib.PosixPath'>
# obj.__delattr__ = <method-wrapper '__delattr__' of PosixPath object at 0x7efeab334358>
# obj.__dir__ = <built-in method __dir__ of PosixPath object at 0x7efeab334358>
# obj.__doc__ = None
# obj.__enter__ = <bound method Path.__enter__ of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.__eq__ = <bound method PurePath.__eq__ of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.__exit__ = <bound method Path.__exit__ of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.__format__ = <built-in method __format__ of PosixPath object at 0x7efeab334358>
# obj.__ge__ = <bound method PurePath.__ge__ of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.__getattribute__ = <method-wrapper '__getattribute__' of PosixPath object at 0x7efeab334358>
# obj.__gt__ = <bound method PurePath.__gt__ of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.__hash__ = <bound method PurePath.__hash__ of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.__init__ = <method-wrapper '__init__' of PosixPath object at 0x7efeab334358>
# obj.__le__ = <bound method PurePath.__le__ of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.__lt__ = <bound method PurePath.__lt__ of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.__module__ = pathlib
# obj.__ne__ = <method-wrapper '__ne__' of PosixPath object at 0x7efeab334358>
# obj.__new__ = <function Path.__new__ at 0x7efeacd84950>
# obj.__reduce__ = <bound method PurePath.__reduce__ of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.__reduce_ex__ = <built-in method __reduce_ex__ of PosixPath object at 0x7efeab334358>
# obj.__repr__ = <bound method PurePath.__repr__ of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.__rtruediv__ = <bound method PurePath.__rtruediv__ of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.__setattr__ = <method-wrapper '__setattr__' of PosixPath object at 0x7efeab334358>
# obj.__sizeof__ = <built-in method __sizeof__ of PosixPath object at 0x7efeab334358>
# obj.__slots__ = ()
# obj.__str__ = <bound method PurePath.__str__ of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.__subclasshook__ = <built-in method __subclasshook__ of type object at 0x2883d18>
# obj.__truediv__ = <bound method PurePath.__truediv__ of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj._accessor = <pathlib._NormalAccessor object at 0x7efeacd7cc88>
# obj._closed = False
# obj._cparts = ['/', 'home', 'pi', 'dev', 'bossjones-github', 'scarlett_os', '_debug', 'generator-player.dot']
# obj._drv =
# obj._flavour = <pathlib._PosixFlavour object at 0x7efeacd7c2e8>
# obj._format_parsed_parts = <bound method PurePath._format_parsed_parts of <class 'pathlib.PosixPath'>>
# obj._from_parsed_parts = <bound method PurePath._from_parsed_parts of <class 'pathlib.PosixPath'>>
# obj._from_parts = <bound method PurePath._from_parts of <class 'pathlib.PosixPath'>>
# obj._init = <bound method Path._init of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj._make_child = <bound method PurePath._make_child of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj._make_child_relpath = <bound method Path._make_child_relpath of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj._opener = <bound method Path._opener of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj._parse_args = <bound method PurePath._parse_args of <class 'pathlib.PosixPath'>>
# obj._parts = ['/', 'home', 'pi', 'dev', 'bossjones-github', 'scarlett_os', '_debug', 'generator-player.dot']
# obj._raise_closed = <bound method Path._raise_closed of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj._raw_open = <bound method Path._raw_open of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj._root = /
# obj._str = /home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot
# obj.absolute = <bound method Path.absolute of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.anchor = /
# obj.as_posix = <bound method PurePath.as_posix of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.as_uri = <bound method PurePath.as_uri of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.chmod = <bound method Path.chmod of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.cwd = <bound method Path.cwd of <class 'pathlib.PosixPath'>>
# obj.drive =
# obj.exists = <bound method Path.exists of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.expanduser = <bound method Path.expanduser of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.glob = <bound method Path.glob of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.group = <bound method Path.group of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.home = <bound method Path.home of <class 'pathlib.PosixPath'>>
# obj.is_absolute = <bound method PurePath.is_absolute of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.is_block_device = <bound method Path.is_block_device of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.is_char_device = <bound method Path.is_char_device of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.is_dir = <bound method Path.is_dir of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.is_fifo = <bound method Path.is_fifo of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.is_file = <bound method Path.is_file of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.is_reserved = <bound method PurePath.is_reserved of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.is_socket = <bound method Path.is_socket of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.is_symlink = <bound method Path.is_symlink of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.iterdir = <bound method Path.iterdir of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.joinpath = <bound method PurePath.joinpath of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.lchmod = <bound method Path.lchmod of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.lstat = <bound method Path.lstat of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.match = <bound method PurePath.match of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.mkdir = <bound method Path.mkdir of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.name = generator-player.dot
# obj.open = <bound method Path.open of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.owner = <bound method Path.owner of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.parent = /home/pi/dev/bossjones-github/scarlett_os/_debug
# obj.parents = <PosixPath.parents>
# obj.parts = ('/', 'home', 'pi', 'dev', 'bossjones-github', 'scarlett_os', '_debug', 'generator-player.dot')
# obj.read_bytes = <bound method Path.read_bytes of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.read_text = <bound method Path.read_text of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.relative_to = <bound method PurePath.relative_to of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.rename = <bound method Path.rename of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.replace = <bound method Path.replace of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.resolve = <bound method Path.resolve of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.rglob = <bound method Path.rglob of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.rmdir = <bound method Path.rmdir of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.root = /
# obj.samefile = <bound method Path.samefile of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.stat = <bound method Path.stat of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.stem = generator-player
# obj.suffix = .dot
# obj.suffixes = ['.dot']
# obj.symlink_to = <bound method Path.symlink_to of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.touch = <bound method Path.touch of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.unlink = <bound method Path.unlink of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.with_name = <bound method PurePath.with_name of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.with_suffix = <bound method PurePath.with_suffix of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.write_bytes = <bound method Path.write_bytes of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
# obj.write_text = <bound method Path.write_text of PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot')>
