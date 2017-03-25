# This module is designed to handle all multi-threading processes in
# Gourmet. Separate threads are limited to doing the following things
# with respect to the GUI:
#
#   1. Start a notification dialog with a progress bar
#   2. Update the progress bar
#   3. Finish successfully
#   4. Stop with an error.
#
# If you need to get user input in the middle of your threaded process,
# you need to redesign so that it works as follows:
#
# 1. Run the first half of your process as a thread.
# 2. Upon completion of your thread, run your dialog to get your user
#    input
# 3. Run the second half of your process as a thread.
#
# In this module, we define the following base classes...
#
# A singleton ThreadingManager that tracks how many threads we have
# running, and allows a maximum number of threads to be run at any
# single time.
#
# A SuspendableThread base class for creating and running threaded
# processes.
#

import os
import sys
import signal
import time
import logging
import threading

# atexit.register(func, *args, **kargs)
#     Register func as a function to be executed at termination. Any optional arguments that are to be passed to func must be passed as arguments to register(). It is possible to register the same function and arguments more than once.
#
#     At normal program termination (for instance, if sys.exit() is called or the main module’s execution completes), all functions registered are called in last in, first out order. The assumption is that lower level modules will normally be imported before higher level modules and thus must be cleaned up later.
#
#     If an exception is raised during execution of the exit handlers, a traceback is printed (unless SystemExit is raised) and the exception information is saved. After all exit handlers have had a chance to run the last exception to be raised is re-raised.
#
#     This function returns func, which makes it possible to use it as a decorator.
import atexit

from gettext import gettext as _
from gettext import ngettext
from scarlett_os.internal.gi import gi
from scarlett_os.internal.gi import GObject
from scarlett_os.internal.gi import GLib
from scarlett_os.utility.gnome import _IdleObject

logger = logging.getLogger(__name__)


