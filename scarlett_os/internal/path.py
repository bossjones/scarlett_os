"""Scarlett path module. Deals with all things at the file system level."""

import logging
import os
import stat
import threading
import bisect

from scarlett_os import compat
from scarlett_os import exceptions

from scarlett_os.internal import encoding

from scarlett_os.internal.gi import Gst

from gettext import gettext as _

# import pathlib

from pathlib import Path
# from pathlib import PurePosixPath

# p = PurePosixPath('/etc/passwd')
# Path('path/to/file.txt').touch()


logger = logging.getLogger(__name__)


def get_parent_dir(path):
    logger.info("get_parent_dir: {}".format(path))
    # In [13]: q.parent
    # Out[13]: PosixPath('/home/pi/dev/bossjones-github/scarlett_os/_debug')
    p = Path(path)
    return p.parent.__str__()


def mkdir_p(path):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    d = dir_exists(path)
    logger.info("Verify mkdir_p ran: {}".format(d))


def dir_exists(path):
    p = Path(path)
    if not p.is_dir():
        logger.error("This is not a dir: {}".format(path))
        # NOTE this should raise a exception
    return p.is_dir()


def mkdir_if_does_not_exist(path):
    if not dir_exists(path):
        mkdir_p(path)
        return True
    return False


def fname_exists(path):
    p = Path(path)
    return p.exists()


def touch_empty_file(path):
    if fname_exists(path):
        logger.info("File already exists: {}".format(path))
    p = Path(path)
    return p.touch()

# NOTE: Borrowed from Pitivi
# ------------------------------ URI helpers --------------------------------
# SOURCE: https://raw.githubusercontent.com/GNOME/pitivi/b2bbe6eef6d1e6d0fa5471d60004c62f936b3146/pitivi/utils/misc.py


def isWritable(path):
    """Returns whether the file/path is writable."""
    try:
        if os.path.isdir(path):
            # The given path is an existing directory.
            # To properly check if it is writable, you need to use os.access.
            return os.access(path, os.W_OK)
        else:
            # The given path is supposed to be a file.
            # Avoid using open(path, "w"), as it might corrupt existing files.
            # And yet, even if the parent directory is actually writable,
            # open(path, "rw") will IOError if the file doesn't already exist.
            # Therefore, simply check the directory permissions instead:

            # path = 'file:///etc/fstab'
            # In [22]: os.path.dirname(path)
            # Out[22]: 'file:///etc'
            return os.access(os.path.dirname(path), os.W_OK)
            # In [23]: os.access(os.path.dirname(path), os.W_OK)
            # Out[23]: False
    except UnicodeDecodeError:
        unicode_error_dialog()


def isReadable(path):
    """Returns whether the file/path exists and is readable."""
    try:
        return (os.path.exists(path) and os.access(path, os.R_OK))
    except UnicodeDecodeError:
        unicode_error_dialog()


def unicode_error_dialog():
    message = _("The system's locale that you are using is not UTF-8 capable. "
                "Unicode support is required for Python3 software like Pitivi. "
                "Please correct your system settings; if you try to use Pitivi "
                "with a broken locale, weird bugs will happen.")

    logger.error(message)


def uri_is_valid(uri):
    """Checks if the specified URI is usable (of type file://).

    Will also check if the size is valid (> 0).

    Args:
        uri (str): The location to check.

    Return:
        (boolean): True if valid, False otherwise.
    """

    # If we have a byte instead of a strng, decode to str type
    if isinstance(uri, compat.bytes):
        uri = uri.decode('utf-8')

    return (Gst.uri_is_valid(uri) and
            Gst.uri_get_protocol(uri) == "file" and
            len(os.path.basename(Gst.uri_get_location(uri))) > 0)


def path_from_uri(raw_uri):
    """Returns a path that can be used with Python's os.path.

    Args:
        raw_uri (str, byte): The location to check.

    Return:
        (str): String containting path to file.
    """
    # NOTE: bossjones added
    # If we have a byte instead of a strng, decode to str type
    if isinstance(raw_uri, compat.bytes):
        raw_uri = raw_uri.decode('utf-8')

    # assume: uri = b'file:///etc/fstab'
    uri = compat.urlparse(raw_uri)
    # In [14]: compat.urlparse(uri)
    # Out[14]: ParseResultBytes(scheme=b'file', netloc=b'', path=b'/etc/fstab', params=b'', query=b'', fragment=b'')
    assert uri.scheme == "file"
    # In [32]: compat.unquote(uri.path)
    # Out[32]: '/etc/fstab'
    return compat.unquote(uri.path)


def filename_from_uri(uri):
    """Returns a filename for display.

    Excludes the path to the file.

    Can be used in UI elements or to shorten debug statements.

    Args:
        uri (str, byte): Uri containing path to file (of type file://).

    Returns:
        (str): String containing file name from uri.
    """
    return os.path.basename(path_from_uri(uri))


