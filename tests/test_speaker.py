#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_speaker
----------------------------------
"""

import os
import sys

import unittest
import unittest.mock as mock

import pytest

import scarlett_os
from scarlett_os.utility.gnome import trace
from scarlett_os.utility.gnome import abort_on_exception
from scarlett_os.utility.gnome import _IdleObject

from scarlett_os import speaker

# NOTE: We can't add this here, otherwise we won't be able to mock them

from tests import common
import signal
import builtins
import datetime

import scarlett_os.exceptions


# source: https://github.com/darvid/reqwire/blob/4a1c94f4beaa25caab2bf13e7a427a4d8150660d/tests/unit/conftest.py
FAKE_TIME = datetime.datetime(2020, 1, 1, 0, 0, 0)


@pytest.fixture
def fake_time():
    yield FAKE_TIME



class TestScarlettSpeaker(object):

    def test_speaker_init(self, mocker, monkeypatch):
        mock_time_logger = mocker.patch('scarlett_os.utility.thread.time_logger')
        mock_scarlett_player = mocker.patch('scarlett_os.speaker.player')
        mock_scarlett_subprocess = mocker.patch('scarlett_os.speaker.subprocess')

        # action
        tts_list = [
            'Hello sir. How are you doing this afternoon?'
            ' I am full lee function nall, andd red ee for'
            ' your commands']

        test_path = "/home/pi/dev/bossjones-github/scarlett_os/espeak_tmp.wav"

        for scarlett_text in tts_list:
            with mock_time_logger('Scarlett Speaks'):
                spk = speaker.ScarlettSpeaker(text_to_speak=scarlett_text,
                                              wavpath=test_path)

        assert len(spk._wavefile) == 1
        assert spk._pitch == 75
        assert spk._speed == 175
        assert spk._wavpath == "/home/pi/dev/bossjones-github/scarlett_os/espeak_tmp.wav"
        assert spk._voice == "en+f3"
        assert spk._text == "Hello sir. How are you doing this afternoon? I am full lee function nall, andd red ee for your commands"

        assert spk._word_gap == 1
        mock_scarlett_player.ScarlettPlayer.assert_called_once_with(
            test_path, False, False)

        assert spk._command == ['espeak', '-p75', '-s175', '-g1', '-w', '/home/pi/dev/bossjones-github/scarlett_os/espeak_tmp.wav',
                                        '-ven+f3', '.   Hello sir. How are you doing this afternoon? I am full lee function nall, andd red ee for your commands   .']

        mock_scarlett_subprocess.Subprocess.assert_called_once_with(['espeak', '-p75', '-s175', '-g1', '-w', '/home/pi/dev/bossjones-github/scarlett_os/espeak_tmp.wav',
                                                                     '-ven+f3', '.   Hello sir. How are you doing this afternoon? I am full lee function nall, andd red ee for your commands   .'], name='speaker_tmp', fork=False)
