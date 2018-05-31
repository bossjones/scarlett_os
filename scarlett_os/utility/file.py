# -*- coding: utf-8 -*-

from __future__ import with_statement, division

from scarlett_os.compat import os
from scarlett_os.compat import errno
from scarlett_os.compat import environ
from scarlett_os.compat import text_type
from scarlett_os.compat import _FSCODING


def format_size(size):
    """Turn an integer size value into something human-readable."""
    # TODO: Better i18n of this (eg use O/KO/MO/GO in French)
    if size >= 1024 ** 3:
        return "%.1f GB" % (float(size) / (1024 ** 3))
    elif size >= 1024 ** 2 * 100:
        return "%.0f MB" % (float(size) / (1024 ** 2))
    elif size >= 1024 ** 2 * 10:
        return "%.1f MB" % (float(size) / (1024 ** 2))
    elif size >= 1024 ** 2:
        return "%.2f MB" % (float(size) / (1024 ** 2))
    elif size >= 1024 * 10:
        return "%d KB" % int(size / 1024)
    elif size >= 1024:
        return "%.2f KB" % (float(size) / 1024)
    else:
        return "%d B" % size


def mkdir(dir_, *args):  # noqa
    """Make a directory, including all its parent directories. This does not
    raise an exception if the directory already exists (and is a
    directory)."""

    try:
        os.makedirs(dir_, *args)
    except OSError as e:
        if e.errno != errno.EEXIST or not os.path.isdir(dir_):
            raise

def iscommand(s):  # noqa
    """True if an executable file `s` exists in the user's path, or is a
    fully qualified and existing executable file."""

    if s == "" or os.path.sep in s:
        return os.path.isfile(s) and os.access(s, os.X_OK)
    else:
        s = s.split()[0]
        path = environ.get('PATH', '') or os.defpath
        for p in path.split(os.path.pathsep):
            p2 = os.path.join(p, s)
            if os.path.isfile(p2) and os.access(p2, os.X_OK):
                return True
        else:
            return False


def is_fsnative(path):
    """Check if file system native"""
    return isinstance(path, bytes)


def fsnative(path=u""):
    """File system native"""
    assert isinstance(path, text_type)
    return path.encode(_FSCODING, 'replace')


def listdir(path, hidden=False):
    """List files in a directory, sorted, fully-qualified.

    If hidden is false, Unix-style hidden files are not returned.
    """

    assert is_fsnative(path)

    if hidden:
        filt = None
    else:
        filt = lambda base: not base.startswith(".")  # noqa
    if path.endswith(os.sep):
        join = "".join
    else:
        join = os.sep.join
    return [join([path, basename])
            for basename in sorted(os.listdir(path))
            if filt(basename)]


def mtime(filename):
    """Return the mtime of a file, or 0 if an error occurs."""
    try:
        return os.path.getmtime(filename)
    except OSError:
        return 0


def filesize(filename):
    """Return the size of a file, or 0 if an error occurs."""
    try:
        return os.path.getsize(filename)
    except OSError:
        return 0


def expanduser(filename):  # noqa
    """convience function to have expanduser return wide character paths
    """
    return os.path.expanduser(filename)


def unexpand(filename, HOME=expanduser("~")):
    """Replace the user's home directory with ~/, if it appears at the
    start of the path name."""
    sub = (os.name == "nt" and "%USERPROFILE%") or "~"
    if filename == HOME:
        return sub
    elif filename.startswith(HOME + os.path.sep):
        filename = filename.replace(HOME, sub, 1)
    return filename


def get_home_dir():
    """Returns the root directory of the user, /home/user"""
    return expanduser("~")