class Terminated (Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SuspendableThread(threading.Thread, _IdleObject):
    """A class for long-running processes that shouldn't interrupt the
    GUI.
    """

    __gsignals__ = {
        'completed': (GObject.SignalFlags.RUN_LAST, None, ()),
        'progress': (GObject.SignalFlags.RUN_LAST, None, [float, str]),  # percent complete, progress bar text
        'error': (GObject.SignalFlags.RUN_LAST, None, [int,  # error number
                                                       str,  # error name
                                                       str   # stack trace
                                                       ]),
        'stopped': (GObject.SignalFlags.RUN_LAST, None, []),  # emitted when we are stopped
        'pause': (GObject.SignalFlags.RUN_LAST, None, []),  # emitted when we pause
        'resume': (GObject.SignalFlags.RUN_LAST, None, []),  # emitted when we resume
        'done': (GObject.SignalFlags.RUN_LAST, None, []),  # emitted when/however we finish
    }

    def __init__(self, name=None):
        self.initialized = False
        self.suspended = False
        self.terminated = False
        self.done = False
        self.tasks_finished = 0
        _IdleObject.__init__(self)
        threading.Thread.__init__(self, name=name)

    def initialize_thread(self):
        self.initialized = True
        self.start()

    def connect_subthread(self, subthread):
        """For subthread subthread, connect to error and pause signals and
        and emit as if they were our own."""
        subthread.connect('error', lambda st, enum, ename, strace: self.emit('error', enum, ename, strace))
        subthread.connect('stopped', lambda st: self.emit('stopped'))
        subthread.connect('pause', lambda st: self.emit('pause'))
        subthread.connect('resume', lambda st: self.emit('resume'))

    def run(self):
        try:
            self.do_run()
        except Terminated:
            self.emit('stopped')
        except:
            import traceback
            self.emit('error', 1,
                      'Error during %s' % self.name,
                      traceback.format_exc())
        else:
            self.emit('completed')
        self.done = True
        self.emit('done')

    def do_run(self):
        # Note that sub-classes need to call check_for_sleep
        # periodically, otherwise pausing & cancelling won't work
        raise NotImplementedError

    def suspend(self):
        self.suspended = True

    def resume(self):
        self.suspended = False

    def terminate(self):
        self.terminated = True
        self.emit('stopped')

    def check_for_sleep(self):
        """Check whether we have been suspended or terminated.
        """
        paused_emitted = False
        emit_resume = False
        if self.terminated:
            raise Terminated('%s terminated' % self.name)
        if self.suspended:
            self.emit('pause')
            emit_resume = True
        while self.suspended:
            if self.terminated:
                raise Terminated('%s terminated' % self.name)
            time.sleep(1)
        if emit_resume:
            self.emit('resume')

    def __repr__(self):
        try:
            return threading.Thread.__repr__(self)
        except AssertionError:
            return '<SuspendableThread %s - uninitialized>' % self.name
    #
    # @GObject.Property(type=int)
    # def tasks_finished(self):
    #     """Read-write integer property."""
    #     return self.tasks_finished
    #
    # @tasks_finished.setter
    # def tasks_finished(self, value):
    #     """Set integer property."""
    #     self.tasks_finished = value


class NotThreadSafe:
    """Subclasses of this do things that are not thread safe. An error
    will be raised if an object that is an instance of this class is
    added to a thread manager.
    """
    pass


class ThreadManager:

    __single = None

    def __init__(self, max_concurrent_threads=2):
        if ThreadManager.__single:
            raise ThreadManager.__single
        self.max_concurrent_threads = max_concurrent_threads
        self.thread_queue = []
        self.count = 0
        self.active_count = 0
        self.completed_threads = 0
        self.threads = []

    def add_thread(self, thread):
        try:
            assert(isinstance(thread, SuspendableThread))
        except AssertionError:
            print('Class', thread, type(thread), 'is not a SuspendableThread')
            raise
        if isinstance(thread, NotThreadSafe):
            raise TypeError("Thread %s is NotThreadSafe" % thread)
        self.threads.append(thread)
        thread.connect('pause', self.register_thread_paused)
        thread.connect('resume', self.register_thread_resume)
        thread.connect('done', self.register_thread_done)
        if self.active_count < self.max_concurrent_threads:
            self.active_count += 1
            thread.initialize_thread()
        else:
            self.thread_queue.append(thread)

    def register_thread_done(self, thread):
        if thread in self.threads:
            self.threads.remove(thread)
            self.active_count -= 1
            self.completed_threads += 1
            self.start_queued_threads()

    def register_thread_paused(self, thread):
        self.active_count -= 1
        self.start_queued_threads()

    def register_thread_resume(self, thread):
        self.active_count += 1

    def resume_thread(self, thread):
        if self.active_count < self.max_concurrent_threads:
            thread.resume()
            self.active_count += 1
        else:
            self.thread_queue.append(thread)

    def start_queued_threads(self):
        while self.active_count < self.max_concurrent_threads and self.thread_queue:
            thread_to_add = self.thread_queue.pop()
            self.active_count += 1
            if thread_to_add.initialized:
                thread_to_add.resume()
            else:
                thread_to_add.initialize_thread()


def get_thread_manager(max_concurrent_threads):
    try:
        return ThreadManager(max_concurrent_threads=max_concurrent_threads)
    except ThreadManager as tm:
        return tm

if __name__ == "__main__":
    # Smoke Tests
    if os.environ.get('SCARLETT_DEBUG_MODE'):
        import faulthandler
        faulthandler.register(signal.SIGUSR2, all_threads=True)

        from scarlett_os.internal.debugger import init_debugger
        init_debugger()

        from scarlett_os.internal.debugger import enable_remote_debugging
        enable_remote_debugging()

    from scarlett_os.logger import setup_logger
    setup_logger()

    loop = GLib.MainLoop()

    to_complete = 2

    class TestThread(SuspendableThread):

        def do_run(self):
            for n in range(1000):
                time.sleep(0.01)
                self.emit('progress', n / 1000.0, '%s of 1000' % n)
                self.check_for_sleep()

    class TestError(SuspendableThread):

        def do_run(self):
            for n in range(1000):
                time.sleep(0.01)
                if n == 100:
                    raise AttributeError("This is a phony error")
                self.emit('progress', n / 1000.0, '%s of 1000' % n)
                self.check_for_sleep()

    # run forever, we'll want this for listener thread in scarlett
    class TestInterminable(SuspendableThread):

        def do_run(self):
            while 1:
                time.sleep(0.1)
                self.emit('progress', -1, 'Working interminably')
                self.check_for_sleep()

    tm = get_thread_manager(2)
    for desc, thread in [
        ('Interminable 1', TestInterminable()),
        ('Linear 1', TestThread()),
        ('Linear 2', TestThread()),
        ('Interminable 2', TestInterminable()),
        ('Error 3', TestError())
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

    # Create a timeout that checks how many tasks have been completed. When 2 have finished, kill threads and finish.
    GLib.timeout_add_seconds(30, get_tm_active_count)
    loop.run()
