#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_integration_mpris
----------------------------------
"""

import os
import sys
import signal
import pytest
import builtins
import threading

import unittest
import unittest.mock as mock

import scarlett_os

from scarlett_os import mpris
# from scarlett_os.utility.gnome import trace
# from scarlett_os.utility.gnome import abort_on_exception
# from scarlett_os.utility.gnome import _IdleObject

# from scarlett_os import speaker

# NOTE: We can't add this here, otherwise we won't be able to mock them

import scarlett_os.exceptions

from tests import common
from pydbus import SessionBus

done = 0


def get_session_bus():
    bus = SessionBus()
    bus.own_name(name='org.scarlett')
    return bus


class TestScarlettSpeaker(unittest.TestCase):

    def __load_dbus_service(self):

      bus = get_session_bus()

      sl = mpris.ScarlettListener(bus=bus.con, path='/org/scarlett/Listener')

      pass


    def setUp(self):  # noqa: N802

        # import faulthandler
        # faulthandler.register(signal.SIGUSR2, all_threads=True)

        # from scarlett_os.internal.debugger import init_debugger
        # from scarlett_os.internal.debugger import set_gst_grapviz_tracing
        # init_debugger()
        # set_gst_grapviz_tracing()
        # # Example of how to use it
        # from pydbus import SessionBus
        # bus = SessionBus()
        # bus.own_name(name='org.scarlett')
        # sl = ScarlettListener(bus=bus.con, path='/org/scarlett/Listener')
        # loop.run()

        # def sigint_handler(*args):
        #     """Exit on Ctrl+C"""

        #     # Unregister handler, next Ctrl-C will kill app
        #     # TODO: figure out if this is really needed or not
        #     signal.signal(signal.SIGINT, signal.SIG_DFL)

        #     sl.Quit()

        # signal.signal(signal.SIGINT, sigint_handler)

        pass

    def tearDown(self):
        pass
