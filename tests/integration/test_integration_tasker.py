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

from tests import PROJECT_ROOT
import time

from tests.integration.baseclass import run_emitter_signal
from tests.integration.baseclass import IntegrationTestbaseMainloop

done = 0

from scarlett_os.internal import gi  # noqa
from scarlett_os.internal.gi import Gio  # noqa
from scarlett_os.internal.gi import GObject  # noqa
from scarlett_os.internal.gi import GLib

from scarlett_os import tasker


class TestScarlettTasker(IntegrationTestbaseMainloop):
    """Test Tasker Signals for various on_* signal-handler methods
    """

    def test_signal_ready(self, request, get_environment, monkeypatch, get_bus):
        """Create a Controller object, call on_new_mode_online method and
        check that the callback fires initially when the sources are set up
        """
        # Append tuple to recieved_signals
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler. Catch and print information about all singals.
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
            self.recieved_signals.append(v)

        self.setup_tasker(monkeypatch, get_bus)

        self.log.info("setting callback")

        self.tasker.prepare(catchall_handler, catchall_handler, catchall_handler)
        # Sleep to give time for connection to be established
        time.sleep(1)
        self.tasker.configure()

        run_emitter_signal(request, get_environment, sig_name='ready')

        self.log.info("waiting for initial callback with"
                      "('  ScarlettListener is ready', 'pi-listening')")
        self.run_mainloop(timeout=5)

        assert self.recieved_signals[0] == ('  ScarlettListener is ready', 'pi-listening')

    def test_signal_failed(self, request, get_environment, monkeypatch, get_bus):
        """Create a Controller object, call on_new_mode_online method and
        check that the callback fires initially when the sources are set up
        """
        # Append tuple to recieved_signals
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler. Catch and print information about all singals.
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
            self.recieved_signals.append(v)

        self.setup_tasker(monkeypatch, get_bus)

        self.log.info("setting callback")

        self.tasker.prepare(catchall_handler, catchall_handler, catchall_handler)
        # Sleep to give time for connection to be established
        time.sleep(1)
        self.tasker.configure()

        run_emitter_signal(request, get_environment, sig_name='failed')

        self.log.info("waiting for initial callback with"
                      "('  ScarlettListener hit Max STT failures', 'pi-response2')")
        self.run_mainloop(timeout=5)

        assert self.recieved_signals[0] == ('  ScarlettListener hit Max STT failures', 'pi-response2')

    def test_signal_kw_rec(self, request, get_environment, monkeypatch, get_bus):
        """Create a Controller object, call on_new_mode_online method and
        check that the callback fires initially when the sources are set up
        """
        # Append tuple to recieved_signals
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler. Catch and print information about all singals.
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
            self.recieved_signals.append(v)

        self.setup_tasker(monkeypatch, get_bus)

        self.log.info("setting callback")

        self.tasker.prepare(catchall_handler, catchall_handler, catchall_handler)
        # Sleep to give time for connection to be established
        time.sleep(1)
        self.tasker.configure()

        run_emitter_signal(request, get_environment, sig_name='kw-rec')

        self.log.info("waiting for initial callback with"
                      "('  ScarlettListener caught a keyword match', 'pi-listening')")
        self.run_mainloop(timeout=5)

        assert self.recieved_signals[0] == ('  ScarlettListener caught a keyword match', 'pi-listening')

    def test_signal_command(self, request, get_environment, monkeypatch, get_bus):
        """Create a Controller object, call on_new_mode_online method and
        check that the callback fires initially when the sources are set up
        """
        # Append tuple to recieved_signals
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler. Catch and print information about all singals.
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
            self.recieved_signals.append(v)

        self.setup_tasker(monkeypatch, get_bus)

        self.log.info("setting callback")

        self.tasker.prepare(catchall_handler, catchall_handler, catchall_handler)
        # Sleep to give time for connection to be established
        time.sleep(1)
        self.tasker.configure()

        run_emitter_signal(request, get_environment, sig_name='command')

        self.log.info("waiting for initial callback with"
                      "('  ScarlettListener caught a command match', 'pi-response', 'what time is it')")
        self.run_mainloop(timeout=5)

        assert self.recieved_signals[0] == ('  ScarlettListener caught a command match', 'pi-response', 'what time is it')

    def test_signal_cancel(self, request, get_environment, monkeypatch, get_bus):
        """Create a Controller object, call on_new_mode_online method and
        check that the callback fires initially when the sources are set up
        """
        # Append tuple to recieved_signals
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler. Catch and print information about all singals.
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
            self.recieved_signals.append(v)

        self.setup_tasker(monkeypatch, get_bus)

        self.log.info("setting callback")

        self.tasker.prepare(catchall_handler, catchall_handler, catchall_handler)
        # Sleep to give time for connection to be established
        time.sleep(1)
        self.tasker.configure()

        run_emitter_signal(request, get_environment, sig_name='cancel')

        self.log.info("waiting for initial callback with"
                      "('  ScarlettListener cancel speech Recognition', 'pi-cancel')")
        self.run_mainloop(timeout=5)

        assert self.recieved_signals[0] == ('  ScarlettListener cancel speech Recognition', 'pi-cancel')

    def test_signal_connect(self, request, get_environment, monkeypatch, get_bus):
        """Create a Controller object, call on_new_mode_online method and
        check that the callback fires initially when the sources are set up
        """
        # Append tuple to recieved_signals
        def catchall_handler(*args, **kwargs):  # pragma: no cover
            """
            Catch all handler. Catch and print information about all singals.
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
            self.recieved_signals.append(v)

        self.setup_tasker(monkeypatch, get_bus)

        self.log.info("setting callback")

        self.tasker.prepare(catchall_handler, catchall_handler, catchall_handler)
        # Sleep to give time for connection to be established
        time.sleep(1)
        self.tasker.configure()

        run_emitter_signal(request, get_environment, sig_name='connect')

        self.log.info("waiting for initial callback with"
                      "('ScarlettEmitter',)")
        self.run_mainloop(timeout=5)

        assert self.recieved_signals[0] == ('ScarlettEmitter',)

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
