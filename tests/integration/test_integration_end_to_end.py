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

# from tests.integration.stubs import create_main_loop

import subprocess
from tests import PROJECT_ROOT
import time

done = 0


# from scarlett_os.internal.gi import gi  # noqa
# from scarlett_os.internal.gi import GLib
# from scarlett_os.internal.gi import Gio
# from scarlett_os.internal.gi import GObject

from scarlett_os.internal import gi
from scarlett_os.internal.gi import GLib
from scarlett_os.internal.gi import Gio
from scarlett_os.internal.gi import GObject

import imp  # Library to help us reload our tasker module

# from scarlett_os.internal.gi import Gst
#
#
# pp = pprint.PrettyPrinter(indent=4)
# logger = logging.getLogger(__name__)
#
#
# def print_keyword_args(**kwargs):  # pragma: no cover
#     print('--- [kargs] ---')
#     if kwargs is not None:
#         for key, value in kwargs.items():
#             print("{} = {}".format(key, value))
#
#
# def print_args(args):  # pragma: no cover
#     for i, v in enumerate(args):
#         print("another arg through *arg : {}".format(v))
#
#


class TestScarlettEndToEnd(object):

    # def _connect_to_signal(self, bus, signal_name):
    #     """Uses the PathWalker to scan URIs."""
    #     mainloop = create_main_loop()
    #
    #     def done_cb(uris):  # pylint: disable=missing-docstring
    #         recieved_signals.extend(signal_name)
    #         mainloop.quit()
    #
    #     mainloop.run()
    #     mainloop.quit()

    def test_mpris_player_and_tasker(self, service_on_outside, service_tasker, service_receiver, get_environment, get_bus):

        # mock.patch.stopall()  # Stops all patches started with start()
        # imp.reload(gi)
        # imp.reload(GLib)
        # imp.reload(GObject)
        # imp.reload(Gio)

        bus = get_bus
        time.sleep(0.5)
        ss = bus.get("org.scarlett", object_path='/org/scarlett/Listener')
        time.sleep(0.5)
        recieved_signals = []
        # mainloop = create_main_loop()

        def cb(pid, status):
            self.status = status
            self.loop.quit()

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

        self.status = None
        self.loop = GLib.MainLoop()

        ss_rdy_signal = bus.subscribe(sender=None,
                                      iface="org.scarlett.Listener",
                                      signal="ListenerReadySignal",
                                      object="/org/scarlett/Listener",
                                      arg0=None,
                                      flags=0,
                                      signal_fired=catchall_handler)

        argv = [sys.executable, '-m', 'scarlett_os.emitter', '-s', 'ready']
        pid, stdin, stdout, stderr = GLib.spawn_async(
            argv,
            envp=[
                'DBUS_SESSION_BUS_ADDRESS=' + get_environment['DBUS_SESSION_BUS_ADDRESS']
            ],
            working_directory=PROJECT_ROOT,
            flags=GLib.SpawnFlags.DO_NOT_REAP_CHILD)
        pid.close()
        id = GLib.child_watch_add(GLib.PRIORITY_HIGH, pid, cb)
        assert self.loop.get_context().find_source_by_id(id).priority == GLib.PRIORITY_HIGH
        time.sleep(1)
        self.loop.run()
        print('--------- recieved_signals -----------')
        print(recieved_signals)
        print('--------- stdin -----------')
        print(stdin)
        print('--------- stdout -----------')
        print(stdout)
        print('--------- stderr -----------')
        print(stderr)
        assert self.status == 0

        # pid, stdin, stdout, stderr = GLib.spawn_async(
        #     ['sh', '-c', 'echo $TEST_VAR'], ['TEST_VAR=moo!'],
        #     flags=GLib.SpawnFlags.SEARCH_PATH, standard_output=True)

        # loop = GLib.MainLoop()
        #
        # recieved_signals = []
        #
        # from pydbus import SessionBus
        # bus = SessionBus()
        # ss = bus.get("org.scarlett", object_path='/org/scarlett/Listener')
        # time.sleep(0.5)
        #
        # # taken from tasker
        # ss_failed_signal = bus.subscribe(sender=None,
        #                                  iface="org.scarlett.Listener",
        #                                  signal="SttFailedSignal",
        #                                  object="/org/scarlett/Listener",
        #                                  arg0=None,
        #                                  flags=0,
        #                                  signal_fired=catchall_handler)
        #
        # ss_rdy_signal = bus.subscribe(sender=None,
        #                               iface="org.scarlett.Listener",
        #                               signal="ListenerReadySignal",
        #                               object="/org/scarlett/Listener",
        #                               arg0=None,
        #                               flags=0,
        #                               signal_fired=catchall_handler)
        #
        # ss_kw_rec_signal = bus.subscribe(sender=None,
        #                                  iface="org.scarlett.Listener",
        #                                  signal="KeywordRecognizedSignal",
        #                                  object="/org/scarlett/Listener",
        #                                  arg0=None,
        #                                  flags=0,
        #                                  signal_fired=catchall_handler)
        #
        # ss_cmd_rec_signal = bus.subscribe(sender=None,
        #                                   iface="org.scarlett.Listener",
        #                                   signal="CommandRecognizedSignal",
        #                                   object="/org/scarlett/Listener",
        #                                   arg0=None,
        #                                   flags=0,
        #                                   signal_fired=catchall_handler)
        #
        # ss_cancel_signal = bus.subscribe(sender=None,
        #                                  iface="org.scarlett.Listener",
        #                                  signal="ListenerCancelSignal",
        #                                  object="/org/scarlett/Listener",
        #                                  arg0=None,
        #                                  flags=0,
        #                                  signal_fired=catchall_handler)
        #
        # ss_connect = bus.subscribe(sender=None,
        #                            iface="org.scarlett.Listener",
        #                            signal="ConnectedToListener",
        #                            object="/org/scarlett/Listener",
        #                            arg0=None,
        #                            flags=0,
        #                            signal_fired=catchall_handler)
        #
        # logger.info('[receiver] RUNNING ....')
        #
        # loop.run()
        # pass
        # # use emitter to run all signal tests
        #
        # _environment = get_environment
        #
        # emitter_service = None
        # scarlett_root = r"{}".format(PROJECT_ROOT)
        #
        # print('[emitter_service] running ...')
        # emitter_service = subprocess.Popen(
        #     [
        #         "python3",
        #         "-m",
        #         "scarlett_os.emitter",
        #         "-s ",
        #         "ready"
        #     ],
        #     env=_environment,
        #     stdout=sys.stdout,
        #     shell=True,
        #     cwd=scarlett_root)
        # print('[emitter_service] FINISHED running ...')
        #
        # service_receiver.wait_for_output("('  ScarlettListener is ready', 'pi-listening')")
        # print('[emitter_service] killing ...')
        # emitter_service.kill()
        # print('[emitter_service] killed ...')
        #
        # service_receiver.terminate()
