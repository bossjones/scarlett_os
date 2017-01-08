# -*- coding: utf-8 -*-

"""ScarlettOS Gnome utility functions."""

from __future__ import with_statement, division

from scarlett_os.compat import PY2, text_type, urlparse  # noqa
from scarlett_os.internal.gi import GObject, Gst, GLib, gi, _gst_available
from scarlett_os.exceptions import MainRunnerError, MainRunnerAbortedError, DecodeError, NoBackendError


import sys
import os
import contextlib
import threading
import traceback
import time
from functools import wraps

import logging
logger = logging.getLogger(__name__)


# source: https://github.com/mopidy/mopidy/blob/develop/mopidy/audio/utils.py
class Signals(object):
    """Helper for tracking gobject signal registrations"""
    def __init__(self):
        self._ids = {}

    def connect(self, element, event, func, *args):
        """Connect a function + args to signal event on an element.

        Each event may only be handled by one callback in this implementation.
        """
        assert (element, event) not in self._ids
        self._ids[(element, event)] = element.connect(event, func, *args)

    def disconnect(self, element, event):
        """Disconnect whatever handler we have for an element+event pair.

        Does nothing it the handler has already been removed.
        """
        signal_id = self._ids.pop((element, event), None)
        if signal_id is not None:
            element.disconnect(signal_id)

    def clear(self):
        """Clear all registered signal handlers."""
        for element, event in self._ids.keys():
            element.disconnect(self._ids.pop((element, event)))

########################################################################################################################
# START - SOURCE: https://github.com/quodlibet/quodlibet/blob/master/quodlibet/quodlibet/util/__init__.py
########################################################################################################################


def get_connected_audio_devices():
    devices = {}
    dm = Gst.DeviceMonitor()
    dm.start()
    for device in dm.get_devices():
        device_class = device.get_device_class()
        props = device.get_properties()
        element = device.create_element(None)
        type_name = element.get_factory().get_name()
        device_name = element.props.device
        print("%s device=%r" % (type_name, device_name))
    dm.stop()

if PY2:
    def gdecode(s):  # noqa
        """Returns unicode for the glib text type"""

        assert isinstance(s, bytes)
        return s.decode("utf-8")
else:
    def gdecode(s):  # noqa
        """Returns unicode for the glib text type"""

        assert isinstance(s, text_type)
        return s


def escape(str):
    """Escape a string in a manner suitable for XML/Pango."""
    return str.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def unescape(str):
    """Unescape a string in a manner suitable for XML/Pango."""
    return str.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def spawn(argv, stdout=False):
    """Asynchronously run a program. argv[0] is the executable name, which
    must be fully qualified or in the path. If stdout is True, return
    a file object corresponding to the child's standard output; otherwise,
    return the child's process ID.

    argv must be strictly str objects to avoid encoding confusion.
    """

    types = map(type, argv)
    if not (min(types) == max(types) == str):
        raise TypeError("executables and arguments must be str objects")
    logger.debug("Running %r" % " ".join(argv))
    args = GLib.spawn_async(argv=argv, flags=GLib.SpawnFlags.SEARCH_PATH,
                            standard_output=stdout)

    if stdout:
        return os.fdopen(args[2])
    else:
        return args[0]


def uri_is_valid(uri):
    return bool(urlparse(uri)[0])


class DeferredSignal(object):
    """A wrapper for connecting functions to signals.

    Some signals may fire hundreds of times, but only require processing
    once per group. This class pushes the call to the mainloop at idle
    priority and prevents multiple calls from being inserted in the
    mainloop at a time, greatly improving responsiveness in some places.

    When the target function is finally called, the arguments passed
    are the last arguments passed to DeferredSignal.

    `priority` defaults to GLib.PRIORITY_DEFAULT

    If `owner` is given, it will not call the target after the owner is
    destroyed.

    Example usage:

    def func(widget, user_arg):
        pass
    widget.connect('signal', DeferredSignal(func, owner=widget), user_arg)
    """

    def __init__(self, func, timeout=None, owner=None, priority=None):
        """Timeout in milliseconds"""

        self.func = func
        self.dirty = False
        self.args = None

        if owner:
            def destroy_cb(owner):
                self.abort()
            owner.connect("destroy", destroy_cb)

        if priority is None:
            priority = GLib.PRIORITY_DEFAULT

        if timeout is None:
            self.do_idle_add = lambda f: GLib.idle_add(f, priority=priority)
        else:
            self.do_idle_add = lambda f: GLib.timeout_add(
                timeout, f, priority=priority)

    @property
    def __self__(self):
        return self.func.__self__

    @property
    def __code__(self):
        return self.func.__code__

    @property
    def __closure__(self):
        return self.func.__closure__

    def abort(self):
        """Abort any queued up calls.

        Can still be reused afterwards.
        """

        if self.dirty:
            GLib.source_remove(self._id)
            self.dirty = False
            self.args = None

    def __call__(self, *args):
        self.args = args
        if not self.dirty:
            self.dirty = True
            self._id = self.do_idle_add(self._wrap)

    def _wrap(self):
        self.func(*self.args)
        self.dirty = False
        self.args = None
        return False


