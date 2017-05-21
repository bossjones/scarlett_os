#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_integration_threadmanager
----------------------------------
"""


# Borrowed from test_integration_player - START
###########################################
###########################################
import builtins
from gettext import gettext as _
import os
import signal
import sys
import threading
import time
import unittest
import unittest.mock as mock

# import pydbus
import pytest

import scarlett_os
import scarlett_os.exceptions
from scarlett_os.internal import gi
from scarlett_os.internal.gi import GLib
from scarlett_os.internal.gi import GObject
from scarlett_os.internal.gi import Gio
from scarlett_os.utility import threadmanager
from scarlett_os.utility.threadmanager import NotThreadSafe, SuspendableThread
from tests import PROJECT_ROOT
from tests.integration.baseclass import IntegrationTestbaseMainloop, run_emitter_signal
from tests.integration.stubs import create_main_loop

# import hunter
# hunter.trace(module='threadmanager', action=hunter.CallPrinter)

done = 0

@pytest.fixture
def tmanager():
    """Create a fixture of ThreadManager"""
    # create threadmanager
    tmanager = threadmanager.ThreadManager.get_instance(2)  # pylint: disable=W0621
    # yield it to calling function/test
    yield tmanager
    # when we get control again after test finishes, nuke tmanager.__instance
    print('\n[teardown] tmanager.__instance = None ...')
    tmanager.__instance = None
    # when we get control again after test finishes, print this
    print('\n[teardown] del tmanager ...')
    # then nuke object
    del tmanager


class TThread(SuspendableThread):
    """Short for Test Thread. Suspendable"""

    def __init__(self):
        SuspendableThread.__init__(
            self,
            name=_('TThread')
        )

    def do_run(self):
        for n in range(1000):  # pylint: disable=C0103
            time.sleep(0.01)
            self.emit('progress', n / 1000.0, '%s of 1000' % n)
            print('progress', n / 1000.0, '%s of 1000' % n)
            self.check_for_sleep()


class TError(SuspendableThread):
    """Thread that raises an exception"""

    def do_run(self):
        for n in range(1000):  # pylint: disable=C0103
            time.sleep(0.01)
            if n == 100:
                raise AttributeError("This is a phony error")
            self.emit('progress', n / 1000.0, '%s of 1000' % n)
            self.check_for_sleep()


# run forever, we'll want this for listener thread in scarlett
class TInterminable(SuspendableThread):
    """Test Thread that never dies"""

    def do_run(self):
        while 1:
            time.sleep(0.1)
            self.emit('progress', -1, 'Working interminably')
            self.check_for_sleep()


class NTsafeThread(SuspendableThread, NotThreadSafe):
    """Non Thread Safe test thread"""

    def __init__(self):
        SuspendableThread.__init__(
            self,
            name=_('NTsafeThread')
        )
        # NotThreadSafe.__init__()

    def do_run(self):
        """Contents of this doesn't matter, just need one defined."""
        while 1:
            time.sleep(0.1)
            self.emit('progress', -1, 'Working interminably')
            self.check_for_sleep()


