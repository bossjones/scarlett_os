#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_integration_listener
----------------------------------
"""

###########################################
# Borrowed from test_integration_player - START
###########################################
import os
import sys
import signal
import pytest
import builtins
import threading
from gettext import gettext as _

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

from scarlett_os.utility import threadmanager
from scarlett_os.utility.threadmanager import SuspendableThread
from scarlett_os.utility.threadmanager import NotThreadSafe

from gettext import gettext as _


@pytest.fixture
def tmanager():
    # create threadmanager
    tmanager = threadmanager.get_thread_manager(2)
    # yield it to calling function/test
    yield tmanager
    # when we get control again after test finishes, print this
    print('\n[teardown] test_ThreadManager, killing threadmanager ...')
    # then nuke object
    del tmanager


class TThread(SuspendableThread):

    def __init__(self):
        SuspendableThread.__init__(
            self,
            name=_('TThread')
        )

    def do_run(self):
        for n in range(1000):
            time.sleep(0.01)
            self.emit('progress', n / 1000.0, '%s of 1000' % n)
            self.check_for_sleep()


class TError(SuspendableThread):

    def do_run(self):
        for n in range(1000):
            time.sleep(0.01)
            if n == 100:
                raise AttributeError("This is a phony error")
            self.emit('progress', n / 1000.0, '%s of 1000' % n)
            self.check_for_sleep()


# run forever, we'll want this for listener thread in scarlett
class TInterminable(SuspendableThread):

    def do_run(self):
        while 1:
            time.sleep(0.1)
            self.emit('progress', -1, 'Working interminably')
            self.check_for_sleep()


class NTsafeThread(SuspendableThread, NotThreadSafe):

    def __init__(self):
        SuspendableThread.__init__(
            self,
            name=_('NTsafeThread')
        )
        NotThreadSafe.__init__()

    def do_run(self):
        """Contents of this doesn't matter, just need one defined."""
        while 1:
            time.sleep(0.1)
            self.emit('progress', -1, 'Working interminably')
            self.check_for_sleep()


class TestThreadManager(object):

    def test_ThreadManager(self, monkeypatch, tmanager):
        tm = tmanager

        assert str(type(tm)) == "<class 'scarlett_os.utility.threadmanager.ThreadManager'>"

        assert tm.active_count == 0
        assert tm.completed_threads == 0
        assert tm.count == 0
        assert tm.max_concurrent_threads == 2
        assert tm.thread_queue == []
        assert tm.threads == []

        # for desc, thread in [
        #     ('Interminable 1', TestInterminable()),
        #     ('Linear 1', TestThread()),
        #     ('Linear 2', TestThread()),
        #     ('Interminable 2', TestInterminable()),
        #     ('Error 3', TestError())
        # ]:
        #     tm.add_thread(thread)

    def test_ThreadManager_TThread(self, monkeypatch, tmanager):
        tm = tmanager

        loop = GLib.MainLoop()

        to_complete = 2

        # assert str(type(tm)) == "<class 'scarlett_os.utility.threadmanager.ThreadManager'>"
        #
        # assert tm.active_count == 0
        # assert tm.completed_threads == 0
        # assert tm.count == 0
        # assert tm.max_concurrent_threads == 2
        # assert tm.thread_queue == []
        # assert tm.threads == []

        # import pdb;pdb.set_trace()

        for desc, thread in [
            ('Linear 1', TThread()),
            ('Linear 2', TThread())
        ]:
            tm.add_thread(thread)

        def get_tm_active_count(*args):
            time.sleep(3)
            if tm.completed_threads < to_complete:
                print("tm.completed_threads < to_complete: {} < {} friends.".format(tm.completed_threads, to_complete))
                # NOTE: keep running callback
                return True
            else:
                print("tm.completed_threads <= to_complete: {} < {} friends.".format(tm.completed_threads, to_complete))

                # Return a list of all Thread objects currently alive. The list includes daemonic threads,
                # dummy thread objects created by current_thread(), and the main thread.
                # It excludes terminated threads and threads that have not yet been started.
                threads = threading.enumerate()
                if len(threads) > 1:
                    msg = "Another process is in progress"
                    for t in threads:
                        if "import" in t.getName():
                            msg = _("An import is in progress.")
                        if "export" in t.getName():
                            msg = _("An export is in progress.")
                        if "delete" in t.getName():
                            msg = _("A delete is in progress.")

                # source: https://github.com/thinkle/gourmet/blob/a97af28b79af7cf1181b8bbd14c61eb396eb7ac6/gourmet/GourmetRecipeManager.py
                print(msg)

                # Normally this is a diaologe where someone selects "yes i'm sure"
                quit_anyway = True

                if quit_anyway:
                    for t in threads:
                        if t.getName() != 'MainThread':
                            try:
                                t.terminate()
                            except:
                                print("Unable to terminate thread %s" % t)
                                # try not to lose data if this is going to
                                # end up in a force quit
                                return True
                else:
                    return True

                loop.quit()
                # remove callback
                return False

        GLib.timeout_add_seconds(10, get_tm_active_count)
        loop.run()
