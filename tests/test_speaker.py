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

import scarlett_os.exceptions


class TestScarlettSpeaker(unittest.TestCase):

    def setUp(self):  # noqa: N802
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """
        pass

    def tearDown(self):
        pass

    @mock.patch('scarlett_os.utility.thread.time_logger', name='mock_time_logger')
    @mock.patch('scarlett_os.speaker.player', name='mock_scarlett_player')
    @mock.patch('scarlett_os.speaker.subprocess', name='mock_scarlett_subprocess')
    def test_speaker_init(self, mock_scarlett_subprocess, mock_scarlett_player, mock_time_logger):
        # action
        tts_list = [
            'Hello sir. How are you doing this afternoon? I am full lee function nall, andd red ee for your commands']

        test_path = "/home/pi/dev/bossjones-github/scarlett_os/espeak_tmp.wav"

        for scarlett_text in tts_list:
            with mock_time_logger('Scarlett Speaks'):
                spk = speaker.ScarlettSpeaker(text_to_speak=scarlett_text,
                                              wavpath=test_path)

        self.assertEqual(len(spk._wavefile), 1)
        self.assertEqual(spk._pitch, 75)
        self.assertEqual(spk._speed, 175)
        self.assertEqual(spk._wavpath, "/home/pi/dev/bossjones-github/scarlett_os/espeak_tmp.wav")
        self.assertEqual(spk._voice, "en+f3")
        self.assertEqual(spk._text, "Hello sir. How are you doing this afternoon? I am full lee function nall, andd red ee for your commands")

        self.assertEqual(spk._word_gap, 1)
        mock_scarlett_player.ScarlettPlayer.assert_called_once_with(test_path, False, False)

        self.assertEqual(spk._command, ['espeak', '-p75', '-s175', '-g1', '-w', '/home/pi/dev/bossjones-github/scarlett_os/espeak_tmp.wav', '-ven+f3', '.   Hello sir. How are you doing this afternoon? I am full lee function nall, andd red ee for your commands   .'])

        mock_scarlett_subprocess.Subprocess.assert_called_once_with(['espeak', '-p75', '-s175', '-g1', '-w', '/home/pi/dev/bossjones-github/scarlett_os/espeak_tmp.wav', '-ven+f3', '.   Hello sir. How are you doing this afternoon? I am full lee function nall, andd red ee for your commands   .'], name='speaker_tmp', fork=False)