def quote_uri(uri):
    """Encodes a URI according to RFC 2396.

    Does not touch the file:/// part.

    Args:
        uri (str, byte): Uri
    Returns:
        (str): string of uri

    """
    # NOTE: bossjones added
    # If we have a byte instead of a strng, decode to str type
    if isinstance(uri, compat.bytes):
        uri = uri.decode('utf-8')

    # Split off the "file:///" part, if present.
    # In [34]: uri = 'file:///etc/fstab'
    #
    # In [35]: compat.urlsplit(uri, allow_fragments=False)
    # Out[35]: SplitResult(scheme='file', netloc='', path='/etc/fstab', query='', fragment='')
    parts = compat.urlsplit(uri, allow_fragments=False)
    # Make absolutely sure the string is unquoted before quoting again!
    # In [46]: raw_path = compat.unquote(parts.path)
    #
    # In [47]: raw_path
    # Out[47]: '/etc/fstab'
    raw_path = compat.unquote(parts.path)
    # For computing thumbnail md5 hashes in the media library, we must adhere to
    # RFC 2396. It is quite tricky to handle all corner cases, leave it to Gst:
    return Gst.filename_to_uri(raw_path)
    # In [48]: Gst.filename_to_uri(raw_path)
    # Out[48]: 'file:///etc/fstab'


