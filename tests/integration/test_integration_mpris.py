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


class TestScarlettSpeaker(object):

    def test_bus_works(self, scarlett_os_interface):
        bus = scarlett_os_interface
        assert type(bus) == pydbus.bus.Bus

    def test_mpris_methods_exist(self, service_on_outside, get_dbus_proxy_obj_helper):  # noqa
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

        for _method in look_for_methods_list:
            assert _method in proxy_methods_list


# class TestScarlettSpeaker(unittest.TestCase):

    # def __load_dbus_service(self):

    #   bus = get_session_bus()

    #   sl = mpris.ScarlettListener(bus=bus.con, path='/org/scarlett/Listener')

    #   pass

