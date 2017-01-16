# -*- coding: utf-8 -*-

'''Utility functions and classes used for integration testing'''

import os
import sys
import time
import unittest
import unittest.mock as mock
import threading
from contextlib import contextmanager
from scarlett_os.internal.gi import GLib
from scarlett_os.internal.gi import Gio
from scarlett_os.internal.gi import GObject
from scarlett_os.internal.gi import Gst


def create_main_loop():
    '''Create isolated GLibMainloop for testing.'''
    mainloop = GLib.MainLoop()
    timed_out = False

    def quit_cb(unused):
        nonlocal timed_out  # noqa
        timed_out = True
        mainloop.quit()

    def run(timeout_seconds=5):
        source = GLib.timeout_source_new_seconds(timeout_seconds)
        source.set_callback(quit_cb)
        source.attach()
        GLib.MainLoop.run(mainloop)
        source.destroy()
        if timed_out:
            raise Exception("Timed out after %s seconds" % timeout_seconds)

    mainloop.run = run
    return mainloop