@pytest.mark.scarlettonly
@pytest.mark.scarlettonlyintgr
class TestThreadManager(object):
    """TestThreadManager. Real test case."""

    # 5/7/2017 def test_ThreadManager(self, monkeypatch, tmanager):
    # pylint: disable=C0111
    # pylint: disable=C0103
    def test_ThreadManager_TThread(self, tmanager):
        blacklist_threads = ['MainThread', 'HistorySavingThread', 'IPythonHistorySavingThread', 'Dummy', 'Thread']
        whitelist_threads = ['SuspendableMainLoopThread', 'NTsafeThread', 'TInterminable', 'TError', 'TThread']
        # MainThread
        # IPythonHistorySavingThread
        # SuspendableMainLoopThread
        # IPythonHistorySavingThread
        # Dummy-6
        # Thread-1

        tm = tmanager

        assert str(type(tm)) == "<class 'scarlett_os.utility.threadmanager.ThreadManager'>"

        assert tm.active_count == 0
        assert tm.completed_threads == 0
        assert tm.count == 0
        assert tm.max_concurrent_threads == 2
        assert tm.thread_queue == []
        assert tm.threads == []

        # import pdb
        # pdb.set_trace()

        loop = GLib.MainLoop()

        to_complete = 2

        for desc, thread in [
            ('Linear 1', TThread()),
            ('Linear 2', TThread())
        ]:
            tm.add_thread(thread)

        # import pdb;pdb.set_trace()

        def get_tm_active_count(*args):
            print('time.sleep(3)')
            time.sleep(3)
            if int(tm.completed_threads) < to_complete:
                print("tm.completed_threads < to_complete: {} < {} friends.".format(tm.completed_threads, to_complete))
                # NOTE: keep running callback
                return True
            else:
                print("tm.completed_threads <= to_complete: {} < {} friends.".format(tm.completed_threads, to_complete))

                # tm.completed_threads < to_complete: 0 < 2 friends.
                # tm.completed_threads <= to_complete: 2 < 2 friends.
                # Current Thread via t_in_progress_intgr.getName(): [MainThread]
                # Current Thread via t_in_progress_intgr.getName(): [IPythonHistorySavingThread]
                # Current Thread via t_in_progress_intgr.getName(): [IPythonHistorySavingThread]
                # Current Thread via t_in_progress_intgr.getName(): [Dummy-5]
                # Current Thread via t_in_progress_intgr.getName(): [Dummy-2]
                # Current Thread via t_in_progress_intgr.getName(): [SuspendableMainLoopThread]
                # Current Thread via t_in_progress_intgr.getName(): [Thread-1]
                # Another process is in progress
                #########################################################################################
                # Return a list of all Thread objects currently alive. The list includes daemonic threads,
                # dummy thread objects created by current_thread(), and the main thread.
                # It excludes terminated threads and threads that have not yet been started.
                #########################################################################################
                threads = threading.enumerate()
                # source: http://www.diveintopython.net/power_of_introspection/filtering_lists.html
                filtered_threads = [elem for elem in threads if elem.getName() in whitelist_threads]
                print("threads = threading.enumerate(): {}".format(filtered_threads))
                for t_print in filtered_threads:
                    print('****************************')
                    print(t_print)
                    print(t_print.getName())
                    print('****************************')

                if len(filtered_threads) > 1:
                    msg = "Another process is in progress"
                    for t_in_progress_intgr in filtered_threads:
                        print("Current Thread via t_in_progress_intgr.getName(): [{}]".format(t_in_progress_intgr.getName()))
                        if "SuspendableMainLoopThread" in t_in_progress_intgr.getName():
                            msg = _("An SuspendableMainLoopThread is in progress.")
                        if "export" in t_in_progress_intgr.getName():
                            msg = _("An export is in progress.")
                        if "delete" in t_in_progress_intgr.getName():
                            msg = _("A delete is in progress.")
                        if "TThread" in t_in_progress_intgr.getName():
                            msg = _("A TThread delete is in progress.")
                    # source: https://github.com/thinkle/gourmet/blob/a97af28b79af7cf1181b8bbd14c61eb396eb7ac6/gourmet/GourmetRecipeManager.py
                    print(msg)

                # Normally this is a diaologe where someone selects "yes i'm sure"
                quit_anyway = True

                if quit_anyway:
                    for t_quit_anyway_intgr in filtered_threads:  # pylint: disable=C0103
                        if t_quit_anyway_intgr.getName() in whitelist_threads:
                            try:
                                print("QUIT ANYWAY t_in_progress_intgr.getName(): [{}]".format(t_quit_anyway_intgr.getName()))
                                t_quit_anyway_intgr.terminate()
                            except BaseException as t_quit_anyway_intgr_exec:  # pylint: disable=C0103
                                print("Unable to terminate thread %s" % t_quit_anyway_intgr)
                                print("[t_quit_anyway_intgr.terminate()] Recieved: {}".format(str(t_quit_anyway_intgr_exec)))
                                # try not to lose data if this is going to
                                # end up in a force quit
                                return True
                        else:
                            print('t_quit_anyway_intgr.getName() in whitelist_threads == FALSE, continue callback')
                            # thread is not part of the whitelist threads list, continue callback
                            return True
                        # end - if t_quit_anyway_intgr.getName() in whitelist_threads:
                else:
                    print('quit_anyway set to false. continue callback')
                    # continue callback
                    return True

                print(__name__ + '.loop.quit()')
                loop.quit()
                # remove callback
                print(__name__ + ': remove callback')
                return False

        GLib.timeout_add_seconds(10, get_tm_active_count)
        loop.run()
