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

from tests.integrationtests.stubs import create_main_loop

from tests import PROJECT_ROOT
import time

from tests.integrationtests.baseclass import run_emitter_signal
from tests.integrationtests.baseclass import IntegrationTestbaseMainloop

done = 0

from scarlett_os.internal import gi  # noqa
from scarlett_os.internal.gi import Gio  # noqa
from scarlett_os.internal.gi import GObject  # noqa
from scarlett_os.internal.gi import GLib

from scarlett_os import tasker
from scarlett_os.tasker import on_signal_recieved


# from scarlett_os.internal.debugger import enable_remote_debugging

# enable_remote_debugging()


@pytest.mark.scarlettonly
@pytest.mark.scarlettonlyintgr
class TestScarlettTasker(IntegrationTestbaseMainloop):
    """Test Tasker Signals for various on_* signal-handler methods
    """

    @pytest.mark.flaky(reruns=5)
    def test_signal_ready(
        self, request, service_on_outside, get_environment, monkeypatch, get_bus
    ):
        """Create a Controller object, call on_new_mode_online method and
        check that the callback fires initially when the sources are set up
        """
        recieved_signals = []

        # Append tuple to recieved_signals
        # FIXME:
        # /home/pi/dev/bossjones-github/scarlett_os/tests/integration/test_integration_tasker.py in catchall_handler(*args=(':1.0', '/org/scarlett/Listener', 'org.scarlett.Listener', 'SttFailedSignal', ('  ScarlettListener hit Max STT failures', 'pi-response2')), **kwargs={})
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler. Catch and print information about all signals.
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

            # Add value to list so we can assert later
            recieved_signals.append(v)

        self.setup_tasker(monkeypatch, get_bus)

        self.log.info("setting callback")

        self.tasker.prepare(catchall_handler, catchall_handler, catchall_handler)
        # Sleep to give time for connection to be established
        time.sleep(2)
        self.tasker.configure()

        run_emitter_signal(request, get_environment, sig_name="ready")

        self.log.info(
            "waiting for initial callback with"
            "('  ScarlettListener is ready', 'pi-listening')"
        )
        self.run_mainloop(timeout=3)

        assert recieved_signals[0] == ("  ScarlettListener is ready", "pi-listening")

    def test_signal_failed(self, request, get_environment, monkeypatch, get_bus):
        """Create a Controller object, call on_new_mode_online method and
        check that the callback fires initially when the sources are set up
        """
        recieved_signals = []

        # Append tuple to recieved_signals
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler. Catch and print information about all signals.
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

            # Add value to list so we can assert later
            recieved_signals.append(v)

        self.setup_tasker(monkeypatch, get_bus)

        self.log.info("setting callback")

        self.tasker.prepare(catchall_handler, catchall_handler, catchall_handler)
        # Sleep to give time for connection to be established
        # time.sleep(1)
        self.tasker.configure()

        run_emitter_signal(request, get_environment, sig_name="failed")

        self.log.info(
            "waiting for initial callback with"
            "('  ScarlettListener hit Max STT failures', 'pi-response2')"
        )
        self.run_mainloop(timeout=3)

        assert recieved_signals[0] == (
            "  ScarlettListener hit Max STT failures",
            "pi-response2",
        )

    def test_signal_kw_rec(self, request, get_environment, monkeypatch, get_bus):
        """Create a Controller object, call on_new_mode_online method and
        check that the callback fires initially when the sources are set up
        """

        recieved_signals = []

        # Append tuple to recieved_signals
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler. Catch and print information about all signals.
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

            # Add value to list so we can assert later
            recieved_signals.append(v)

        self.setup_tasker(monkeypatch, get_bus)

        self.log.info("setting callback")

        self.tasker.prepare(catchall_handler, catchall_handler, catchall_handler)
        # Sleep to give time for connection to be established
        # time.sleep(1)
        self.tasker.configure()

        run_emitter_signal(request, get_environment, sig_name="kw-rec")

        self.log.info(
            "waiting for initial callback with"
            "('  ScarlettListener caught a keyword match', 'pi-listening')"
        )
        self.run_mainloop(timeout=3)

        assert recieved_signals[0] == (
            "  ScarlettListener caught a keyword match",
            "pi-listening",
        )

    def test_signal_command(self, request, get_environment, monkeypatch, get_bus):
        """Create a Controller object, call on_new_mode_online method and
        check that the callback fires initially when the sources are set up
        """
        recieved_signals = []

        # Append tuple to recieved_signals
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler. Catch and print information about all signals.
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

            # Add value to list so we can assert later
            recieved_signals.append(v)

        self.setup_tasker(monkeypatch, get_bus)

        self.log.info("setting callback")

        self.tasker.prepare(catchall_handler, catchall_handler, catchall_handler)
        # Sleep to give time for connection to be established
        # time.sleep(1)
        self.tasker.configure()

        run_emitter_signal(request, get_environment, sig_name="cmd-rec")

        self.log.info(
            "waiting for initial callback with"
            "('  ScarlettListener caught a command match', 'pi-response', 'what time is it')"
        )
        self.run_mainloop(timeout=3)

        assert recieved_signals[0] == (
            "  ScarlettListener caught a command match",
            "pi-response",
            "what time is it",
        )

    def test_signal_cancel(self, request, get_environment, monkeypatch, get_bus):
        """Create a Controller object, call on_new_mode_online method and
        check that the callback fires initially when the sources are set up
        """
        recieved_signals = []

        # Append tuple to recieved_signals
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler. Catch and print information about all signals.
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

            # Add value to list so we can assert later
            recieved_signals.append(v)

        self.setup_tasker(monkeypatch, get_bus)

        self.log.info("setting callback")

        self.tasker.prepare(catchall_handler, catchall_handler, catchall_handler)
        # Sleep to give time for connection to be established
        # time.sleep(1)
        self.tasker.configure()

        run_emitter_signal(request, get_environment, sig_name="cancel")

        self.log.info(
            "waiting for initial callback with"
            "('  ScarlettListener cancel speech Recognition', 'pi-cancel')"
        )
        self.run_mainloop(timeout=3)

        assert recieved_signals[0] == (
            "  ScarlettListener cancel speech Recognition",
            "pi-cancel",
        )

    def test_signal_connect(self, request, get_environment, monkeypatch, get_bus):
        """Create a Controller object, call on_new_mode_online method and
        check that the callback fires initially when the sources are set up
        """
        recieved_signals = []

        # Append tuple to recieved_signals
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler. Catch and print information about all signals.
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

            # Add value to list so we can assert later
            recieved_signals.append(v)

        self.setup_tasker(monkeypatch, get_bus)

        self.log.info("setting callback")

        self.tasker.prepare(catchall_handler, catchall_handler, catchall_handler)
        self.tasker.configure()

        run_emitter_signal(request, get_environment, sig_name="connect")

        self.log.info("waiting for initial callback with" "('ScarlettEmitter',)")
        self.run_mainloop(timeout=3)

        assert recieved_signals[0] == ("ScarlettEmitter",)

    def test_real_signal_ready(self, request, get_environment, monkeypatch, get_bus):
        """Create a Controller object, call on_new_mode_online method and
        check that the callback fires initially when the sources are set up
        """
        recieved_signals = []

        monkeypatch.setattr(tasker.player.ScarlettPlayer, "DEFAULT_SINK", "fakesink")

        # Append tuple to recieved_signals
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler. Catch and print information about all signals.
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

            # Add value to list so we can assert later
            recieved_signals.append(v)

        self.setup_tasker(monkeypatch, get_bus)

        self.log.info("setting callback")

        self.tasker.prepare(on_signal_recieved, on_signal_recieved, on_signal_recieved)
        # Sleep to give time for connection to be established
        # time.sleep(1)
        self.tasker.configure()

        run_emitter_signal(request, get_environment, sig_name="ready")

        self.log.info(
            "waiting for initial callback with"
            "('  ScarlettListener is ready', 'pi-listening')"
        )
        self.run_mainloop(timeout=3)

        # At this point is should have played the ready sound
        ########################################################

    def test_real_signal_failed(self, request, get_environment, monkeypatch, get_bus):
        """Create a Controller object, call on_new_mode_online method and
        check that the callback fires initially when the sources are set up
        """
        recieved_signals = []

        monkeypatch.setattr(tasker.player.ScarlettPlayer, "DEFAULT_SINK", "fakesink")

        # Append tuple to recieved_signals
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler. Catch and print information about all signals.
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

            # Add value to list so we can assert later
            recieved_signals.append(v)

        self.setup_tasker(monkeypatch, get_bus)

        self.log.info("setting callback")

        self.tasker.prepare(on_signal_recieved, on_signal_recieved, on_signal_recieved)
        self.tasker.configure()

        run_emitter_signal(request, get_environment, sig_name="failed")

        self.log.info(
            "waiting for initial callback with"
            "('  ScarlettListener hit Max STT failures', 'pi-response2')"
        )
        self.run_mainloop(timeout=3)

    def test_real_signal_kw_rec(self, request, get_environment, monkeypatch, get_bus):
        """Create a Controller object, call on_new_mode_online method and
        check that the callback fires initially when the sources are set up
        """

        recieved_signals = []

        monkeypatch.setattr(tasker.player.ScarlettPlayer, "DEFAULT_SINK", "fakesink")

        # Append tuple to recieved_signals
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler. Catch and print information about all signals.
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

            # Add value to list so we can assert later
            recieved_signals.append(v)

        self.setup_tasker(monkeypatch, get_bus)

        self.log.info("setting callback")

        self.tasker.prepare(on_signal_recieved, on_signal_recieved, on_signal_recieved)
        self.tasker.configure()

        run_emitter_signal(request, get_environment, sig_name="kw-rec")

        self.log.info(
            "waiting for initial callback with"
            "('  ScarlettListener caught a keyword match', 'pi-listening')"
        )
        self.run_mainloop(timeout=3)

    def test_real_signal_command(self, request, get_environment, monkeypatch, get_bus):
        """Create a Controller object, call on_new_mode_online method and
        check that the callback fires initially when the sources are set up
        """
        recieved_signals = []

        monkeypatch.setattr(tasker.player.ScarlettPlayer, "DEFAULT_SINK", "fakesink")

        # Append tuple to recieved_signals
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler. Catch and print information about all signals.
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

            # Add value to list so we can assert later
            recieved_signals.append(v)

        self.setup_tasker(monkeypatch, get_bus)

        self.log.info("setting callback")

        self.tasker.prepare(on_signal_recieved, on_signal_recieved, on_signal_recieved)
        self.tasker.configure()

        run_emitter_signal(request, get_environment, sig_name="cmd-rec")

        self.log.info(
            "waiting for initial callback with"
            "('  ScarlettListener caught a command match', 'pi-response', 'what time is it')"
        )
        self.run_mainloop(timeout=3)

    def test_real_signal_cancel(self, request, get_environment, monkeypatch, get_bus):
        """Create a Controller object, call on_new_mode_online method and
        check that the callback fires initially when the sources are set up
        """
        recieved_signals = []

        monkeypatch.setattr(tasker.player.ScarlettPlayer, "DEFAULT_SINK", "fakesink")

        # Append tuple to recieved_signals
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler. Catch and print information about all signals.
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

            # Add value to list so we can assert later
            recieved_signals.append(v)

        self.setup_tasker(monkeypatch, get_bus)

        self.log.info("setting callback")

        self.tasker.prepare(on_signal_recieved, on_signal_recieved, on_signal_recieved)
        self.tasker.configure()

        run_emitter_signal(request, get_environment, sig_name="cancel")

        self.log.info(
            "waiting for initial callback with"
            "('  ScarlettListener cancel speech Recognition', 'pi-cancel')"
        )
        self.run_mainloop(timeout=3)
