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

from tests.integration.stubs import create_main_loop

import time

done = 0


class TestScarlettSpeaker(object):


    # @xfail(reason="Still getting 'assert None == 0' instead of 'assert self.status == 0'")
    @pytest.mark.flaky(reruns=5)
    def test_mpris_methods_exist(self, service_on_outside, get_bus):  # noqa
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

        # Return dbus obj
        bus = get_bus

        # Sleep to give time for connection to be established
        time.sleep(1)

        # Return dbus proxy object
        scarlett_speaker_proxy = bus.get("org.scarlett", object_path='/org/scarlett/Listener')

        # wait till we get proxy object
        time.sleep(0.5)

        proxy_methods_list = dir(scarlett_speaker_proxy)

        # all dbus methos exists
        for _method in look_for_methods_list:
            assert _method in proxy_methods_list


# class PathWalkerTest(unittest.TestCase):
#     """Tests for the `PathWalker` class."""

#     def _scan(self, uris):
#         """Uses the PathWalker to scan URIs."""
#         mainloop = create_main_loop()
#         received_uris = []

#         def done_cb(uris):  # pylint: disable=missing-docstring
#             received_uris.extend(uris)
#             mainloop.quit()
#         walker = PathWalker(uris, done_cb)
#         walker.run()
#         mainloop.run()
#         return received_uris

#     def test_scanning(self):
#         """Checks the scanning of the URIs."""
#         valid_uri = get_sample_uri("tears_of_steel.webm")
#         uris = self._scan([valid_uri,
#                            get_sample_uri("missing.webm"),
#                            "http://pitivi.org/very_real.webm"])
#         self.assertEqual(len(uris), 1, uris)
#         self.assertIn(valid_uri, uris)

    def test_mpris_catchall_signal(self, service_on_outside, get_dbus_proxy_obj_helper):  # noqa
        # source: https://github.com/stylesuxx/python-dbus-examples/blob/master/receiver.py

        recieved_signals = []
        ############################################################################
        # EXAMPLE [ready signal]
        # another arg through *arg : :1.0
        # another arg through *arg : /org/scarlett/Listener
        # another arg through *arg : org.scarlett.Listener
        # another arg through *arg : ListenerReadySignal
        # another arg through *arg : ('  ScarlettListener is ready', 'pi-listening')
        ############################################################################

        #############################################################################
        # EXAMPLE [failed]
        # another arg through *arg : :1.0
        # another arg through *arg : /org/scarlett/Listener
        # another arg through *arg : org.scarlett.Listener
        # another arg through *arg : SttFailedSignal
        # another arg through *arg : ('  ScarlettListener hit Max STT failures', 'pi-response2')
        #############################################################################

        #############################################################################
        # EXAMPLE [listener]
        # another arg through *arg : :1.0
        # another arg through *arg : /org/scarlett/Listener
        # another arg through *arg : org.scarlett.Listener
        # another arg through *arg : KeywordRecognizedSignal
        # another arg through *arg : ('  ScarlettListener caught a keyword match', 'pi-listening')
        #############################################################################

        ##############################################################################
        # EXAMPLE [command]
        # another arg through *arg : :1.0
        # another arg through *arg : /org/scarlett/Listener
        # another arg through *arg : org.scarlett.Listener
        # another arg through *arg : CommandRecognizedSignal
        # another arg through *arg : ('  ScarlettListener caught a command match', 'pi-response', 'what time is it')
        ##############################################################################

        ###############################################################################
        # EXAMPLE [cancel]
        # another arg through *arg : :1.0
        # another arg through *arg : /org/scarlett/Listener
        # another arg through *arg : org.scarlett.Listener
        # another arg through *arg : ListenerCancelSignal
        # another arg through *arg : ('  ScarlettListener cancel speech Recognition', 'pi-cancel')
        ###############################################################################

        ################################################################################
        # EXAMPLE [connect]
        # another arg through *arg : :1.0
        # another arg through *arg : /org/scarlett/Listener
        # another arg through *arg : org.scarlett.Listener
        # another arg through *arg : ConnectedToListener
        # another arg through *arg : ('ScarlettEmitter',)
        ################################################################################

        # def catchall_handler(*args, **kwargs):
        #     """Catch all handler.
        #     Catch and print information about all singals.
        #     """
        #     print('---- Caught signal ----')
        #     print('%s:%s\n' % (kwargs['dbus_interface'], kwargs['member']))

        #     print('Arguments:')
        #     for arg in args:
        #         print '* %s' % str(arg)

        #     print("\n")

        #     recieved_signals.append()

        def _subscribe_to_dbus():
            pass

        # taken from tasker
        # ss_failed_signal = bus.subscribe(sender=None,
        #                                  iface="org.scarlett.Listener",
        #                                  signal="SttFailedSignal",
        #                                  object="/org/scarlett/Listener",
        #                                  arg0=None,
        #                                  flags=0,
        #                                  signal_fired=player_cb)

        # ss_rdy_signal = bus.subscribe(sender=None,
        #                               iface="org.scarlett.Listener",
        #                               signal="ListenerReadySignal",
        #                               object="/org/scarlett/Listener",
        #                               arg0=None,
        #                               flags=0,
        #                               signal_fired=player_cb)

        # ss_kw_rec_signal = bus.subscribe(sender=None,
        #                                  iface="org.scarlett.Listener",
        #                                  signal="KeywordRecognizedSignal",
        #                                  object="/org/scarlett/Listener",
        #                                  arg0=None,
        #                                  flags=0,
        #                                  signal_fired=player_cb)

        # ss_cmd_rec_signal = bus.subscribe(sender=None,
        #                                   iface="org.scarlett.Listener",
        #                                   signal="CommandRecognizedSignal",
        #                                   object="/org/scarlett/Listener",
        #                                   arg0=None,
        #                                   flags=0,
        #                                   signal_fired=command_cb)

        # ss_cancel_signal = bus.subscribe(sender=None,
        #                                  iface="org.scarlett.Listener",
        #                                  signal="ListenerCancelSignal",
        #                                  object="/org/scarlett/Listener",
        #                                  arg0=None,
        #                                  flags=0,
        #                                  signal_fired=player_cb)

        # pp.pprint((ss_failed_signal,
        #            ss_rdy_signal,
        #            ss_kw_rec_signal,
        #            ss_cmd_rec_signal,
        #            ss_cancel_signal))

        # logger.debug("ss_failed_signal: {}".format(ss_failed_signal))
        # logger.debug("ss_rdy_signal: {}".format(ss_rdy_signal))
        # logger.debug("ss_kw_rec_signal: {}".format(ss_kw_rec_signal))
        # logger.debug("ss_cmd_rec_signal: {}".format(ss_cmd_rec_signal))
        # logger.debug("ss_cancel_signal: {}".format(ss_cancel_signal))

        # ss.emitConnectedToListener('ScarlettTasker')

        # loop.run()
        pass


# class TestScarlettSpeaker(unittest.TestCase):

    # def __load_dbus_service(self):

    #   bus = get_session_bus()

    #   sl = mpris.ScarlettListener(bus=bus.con, path='/org/scarlett/Listener')

    #   pass
