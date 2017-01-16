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

import pydbus
import scarlett_os
import scarlett_os.exceptions

done = 0

# NOTE: example of testing dbus send on commandline
# pi@e17ba21a9d2b:~/dev/bossjones-github/scarlett_os$ dbus-send \
# > --session \
# > --print-reply \
# > --dest=org.scarlett \
# > /org/scarlett/Listener \
# > org.scarlett.Listener1.emitConnectedToListener \
# > string:"ScarlettEmitter"
# method return time=1484522999.087256 sender=:1.1 -> destination=:1.12 serial=12 reply_serial=2
#    string " ScarlettEmitter is connected to ScarlettListener"
# pi@e17ba21a9d2b:~/dev/bossjones-github/scarlett_os$

# NOTE: THIS WORKS
# dbus-send --session --print-reply --dest=org.scarlett /org/scarlett/Listener org.scarlett.Listener1.emitConnectedToListener string:"ScarlettEmitter"

# NOTE: We can use this instead of dbus-send
# [FIXME]
# pi@e17ba21a9d2b:~/dev/bossjones-github/scarlett_os$ python3 -m scarlett_os.emitter --signal=ready
# ready
# pi@e17ba21a9d2b:~/dev/bossjones-github/scarlett_os$
#
class TestScarlettSpeaker(object):

    def test_bus_works(self, scarlett_os_interface):
        bus = scarlett_os_interface
        assert type(bus) == pydbus.bus.Bus

    def test_mpris_methods_exist(self, service_on_outside, get_dbus_proxy_obj_helper):  # noqa
        # NOTE: Technically these are both methods and signals
        look_for_methods_list = ['CanQuit',
                                 'CanRaise',
                                 'CommandRecognizedSignal',
                                 'ConnectedToListener',
                                 'DesktopEntry',
                                 'Fullscreen',
                                 'Get',
                                 'GetAll',
                                 'HasTrackList',
                                 'Identity',
                                 'Introspect',
                                 'KeywordRecognizedSignal',
                                 'ListenerCancelSignal',
                                 'ListenerReadySignal',
                                 'Quit',
                                 'Set',
                                 'SttFailedSignal',
                                 'emitCommandRecognizedSignal',
                                 'emitConnectedToListener',
                                 'emitKeywordRecognizedSignal',
                                 'emitListenerCancelSignal',
                                 'emitListenerMessage',
                                 'emitListenerReadySignal',
                                 'emitSttFailedSignal',
                                 'onCommandRecognizedSignal',
                                 'onConnectedToListener',
                                 'onKeywordRecognizedSignal',
                                 'onListenerCancelSignal',
                                 'onListenerReadySignal',
                                 'onSttFailedSignal']

        scarlett_speaker_proxy = get_dbus_proxy_obj_helper
        proxy_methods_list = dir(scarlett_speaker_proxy)

        # all dbus methos exists
        for _method in look_for_methods_list:
            assert _method in proxy_methods_list


    def test_mpris_catchall_signal(self, service_on_outside, get_dbus_proxy_obj_helper):  # noqa
        # source: https://github.com/stylesuxx/python-dbus-examples/blob/master/receiver.py
        pass


# class TestScarlettSpeaker(unittest.TestCase):

    # def __load_dbus_service(self):

    #   bus = get_session_bus()

    #   sl = mpris.ScarlettListener(bus=bus.con, path='/org/scarlett/Listener')

    #   pass

