"""Test the helper method for writing tests."""
import os

import contextlib
import gc
import tempfile
import unittest
import unittest.mock as mock

# from datetime import timedelta
from unittest.mock import patch
from io import StringIO
import logging
import threading
from contextlib import contextmanager

from scarlett_os.internal.gi import GLib
from scarlett_os.internal.gi import Gio
from scarlett_os.internal.gi import GObject
from scarlett_os.internal.gi import Gst

from scarlett_os import core as s, loader
from scarlett_os.utility.unit_system import METRIC_SYSTEM
import scarlett_os.utility.dt as date_utility
import scarlett_os.utility.yaml as yaml

from scarlett_os.const import STATE_ON
from scarlett_os.const import STATE_OFF
from scarlett_os.const import DEVICE_DEFAULT_NAME
from scarlett_os.const import EVENT_TIME_CHANGED,
from scarlett_os.const import EVENT_STATE_CHANGED
from scarlett_os.const import EVENT_PLATFORM_DISCOVERED
from scarlett_os.const import ATTR_SERVICE,
from scarlett_os.const import ATTR_DISCOVERED
from scarlett_os.const import SERVER_PORT

_TEST_INSTANCE_PORT = SERVER_PORT
logger = logging.getLogger(__name__)


def create_glib_main_loop():
    mainloop = GLib.MainLoop()
    timed_out = False

    def quit_cb(unused):
        # source: http://stackoverflow.com/questions/1261875/python-nonlocal-statement
        # source: https://www.smallsurething.com/a-quick-guide-to-nonlocal-in-python-3/
        #
        # Now, by adding nonlocal timed_out to the top of quit_cb,
        # Python knows that when it sees an assignment to timed_out,
        # it should assign to the variable from the outer scope
        # instead of declaring a new variable that shadows its name.
        nonlocal timed_out
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
