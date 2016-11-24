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

        types = map(type, command)
        if not (min(types) == max(types) == str):
            raise TypeError("executables and arguments must be str objects")
        logger.debug("Running %r" % " ".join(command))

        self.command = command
        self.name = name
        self.forked = fork

        logger.debug("command: ".format(self.command))
        logger.debug("name: ".format(self.name))
        logger.debug("forked: ".format(self.forked))
        logger.debug("process: ".format(self.process))
        logger.debug("pid: ".format(self.pid))

        if fork:
            self.fork()

    def run(self):
        """Run the process."""

        # NOTE: DO_NOT_REAP_CHILD: the child will not be automatically reaped;
        # you must use g_child_watch_add yourself (or call waitpid or handle `SIGCHLD` yourself),
        # or the child will become a zombie.
        # source:
        # http://valadoc.org/#!api=glib-2.0/GLib.SpawnFlags.DO_NOT_REAP_CHILD

        # NOTE: SEARCH_PATH: argv[0] need not be an absolute path, it will be looked for in the userâ€™s PATH
        # source:
        # http://lazka.github.io/pgi-docs/#GLib-2.0/flags.html#GLib.SpawnFlags.SEARCH_PATH

        self.pid, self.stdin, self.stdout, self.stderr = GLib.spawn_async(self.command,
                                                                          flags=GLib.SpawnFlags.SEARCH_PATH | GLib.SpawnFlags.DO_NOT_REAP_CHILD
                                                                          )

        logger.debug("command: ".format(self.command))
        logger.debug("stdin: ".format(self.stdin))
        logger.debug("stdout: ".format(self.stdout))
        logger.debug("stderr: ".format(self.stderr))
        logger.debug("pid: ".format(self.pid))

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
                sys.exit(0)
        except OSError as e:
            sys.exit(1)

        os.chdir("/")
        os.setsid()
        os.umask(0)

        try:
            # second fork
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.exit(1)