def connect_obj(this, detailed_signal, handler, that, *args, **kwargs):
    """A wrapper for connect() that has the same interface as connect_object().
    Used as a temp solution to get rid of connect_object() calls which may
    be changed to match the C version more closely in the future.

    https://git.gnome.org/browse/pygobject/commit/?id=86fb12b3e9b75

    While it's not clear if switching to weak references will break anything,
    we mainly used this for adjusting the callback signature. So using
    connect() behind the scenes will keep things working as they are now.
    """

    def wrap(this, *args):
        return handler(that, *args)

    return this.connect(detailed_signal, wrap, *args, **kwargs)


def _connect_destroy(sender, func, detailed_signal, handler, *args, **kwargs):
    """Connect a bound method to a foreign object signal and disconnect
    if the object the method is bound to emits destroy (Gtk.Widget subclass).

    Also works if the handler is a nested function in a method and
    references the method's bound object.

    This solves the problem that the sender holds a strong reference
    to the bound method and the bound to object doesn't get GCed.
    """

    if hasattr(handler, "__self__"):
        obj = handler.__self__
    else:
        # XXX: get the "self" var of the enclosing scope.
        # Used for nested functions which ref the object but aren't methods.
        # In case they don't ref "self" normal connect() should be used anyway.
        index = handler.__code__.co_freevars.index("self")
        obj = handler.__closure__[index].cell_contents

    assert obj is not sender

    handler_id = func(detailed_signal, handler, *args, **kwargs)

    def disconnect_cb(*args):
        sender.disconnect(handler_id)

    obj.connect('destroy', disconnect_cb)
    return handler_id


def connect_destroy(sender, *args, **kwargs):
    return _connect_destroy(sender, sender.connect, *args, **kwargs)


def connect_after_destroy(sender, *args, **kwargs):
    return _connect_destroy(sender, sender.connect_after, *args, **kwargs)


def gi_require_versions(name, versions):
    """Like gi.require_version, but will take a list of versions.

    Returns the required version or raises ValueError.
    """

    assert versions

    error = None
    for version in versions:
        try:
            gi.require_version(name, version)
        except ValueError as e:
            error = e
        else:
            return version
    else:
        raise error


def is_main_thread():
    """If the calling thread is the main one"""

    return threading.current_thread().name == "MainThread"


class MainRunner(object):
    """Schedule a function call in the main loop from a
    worker thread and wait for the result.

    Make sure to call abort() before the main loop gets destroyed, otherwise
    the worker thread may block forever in call().
    """

    def __init__(self):
        self._source_id = None
        self._call_id = None
        self._lock = threading.Lock()
        self._cond = threading.Condition(self._lock)
        self._return = None
        self._error = None
        self._aborted = False

    def _run(self, func, *args, **kwargs):
        try:
            self._return = func(*args, **kwargs)
        except Exception as e:
            self._error = MainRunnerError(e)

    def _idle_run(self, call_id, call_event, func, *args, **kwargs):
        call_event.set()
        with self._lock:
            # In case a timeout happened but this got still
            # scheduled, this could be called after call() returns;
            # Compare to the current call id and do nothing if it isn't ours
            if call_id is not self._call_id:
                return False
            try:
                self._run(func, *args, **kwargs)
            finally:
                self._source_id = None
                self._cond.notify()
                return False

    def abort(self):
        """After this call returns no function will be executed anymore
        and a currently blocking call will fail with MainRunnerAbortedError.

        Can be called multiple times and can not fail.
        call() will always fail after this was called.
        """

        with self._lock:
            if self._aborted:
                return
            if self._source_id is not None:
                GLib.source_remove(self._source_id)
                self._source_id = None
            self._aborted = True
            self._call_id = None
            self._error = MainRunnerAbortedError("aborted")
            self._cond.notify()

    def call(self, func, *args, **kwargs):
        """Runs the function in the main loop and blocks until
        it is finshed or abort() was called. In case this is called
        from the main loop the function gets executed immediately.

        The priority kwargs defines the event source priority and will
        not be passed to func.

        In case a timeout kwarg is given the call will raise
        MainRunnerTimeoutError in case the function hasn't been scheduled
        (doesn't mean returned) until that time. timeout is a float in seconds.

        Can raise MainRunnerError in case the function raises an exception.
        Raises MainRunnerAbortedError in case the runner was aborted.
        Raises MainRunnerTimeoutError in case the timeout was reached.
        """

        with self._lock:
            if self._aborted:
                raise self._error
            self._error = None
            # XXX: ideally this should be GLib.MainContext.default().is_owner()
            # but that's not available in older pygobject
            if is_main_thread():
                kwargs.pop("priority", None)
                self._run(func, *args, **kwargs)
            else:
                assert self._source_id is None
                assert self._call_id is None
                timeout = kwargs.pop("timeout", None)
                call_event = threading.Event()
                self._call_id = object()
                self._source_id = GLib.idle_add(
                    self._idle_run, self._call_id, call_event,
                    func, *args, **kwargs)
                # only wait for the result if we are sure it got scheduled
                if call_event.wait(timeout):
                    self._cond.wait()
                self._call_id = None
                if self._source_id is not None:
                    GLib.source_remove(self._source_id)
                    self._source_id = None
                    raise MainRunnerTimeoutError("timeout: %r" % timeout)
            if self._error is not None:
                raise self._error
            return self._return


