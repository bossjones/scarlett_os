#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_listener
----------------------------------
"""

import os
import sys

import unittest

# import mock
import unittest.mock as mock

import threading
import pytest


import scarlett_os
from scarlett_os.utility.gnome import trace
from scarlett_os.utility.gnome import abort_on_exception
from scarlett_os.utility.gnome import _IdleObject

from scarlett_os import listener
from scarlett_os.listener import get_loop_thread, MainLoopThread

# NOTE: We can't add this here, otherwise we won't be able to mock them
# from scarlett_os.internal.gi import GLib, GObject

from tests import common
import signal
import builtins

import scarlett_os.exceptions
