#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_integration_player
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
from _pytest.monkeypatch import MonkeyPatch

import scarlett_os
import scarlett_os.exceptions

from tests.integrationtests.stubs import create_main_loop

from scarlett_os import player
from scarlett_os.user import get_user_project_base_path

import imp

done = 0


# source: https://github.com/pytest-dev/pytest/issues/363
@pytest.fixture(scope="function")
def player_monkeyfunc(request):
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture(scope="function")
def player_mocker_stopall(mocker):
    "Stop previous mocks, yield mocker plugin obj, then stopall mocks again"
    print("Called [setup]: mocker.stopall()")
    mocker.stopall()
    print("Called [setup]: imp.reload(threadmanager)")
    imp.reload(player)
    yield mocker
    print("Called [teardown]: mocker.stopall()")
    mocker.stopall()
    print("Called [setup]: imp.reload(threadmanager)")
    imp.reload(player)


@pytest.mark.scarlettonly
@pytest.mark.scarlettonlyintgr
class TestScarlettPlayer(object):
    def test_ScarlettPlayer_listening(self, player_monkeyfunc, player_mocker_stopall):
        # we want to use pulsesink by default but in docker we might
        # not have a pulseaudio server running
        # test using fakesink in this usecase
        player_monkeyfunc.setattr(
            __name__ + ".player.ScarlettPlayer.DEFAULT_SINK", "fakesink"
        )

        player_data = []

        pi_listening_wav = os.path.join(
            get_user_project_base_path() + "/static/sounds", "pi-listening.wav"
        )
        # Run player
        wavefile = [pi_listening_wav]
        for path in wavefile:
            path = os.path.abspath(os.path.expanduser(path))
            with player.ScarlettPlayer(path, False, False) as f:
                player_data.append(f)

        # Test audio info
        assert player_data[0].channels == 2
        assert player_data[0].samplerate == 44100
        assert player_data[0].duration == 2.5

        # Check values of elements
        assert str(type(player_data[0].source)) == "<class '__gi__.GstURIDecodeBin'>"
        assert str(type(player_data[0].queueA)) == "<class '__gi__.GstQueue'>"
        assert str(type(player_data[0].queueB)) == "<class '__gi__.GstQueue'>"
        assert str(type(player_data[0].appsink)) == "<class '__gi__.GstAppSink'>"
        assert (
            str(type(player_data[0].audioconvert)) == "<class '__gi__.GstAudioConvert'>"
        )
        assert str(type(player_data[0].splitter)) == "<class '__gi__.GstTee'>"
        assert str(type(player_data[0].pulsesink)) == "<class '__gi__.GstFakeSink'>"

        # Means pipeline was setup correct and ran without error
        assert player_data[0].read_exc is None
        assert player_data[0].dot_exc is None
        assert player_data[0].handle_error is False

        # Test
        assert player_data[0].got_caps is True
        assert player_data[0].running is False
        assert player_data[0].finished is True
