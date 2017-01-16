#!/usr/bin/env python  # NOQA
# -*- coding: utf-8 -*-

"""Scarlett Reciever Module. Mainly for debugging dbus."""

import os
import sys
import time
import signal
import logging
import pprint

from scarlett_os.internal.gi import gi  # noqa
from scarlett_os.internal.gi import GLib
from scarlett_os.internal.gi import Gio
from scarlett_os.internal.gi import GObject
# from scarlett_os.internal.gi import Gst


pp = pprint.PrettyPrinter(indent=4)
logger = logging.getLogger(__name__)


def print_keyword_args(**kwargs):  # pragma: no cover
    print('--- [kargs] ---')
    if kwargs is not None:
        for key, value in kwargs.items():
            print("{} = {}".format(key, value))


def print_args(args):  # pragma: no cover
    for i, v in enumerate(args):
        print("another arg through *arg : {}".format(v))


def catchall_handler(*args, **kwargs):  # pragma: no cover
    """
    Catch all handler.
    Catch and print information about all singals.
    """
    # unpack tuple to variables ( Taken from Tasker )
    for i, v in enumerate(args):
        if isinstance(v, tuple):
            tuple_args = len(v)
            if tuple_args == 1:
                msg = v
            elif tuple_args == 2:
                msg, scarlett_sound = v
            elif tuple_args == 3:
                msg, scarlett_sound, command = v

            recieved_signals.append(v)

    print('---- Caught signal ----')

    print('--- [args] ---')
    for arg in args:
        print("another arg through *arg : {}".format(arg))

    print('--- [kargs] ---')
    if kwargs is not None:
        for key, value in kwargs.items():
            print("{} = {}".format(key, value))

    print("\n")


if __name__ == '__main__':
    if os.environ.get('SCARLETT_DEBUG_MODE'):
        import faulthandler
        faulthandler.register(signal.SIGUSR2, all_threads=True)

        from scarlett_os.internal.debugger import init_debugger
        from scarlett_os.internal.debugger import set_gst_grapviz_tracing
        init_debugger()
        set_gst_grapviz_tracing()
        # Example of how to use it

    loop = GLib.MainLoop()

    recieved_signals = []

    from pydbus import SessionBus
    bus = SessionBus()
    ss = bus.get("org.scarlett", object_path='/org/scarlett/Listener')
    time.sleep(0.5)

    # taken from tasker
    ss_failed_signal = bus.subscribe(sender=None,
                                     iface="org.scarlett.Listener",
                                     signal="SttFailedSignal",
                                     object="/org/scarlett/Listener",
                                     arg0=None,
                                     flags=0,
                                     signal_fired=catchall_handler)

    ss_rdy_signal = bus.subscribe(sender=None,
                                  iface="org.scarlett.Listener",
                                  signal="ListenerReadySignal",
                                  object="/org/scarlett/Listener",
                                  arg0=None,
                                  flags=0,
                                  signal_fired=catchall_handler)

    ss_kw_rec_signal = bus.subscribe(sender=None,
                                     iface="org.scarlett.Listener",
                                     signal="KeywordRecognizedSignal",
                                     object="/org/scarlett/Listener",
                                     arg0=None,
                                     flags=0,
                                     signal_fired=catchall_handler)

    ss_cmd_rec_signal = bus.subscribe(sender=None,
                                      iface="org.scarlett.Listener",
                                      signal="CommandRecognizedSignal",
                                      object="/org/scarlett/Listener",
                                      arg0=None,
                                      flags=0,
                                      signal_fired=catchall_handler)

    ss_cancel_signal = bus.subscribe(sender=None,
                                     iface="org.scarlett.Listener",
                                     signal="ListenerCancelSignal",
                                     object="/org/scarlett/Listener",
                                     arg0=None,
                                     flags=0,
                                     signal_fired=catchall_handler)

    ss_connect = bus.subscribe(sender=None,
                               iface="org.scarlett.Listener",
                               signal="ConnectedToListener",
                               object="/org/scarlett/Listener",
                               arg0=None,
                               flags=0,
                               signal_fired=catchall_handler)
    loop.run()

    def sigint_handler(*args):
        """Exit on Ctrl+C"""
        # Unregister handler, next Ctrl-C will kill app
        # TODO: figure out if this is really needed or not
        # signal.signal(signal.SIGINT, signal.SIG_DFL)
        ss_failed_signal.disconnect()
        ss_rdy_signal.disconnect()
        ss_kw_rec_signal.disconnect()
        ss_cmd_rec_signal.disconnect()
        ss_cancel_signal.disconnect()
        ss_connect.disconnect()
        loop.quit()

    signal.signal(signal.SIGINT, sigint_handler)