def quantize(input, interval):
    # In Python 3, they made the / operator do a floating-point division, and added the // operator to do integer division (i.e. quotient without remainder);
    return (input // interval) * interval


def binary_search(elements, value):
    """Returns the index of the element closest to value.

    Args:
        elements (List): A sorted list.
    """
    if not elements:
        return -1
    closest_index = bisect.bisect_left(elements, value, 0, len(elements) - 1)
    element = elements[closest_index]
    closest_distance = abs(element - value)
    if closest_distance == 0:
        return closest_index
    for index in (closest_index - 1,):
        if index < 0:
            continue
        distance = abs(elements[index] - value)
        if closest_distance > distance:
            closest_index = index
            closest_distance = distance
    return closest_index

# ------------------------------ URI helpers --------------------------------


# def get_or_create_dir(dir_path):
#     if not isinstance(dir_path, bytes):
#         raise ValueError('Path is not a bytestring.')
#     dir_path = expand_path(dir_path)
#     if os.path.isfile(dir_path):
#         raise OSError(
#             'A file with the same name as the desired dir, '
#             '"%s", already exists.' % dir_path)
#     elif not os.path.isdir(dir_path):
#         logger.info('Creating dir %s', dir_path)
#         os.makedirs(dir_path, 0o755)
#     return dir_path
#
#
# def get_or_create_file(file_path, mkdir=True, content=None):
#     if not isinstance(file_path, bytes):
#         raise ValueError('Path is not a bytestring.')
#     file_path = expand_path(file_path)
#     if isinstance(content, compat.text_type):
#         content = content.encode('utf-8')
#     if mkdir:
#         get_or_create_dir(os.path.dirname(file_path))
#     if not os.path.isfile(file_path):
#         logger.info('Creating file %s', file_path)
#         with open(file_path, 'wb') as fh:
#             if content is not None:
#                 fh.write(content)
#     return file_path


def path_to_uri(path):
    """
    Convert OS specific path to file:// URI.
    Accepts either unicode strings or bytestrings. The encoding of any
    bytestring will be maintained so that :func:`uri_to_path` can return the
    same bytestring.
    Returns a file:// URI as an unicode string.
    """
    if isinstance(path, compat.text_type):
        path = path.encode('utf-8')  # str -> bytes
    # path = compat.quote(path)
    # urlunsplit: Combine the elements of a tuple as returned by urlsplit() into a complete URL as a string.
    # The parts argument can be any five-item iterable. This may result in a slightly different,
    # but equivalent URL, if the URL that was parsed originally had unnecessary delimiters
    # (for example, a ? with an empty query; the RFC states that these are equivalent).
    # NOTE: urlunsplit expects 5 args of type bytes

    # In [52]: uri = b'/etc/fstab'
    #
    # In [53]: compat.urlunsplit((b'file', b'', uri, b'', b''))
    # Out[53]: b'file:///etc/fstab'

    return compat.urlunsplit((b'file', b'', path, b'', b''))


def uri_to_path(uri):
    """
    Convert an URI to a OS specific path.

    Returns a bytestring, since the file path can contain chars with other
    encoding than UTF-8.

    If we had returned these paths as unicode strings, you wouldn't be able to
    look up the matching dir or file on your file system because the exact path
    would be lost by ignoring its encoding.
    """
    # convert str to byte
    if isinstance(uri, compat.text_type):
        uri = uri.encode('utf-8')

        # logger.debug('URI:')
        # logger.debug(uri)
        # In [6]: compat.urlsplit(uri)
        # Out[6]: SplitResultBytes(scheme=b'file', netloc=b'', path=b'/etc/fstab', query=b'', fragment=b'')
        # In [7]: compat.urlsplit(uri).path
        # Out[7]: b'/etc/fstab'
    _path = compat.urlsplit(uri).path

    if isinstance(_path, compat.bytes):
        _path = _path.decode('utf-8')

    return compat.unquote(_path)


# def split_path(path):
#     parts = []
#     while True:
#         path, part = os.path.split(path)
#         if part:
#             parts.insert(0, part)
#         if not path or path == b'/':
#             break
#     return parts


# def expand_path(path):
#     # TODO: document as we want people to use this.
#     if not isinstance(path, bytes):
#         raise ValueError('Path is not a bytestring.')
#     try:
#         path = string.Template(path).substitute(XDG_DIRS)
#     except KeyError:
#         return None
#     path = os.path.expanduser(path)
#     path = os.path.abspath(path)
#     return path


def _find_worker(relative, follow, done, work, results, errors):  # pragma: no cover
    """Worker thread for collecting stat() results.

    :param str relative: directory to make results relative to
    :param bool follow: if symlinks should be followed
    :param threading.Event done: event indicating that all work has been done
    :param queue.Queue work: queue of paths to process
    :param dict results: shared dictionary for storing all the stat() results
    :param dict errors: shared dictionary for storing any per path errors
    """
    while not done.is_set():
        try:
            entry, parents = work.get(block=False)
        except compat.queue.Empty:
            continue

        if relative:
            path = os.path.relpath(entry, relative)
        else:
            path = entry

        try:
            if follow:
                st = os.stat(entry)
            else:
                st = os.lstat(entry)

            if (st.st_dev, st.st_ino) in parents:
                errors[path] = exceptions.FindError('Sym/hardlink loop found.')
                continue

            parents = parents + [(st.st_dev, st.st_ino)]
            if stat.S_ISDIR(st.st_mode):
                for e in os.listdir(entry):
                    work.put((os.path.join(entry, e), parents))
            elif stat.S_ISREG(st.st_mode):
                results[path] = st
            elif stat.S_ISLNK(st.st_mode):
                errors[path] = exceptions.FindError('Not following symlinks.')
            else:
                errors[path] = exceptions.FindError('Not a file or directory.')

        except OSError as e:
            errors[path] = exceptions.FindError(
                encoding.locale_decode(e.strerror), e.errno)
        finally:
            work.task_done()


def _find(root, thread_count=10, relative=False, follow=False):  # pragma: no cover
    """Threaded find implementation that provides stat results for files.

    Tries to protect against sym/hardlink loops by keeping an eye on parent
    (st_dev, st_ino) pairs.

    :param str root: root directory to search from, may not be a file
    :param int thread_count: number of workers to use, mainly useful to
        mitigate network lag when scanning on NFS etc.
    :param bool relative: if results should be relative to root or absolute
    :param bool follow: if symlinks should be followed
    """
    threads = []
    results = {}
    errors = {}
    done = threading.Event()
    work = compat.queue.Queue()
    work.put((os.path.abspath(root), []))

    if not relative:
        root = None

    args = (root, follow, done, work, results, errors)
    for i in range(thread_count):
        t = threading.Thread(target=_find_worker, args=args)
        t.daemon = True
        t.start()
        threads.append(t)

    work.join()
    done.set()
    for t in threads:
        t.join()
    return results, errors


def find_mtimes(root, follow=False):  # pragma: no cover
    results, errors = _find(root, relative=False, follow=follow)
    # return the mtimes as integer milliseconds
    mtimes = {f: int(st.st_mtime * 1000) for f, st in list(results.items())}
    return mtimes, errors


def is_path_inside_base_dir(path, base_path):  # pragma: no cover
    if not isinstance(path, bytes):
        raise ValueError('path is not a bytestring')
    if not isinstance(base_path, bytes):
        raise ValueError('base_path is not a bytestring')

    if path.endswith(os.sep):
        raise ValueError('Path %s cannot end with a path separator'
                         % path)
    # Expand symlinks
    real_base_path = os.path.realpath(base_path)
    real_path = os.path.realpath(path)

    if os.path.isfile(path):
        # Use dir of file for prefix comparision, so we don't accept
        # /tmp/foo.m3u as being inside /tmp/foo, simply because they have a
        # common prefix, /tmp/foo, which matches the base path, /tmp/foo.
        real_path = os.path.dirname(real_path)

    # Check if dir of file is the base path or a subdir
    common_prefix = os.path.commonprefix([real_base_path, real_path])
    return common_prefix == real_base_path


# FIXME replace with mock usage in tests.
class Mtime(object):  # pragma: no cover

    def __init__(self):
        self.fake = None

    def __call__(self, path):
        if self.fake is not None:
            return self.fake
        return int(os.stat(path).st_mtime)

    def set_fake_time(self, time):
        self.fake = time

    def undo_fake(self):
        self.fake = None

mtime = Mtime()