def re_escape(string, BAD="/.^$*+-?{,\\[]|()<>#=!:"):
    """A re.escape which also works with unicode"""

    needs_escape = lambda c: (c in BAD and "\\" + c) or c  # noqa
    return type(string)().join(map(needs_escape, string))


class _IdleObject(GObject.GObject):
    """
    Override GObject.GObject to always emit signals in the main thread
    by emmitting on an idle handler
    """

    # @trace
    def __init__(self):
        GObject.GObject.__init__(self)

    # @trace
    def emit(self, *args):
        GObject.idle_add(GObject.GObject.emit, self, *args)


# source: https://github.com/hpcgam/dicomimport/blob/1f265b1a5c9e631a536333633893ab525da87f16/doc-dcm/SAMPLEZ/nostaples/utils/scanning.py  # noqa
def abort_on_exception(func):  # noqa
    """
    This function decorator wraps the run() method of a thread
    so that any exceptions in that thread will be logged and
    cause the threads 'abort' signal to be emitted with the exception
    as an argument.  This way all exception handling can occur
    on the main thread.

    Note that the entire sys.exc_info() tuple is passed out, this
    allows the current traceback to be used in the other thread.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            thread_object = args[0]
            exc_type, exc_value, exc_tb = exc_info = sys.exc_info()
            filename, line_num, func_name, text = traceback.extract_tb(exc_tb)[-1]
            logger.error('Exception Thrown from [%s] on line [%s] via function [%s]' % (filename, line_num, func_name))
            logger.error('Exception type %s: %s' % (e.__class__.__name__, e.message))
            # NOTE: ORIGINAL # thread_object.log.error('Exception type %s: %s' % (e.__class__.__name__, e.message))
            thread_object.emit('aborted', exc_info)
    return wrapper


def trace(func):
    """Tracing wrapper to log when function enter/exit happens.
    :param func: Function to wrap
    :type func: callable
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug('Start {!r}'. format(func.__name__))
        result = func(*args, **kwargs)
        logger.debug('End {!r}'. format(func.__name__))
        return result
    return wrapper


@contextlib.contextmanager
def time_logger(name, level=logging.DEBUG):
    """Time logger context manager. Shows how long it takes to run a particular method"""
    start = time.time()
    yield
    logger.log(level, '%s took %dms', name, (time.time() - start) * 1000)


def glib2fsnative(path):
    """Convert glib to native filesystem format"""
    assert isinstance(path, bytes)
    return path


def fsnative2glib(path):
    """Convert file system to native glib format"""
    assert isinstance(path, bytes)
    return path

fsnative2bytes = fsnative2glib

bytes2fsnative = glib2fsnative


def audio_open(path):
    """Open an audio file using a library that is available on this
    system.
    """
    # GStreamer.
    if _gst_available():
        from . import generator_player
        try:
            return generator_player.ScarlettPlayer(path)
            # return gstdec.ScarlettPlayer(path)
        except DecodeError:
            pass

    # All backends failed!
    raise NoBackendError()
