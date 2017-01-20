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
# from tests.integration.stubs import ProcessMonitor

import subprocess
from tests import PROJECT_ROOT

done = 0


class TestScarlettEndToEnd(object):

    def test_mpris_player_and_tasker(self, service_on_outside, service_tasker, service_receiver, get_environment):
        # use emitter to run all signal tests
        #
        # receiver_cmd = [
        #     "python3",
        #     "-m",
        #     "scarlett_os.receiver"
        # ]
        # proc = ProcessMonitor(receiver_cmd)
        # pid = proc.pid
        _environment = get_environment
        # print("[test_mpris_player_and_tasker] environment: - {}".format(_environment))

        emitter_service = None
        scarlett_root = r"{}".format(PROJECT_ROOT)

        print('[emitter_service] running ...')
        emitter_service = subprocess.Popen(
            [
                "python3",
                "-m",
                "scarlett_os.emitter",
                "-s ",
                "ready"
            ],
            env=_environment,
            stdout=sys.stdout,
            shell=True,
            cwd=scarlett_root)
        print('[emitter_service] FINISHED running ...')
        # time.sleep(0.3)

        service_receiver.wait_for_output("('  ScarlettListener is ready', 'pi-listening')")
        print('[emitter_service] killing ...')
        emitter_service.kill()
        print('[emitter_service] killed ...')

        service_receiver.terminate()

        # os.kill(pid, signal.SIGKILL)
        # proc.terminate()
        # proc = None

        # if proc:
        #         poll = proc.poll()
        #         if poll == -11:
        #             print("Process exited with Segmentation Fault")
        #         if poll != 0:
        #             print("Process exited Error Eode %s", poll)
