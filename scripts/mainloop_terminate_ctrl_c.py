#!/usr/bin/env python  # NOQA
# -*- coding: utf-8 -*-

# Proof of concept pure python implementation
# Bug: "Ctrl+C does not exit gtk app"

# source: https://bugzilla.gnome.org/show_bug.cgi?id=622084#c4
# source: https://bugzilla.gnome.org/attachment.cgi?id=238552
# source: http://stackoverflow.com/questions/16410852/keyboard-interrupt-with-with-python-gtk
# via Benjamin Berg

from gi.repository import Gtk, GLib

import signal
import sys
import os


# I tried to support multiple mainloops, which is why there these
# dictionaries exist. As it turns out there is no way to figure out
# whether to Gtk.MainLoop objects are the same apparently.
# So everything is hardcoded to None for now. GLib.MainContext is not
# even hashable.
_main_loop_quit_reason = dict()
_main_loop_quit_func = dict()


def run_mainloop(main_loop_func, quit_func, maincontext, *args, **kwargs):
    # if maincontext is None:
    #    maincontext = GLib.main_context_default()

    # TODO: Ensure that the event source is attached to this context

    # if not maincontext in _main_loop_quit_func:
    if maincontext not in _main_loop_quit_func:
        # Attach the notification FD from python
        attach_readfd(signal_notify_fd, maincontext)

        _main_loop_quit_func[maincontext] = None

    last_quit_func = _main_loop_quit_func[maincontext]

    try:
        _main_loop_quit_func[maincontext] = quit_func
        _main_loop_quit_reason[maincontext] = None

        result = main_loop_func(*args, **kwargs)
    finally:
        _main_loop_quit_func[maincontext] = last_quit_func

    # Raise any exception that may have happened
    if _main_loop_quit_reason[maincontext] is not None:
        raise _main_loop_quit_reason[maincontext]

    return result


def attach_readfd(iochannel, context):
    # This does not work currently :-(
    # Also, things are mixed up a bit with iochannel vs. FDs apparently
    # as I am getting an int back in the handler
    # if isinstance(iochannel, int):
    #    iochannel = GLib.IOChannel(iochannel)
    # source = GLib.io_create_watch(iochannel, GLib.IOCondition(GLib.IO_IN | GLib.IO_PRI))
    # source.set_callback(_glib_signal_cb, context)
    # source.set_priority(GLib.PRIORITY_HIGH)
    # source.attach(context)
    GLib.io_add_watch(iochannel, GLib.IO_IN | GLib.IO_PRI, _glib_signal_cb, context)


# Now, this is our magic exception hook. It is *magic*
# it detects whether the exception happened in our signal handler.
# The fun part is that the handler does not run properly. The mainloop
# will actually try to run it again as soon as it can (if it manages).
# We use that to clear the exception option again.
orig_excepthook = sys.excepthook


def excepthook(type, value, tb):
    frame = tb.tb_frame
    code = frame.f_code
    if code.co_name == "_glib_signal_cb":
        # We have some known parameters
        iochannel = frame.f_locals["iochannel"]
        # condition = frame.f_locals['condition']
        context = frame.f_locals["context"]

        # Reaad the event because the exception means that
        # it will be removed.
        # Note that the handler does *not* run because of the exception.
        # The next time it runs it will clear the stored exception again.
        attach_readfd(iochannel, context)

        # Store the exception for later use (ie. raise it after the mainloop
        # has quit)
        _main_loop_quit_reason[context] = value

        # Try to quit the mainloop using the attached _quit_func. If this
        # raises an exception, then just live with it.
        if context in _main_loop_quit_func:
            if _main_loop_quit_func[context] is not None:
                _main_loop_quit_func[context]()
        return

    return orig_excepthook(type, value, tb)


sys.excepthook = excepthook

# Create FDs for communication, and make them non-blocking
signal_notify_fd, signal_wakeup_fd = os.pipe()
import fcntl

fcntl.fcntl(
    signal_wakeup_fd,
    fcntl.F_SETFL,
    fcntl.fcntl(signal_wakeup_fd, fcntl.F_GETFL) | os.O_NONBLOCK,
)
fcntl.fcntl(
    signal_notify_fd,
    fcntl.F_SETFL,
    fcntl.fcntl(signal_notify_fd, fcntl.F_GETFL) | os.O_NONBLOCK,
)

signal.set_wakeup_fd(signal_wakeup_fd)


def _glib_signal_cb(iochannel, condition, context):
    # This function aborts right away with the exception that needs
    # to be handled. Because of this, it is called a second time by
    # the sysexcept hook. Which also readds it.
    # iochannel seems to be the FD, not an IOChannel object

    # Read the byte that is send by the python interpreter
    os.read(iochannel, 1)

    # If the mainloop has been quit, than this will only be
    # executed by an outer mainloop (and the exception has been
    # raised already). In general, if this executes, the mainloop
    # is executing code, so we should clear the flag again.
    _main_loop_quit_reason[context] = None

    # Keep the handler installed
    return True


#####################################################################

# If the signal is overriden in python, then KeyboardInterrupt will
# never be raised. We still need all the stuff to wake up the mainloop
# though.
#
# def sigint_handler(*args):
#    print "got sigint!!!"
#
# signal.signal(signal.SIGINT, sigint_handler)

#####################################################################

# Override GTK+ functions
def decorate_gtk_mainfunc(function):
    def decorated_function(*args, **kwargs):
        run_mainloop(function, Gtk.main_quit, None, *args, **kwargs)

    return decorated_function


# We could override Gtk.main_iteration and Gtk.main_iteration_do too,
# but that does not seem to be necessary (because they don't dispatch
# our event handler, but instead return; this means that the exception
# is raised anyways).
Gtk.main = decorate_gtk_mainfunc(Gtk.main)


def long_running_code():
    # try/except block so that the function will not be
    # removed from the mainloop
    try:
        import time

        print("sleeping")
        time.sleep(1)
    finally:
        print("done sleeping, in mainloop now")
        return True


GLib.timeout_add(2000, long_running_code)

try:
    Gtk.main()
finally:
    print("mainloop was quit")
