# -*- coding: utf-8 -*-

"""ScarlettOS Audio Utility functions and classes."""

from __future__ import with_statement, division

from scarlett_os.compat import *
from scarlett_os.utility import compat as s_utility_compat


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
