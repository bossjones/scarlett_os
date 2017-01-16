#!/usr/bin/env python3  # NOQA
# -*- coding: utf-8 -*-

"""Scarlett Emitter Module. Mainly for debugging dbus."""

import os
import sys
import time

SCARLETT_DEBUG = True

import argparse
import pprint
pp = pprint.PrettyPrinter(indent=4)

from scarlett_os.internal.gi import gi  # noqa

valid_signals = ['failed',
                 'ready',
                 'kw-rec',
                 'cancel',
                 'connect',
                 'cmd-rec']


import logging
logger = logging.getLogger(__name__)


def main(ss, args):  # pragma: no cover
    if args.signal == 'failed':
        ss.emitSttFailedSignal()

    if args.signal == 'ready':
        ss.emitListenerReadySignal()

    if args.signal == 'kw-rec':
        ss.emitKeywordRecognizedSignal()

    if args.signal == 'cmd-rec':
        ss.emitCommandRecognizedSignal('what time is it')

    if args.signal == 'cancel':
        ss.emitListenerCancelSignal()

    if args.signal == 'connect':
        ss.emitConnectedToListener('ScarlettEmitter')

if __name__ == '__main__':
    if os.environ.get('SCARLETT_DEBUG_MODE'):
        import faulthandler
        faulthandler.register(signal.SIGUSR2, all_threads=True)

        from scarlett_os.internal.debugger import init_debugger
        from scarlett_os.internal.debugger import set_gst_grapviz_tracing
        init_debugger()
        set_gst_grapviz_tracing()
        # Example of how to use it

    from pydbus import SessionBus
    bus = SessionBus()
    ss = bus.get("org.scarlett", object_path='/org/scarlett/Listener')
    time.sleep(0.5)

    parser = argparse.ArgumentParser(description='Test emit signal.')
    parser.add_argument('-s',
                        '--signal',
                        help='signal to carry out.  Can be one of:\n'
                             'failed\n'
                             'ready\n'
                             'kw-rec\n'
                             'cancel\n'
                             'connect\n'
                             'cmd-rec',
                        choices=valid_signals)

    args = parser.parse_args()

    main(ss, args)
