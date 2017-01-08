# -*- coding: utf-8 -*-

"""ScarlettOS Audio Utility functions and classes."""

from __future__ import with_statement, division

from scarlett_os.internal.gi import Gst
from scarlett_os.internal.gi import _gst_available
# from scarlett_os import subprocess
# import json

from gettext import gettext as _
import re
import logging
logger = logging.getLogger(__name__)

QUEUE_SIZE = 10
BUFFER_SIZE = 10
SENTINEL = '__GSTDEC_SENTINEL__'

CARD_MATCH = re.compile(
    r'card (?P<card>\d+)[:].*?[[](?P<description>.*?)[]], device (?P<device>\d+)[:].*?[[](?P<device_description>.*?)[]]')


# subprocess.Subprocess(
#     self._command, name='speaker_tmp', fork=False).run()
# subprocess.check_pid(int(self.res))


# def get_inputs():
#     """Get alsa inputs (relies on having arecord present)"""
#     output = subprocess.check_output(['arecord', '-l'])
#     cards = [line for line in output.splitlines() if line.startswith('card ')]
#     results = [
#         ('Use Default', 'default'),
#     ]
#     for line in cards:
#         match = CARD_MATCH.match(line)
#         if match:
#             description = '%(description)s: %(device_description)s' % match.groupdict(
#             )
#             device = 'hw:%(card)s,%(device)s' % match.groupdict()
#             results.append((description, device))
#     return json.dumps(results)

# def get_outputs():
#     output = subprocess.check_output(['aplay', '-l'])
#     cards = [line for line in output.splitlines() if line.startswith('card ')]
#     results = [
#         ('Use Default', 'default'),
#     ]
#     for line in cards:
#         match = CARD_MATCH.match(line)
#         if match:
#             description = '%(description)s: %(device_description)s' % match.groupdict(
#             )
#             device = 'hw:%(card)s,%(device)s' % match.groupdict()
#             results.append((description, device))
#     return json.dumps(results)


def format_bitrate(value):
    return _("%d kbps") % int(value)


def calculate_duration(num_samples, sample_rate):
    """Determine duration of samples using GStreamer helper for precise
    math."""
    if _gst_available():
        return Gst.util_uint64_scale(num_samples, Gst.SECOND, sample_rate)


def millisecond_to_clocktime(value):
    """Convert a millisecond time to internal GStreamer time."""
    if _gst_available():
        return value * Gst.MSECOND


def clocktime_to_millisecond(value):
    """Convert an internal GStreamer time to millisecond time."""
    if _gst_available():
        return value // Gst.MSECOND
