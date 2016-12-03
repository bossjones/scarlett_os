#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Scarlett Dbus Service. Implemented via MPRIS D-Bus Interface Specification."""

from __future__ import with_statement, division, absolute_import

import os
import sys
from scarlett_os.exceptions import SubProcessError, TimeOutError
import logging
from scarlett_os.internal.gi import GObject, GLib

logger = logging.getLogger(__name__)


def check_pid(pid):
    """Check For the existence of a unix pid."""
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


# def map_type_to_command(command):
#     """Return: Map after applying type to several objects in an array"""
#     return map(type, command)
#
#
# def check_command_type(command):
#     types = map_type_to_command(command)
#     # <map at 0x7f08918d74e0>
#     if not (min(types) == max(types) == str):
#         raise TypeError("Executables and arguments must be str objects")
#     else:
#         logger.debug("Running %r" % " ".join(command))
#         return True


class Subprocess(GObject.GObject):
    """
    GObject API for handling child processes.

    :param command: The command to be run as a subprocess.
    :param fork: If `True` this process will be detached from its parent and
                 run independent. This means that no excited-signal will be emited.

    :type command: `list`
    :type fork: `bool`
    """

    __gtype_name__ = 'Subprocess'
    __gsignals__ = {
        'exited': (GObject.SignalFlags.RUN_LAST, None, (GObject.TYPE_INT, GObject.TYPE_INT))
    }

    def __init__(self, command, name=None, fork=False):
        """Create instance of Subprocess."""

        GObject.GObject.__init__(self)

        self.process = None
        self.pid = None

        if not fork:
            self.stdout = True
            self.stderr = True
        else:
            self.stdout = False
            self.stderr = False

        self.forked = fork
        # self.types = None

        # types = map(type, command)
        # # <map at 0x7f08918d74e0>
        # if not (min(types) == max(types) == str):
        #     raise TypeError("executables and arguments must be str objects")
        # logger.debug("Running %r" % " ".join(command))

        # Verify that command is properly formatted and each argument is a str
        self.check_command_type(command)

        self.command = command
        self.name = name

        # self.command = command
        # self.name = name
        # self.forked = fork
        # self.types = None

        logger.debug("command: {}".format(self.command))
        logger.debug("name: {}".format(self.name))
        logger.debug("forked: {}".format(self.forked))
        logger.debug("process: {}".format(self.process))
        logger.debug("pid: {}".format(self.pid))

        if fork:
            self.fork()

    def spawn_command(self):
        """Return: Tuple (pid(int), stdin, stdout, stderr)"""
        return GLib.spawn_async(self.command,
                                flags=GLib.SpawnFlags.SEARCH_PATH | GLib.SpawnFlags.DO_NOT_REAP_CHILD
                                )

    def map_type_to_command(self, command):
        """Return: Map after applying type to several objects in an array"""
        # NOTE: In python3, many processes that iterate over iterables return iterators themselves. In most cases, this ends up saving memory, and should make things go faster.
        # cause of that, we need to call list() over the map object
        return list(map(type, command))

    def check_command_type(self, command):
        # TODO: Add a test to see if function
        # source: http://stackoverflow.com/questions/624926/how-to-detect-whether-a-python-variable-is-a-function

        # if callable(map_func):
        types = self.map_type_to_command(command)

        if type(types) is not list:
            raise TypeError("Variable types should return a list in python3. Got: {}".format(types))

        # <map at 0x7f08918d74e0>
        # NOTE: str is a built-in function (actually a class) which converts its argument to a string. string is a module which provides common string operations.
        # source: http://stackoverflow.com/questions/2026038/relationship-between-string-module-and-str
        for t in types:
            if t is not str:
                raise TypeError("Executables and arguments must be str objects. types: {}".format(t))

        # if not (min(types) == max(types) == str):
        #     raise TypeError("Executables and arguments must be str objects. types: {}".format(types))
        # else:
        logger.debug("Running Command: %r" % " ".join(command))
        return True

    def run(self):
        """Run the process."""

        # NOTE: DO_NOT_REAP_CHILD: the child will not be automatically reaped;
        # you must use g_child_watch_add yourself (or call waitpid or handle `SIGCHLD` yourself),
        # or the child will become a zombie.
        # source:
        # http://valadoc.org/#!api=glib-2.0/GLib.SpawnFlags.DO_NOT_REAP_CHILD

        # NOTE: SEARCH_PATH: argv[0] need not be an absolute path, it will be looked for in the user's PATH
        # source:
        # http://lazka.github.io/pgi-docs/#GLib-2.0/flags.html#GLib.SpawnFlags.SEARCH_PATH

        self.pid, self.stdin, self.stdout, self.stderr = self.spawn_command()

        logger.debug("command: {}".format(self.command))
        logger.debug("stdin: {}".format(self.stdin))
        logger.debug("stdout: {}".format(self.stdout))
        logger.debug("stderr: {}".format(self.stderr))
        logger.debug("pid: {}".format(self.pid))

        # close file descriptor
        self.pid.close()

        print(self.stderr)

        # NOTE: GLib.PRIORITY_HIGH = -100
        # Use this for high priority event sources.
        # It is not used within GLib or GTK+.
        watch = GLib.child_watch_add(GLib.PRIORITY_HIGH, self.pid, self.exited_cb)

        return self.pid

    def exited_cb(self, pid, condition):
        if not self.forked:
            self.emit('exited', pid, condition)

    def fork(self):
        """Fork the process."""
        try:
            # first fork
            pid = os.fork()
            if pid > 0:
                logger.debug('pid greater than 0 first time')
                sys.exit(0)
        except OSError as e:
            logger.error('Error forking process first time')
            sys.exit(1)

        # Change the current working directory to path.
        os.chdir("/")

        # Description: setsid() creates a new session if the calling process is not a process group leader. The calling process is the leader of the new session, the process group leader of the new process group, and has no controlling terminal. The process group ID and session ID of the calling process are set to the PID of the calling process. The calling process will be the only process in this new process group and in this new session.

        # Return Value: On success, the (new) session ID of the calling process is returned. On error, (pid_t) -1 is returned, and errno is set to indicate the error.
        os.setsid()

        # Set the current numeric umask and return the previous umask.
        os.umask(0)

        try:
            # second fork
            pid = os.fork()
            if pid > 0:
                logger.debug('pid greater than 0 second time')
                sys.exit(0)
        except OSError as e:
            logger.error('Error forking process second time')
            sys.exit(1)
