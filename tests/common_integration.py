"""Test the helper method for writing tests."""
# from datetime import timedelta
import contextlib
from contextlib import contextmanager
import gc
from io import StringIO
import logging
import os
import tempfile
import threading
import unittest
import unittest.mock as mock
from unittest.mock import patch

from scarlett_os import core as s
from scarlett_os import loader
from scarlett_os.const import (
    ATTR_DISCOVERED,
    ATTR_SERVICE,
    DEVICE_DEFAULT_NAME,
    EVENT_PLATFORM_DISCOVERED,
    EVENT_STATE_CHANGED,
    EVENT_TIME_CHANGED,
    SERVER_PORT,
    STATE_OFF,
    STATE_ON,
)
from scarlett_os.internal.gi import Gio, GLib, GObject, Gst
import scarlett_os.utility.dt as date_utility
from scarlett_os.utility.unit_system import METRIC_SYSTEM
import scarlett_os.utility.yaml as yaml

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
