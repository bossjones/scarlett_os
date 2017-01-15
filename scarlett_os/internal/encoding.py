# -*- coding: utf-8 -*-

"""
scarlett_os.internal.encoding
~~~~~~~~~~~~~~
Provides utility functions that are consumed internally by ScarlettOS
which depend on extremely few external helpers (such as compat)
"""

import locale
import codecs

from scarlett_os import compat
# from .compat import is_py2, builtin_str, str

# NOTE: python 3 convert byte string variable to regular string
# http://stackoverflow.com/questions/31058055/python-3-convert-byte-string-variable-to-regular-string


def bytesting_to_string(a_bytestring):
    # If we have a byte instead of a strng, decode to str type
    if isinstance(a_bytestring, compat.bytes):
        a_bytestring = a_bytestring.decode('utf-8')

    return a_bytestring

# def locale_decode(bytestr):
#     try:
#         return compat.text_type(bytestr)
#     except UnicodeError:
#         # char = chr(bytestr)
#         # python Only, we don't need to cast
#         return bytestr.decode(locale.getpreferredencoding())

def locale_decode(bytestr):
    # try:
        # PY2: text_type = unicode  # noqa
        # In [8]: unicode(bytestr)
        # ---------------------------------------------------------------------------
        # UnicodeDecodeError                        Traceback (most recent call last)
        # <ipython-input-8-819e1ae0f3d4> in <module>()
        # ----> 1 unicode(bytestr)
        #
        # UnicodeDecodeError: 'ascii' codec can't decode byte 0xe9 in position 20: ordinal not in range(128)

        # PY3: text_type = str
        #      str(bytestr) = "b'[Errno 98] Adresse d\\xe9j\\xe0 utilis\\xe9e'"
    return compat.text_type(bytestr)
    # except UnicodeError:
    #     return bytes(bytestr).decode(locale.getpreferredencoding())

# # source: https://github.com/audreyr/cookiecutter/blob/ea987b0edba1b317385de07ab2e65d0d07503098/tests/test_preferred_encoding.py
# def get_preferred_encoding():
#     """Make sure that the systems preferred encoding is not `ascii`.
#     Otherwise `click` is raising a RuntimeError for Python3. For a detailed
#     description of this very problem please consult the following gist:
#     https://gist.github.com/hackebrot/937245251887197ef542
#     This test also checks that `tox.ini` explicitly copies the according
#     system environment variables to the test environments.
#     """
#     try:
#         preferred_encoding = locale.getpreferredencoding()
#         fs_enc = codecs.lookup(preferred_encoding).name
#     except Exception:
#         fs_enc = 'ascii'
#     assert fs_enc != 'ascii'


# def not_ascii():
#     try:
#         return compat.text_type(bytestr)
#     except UnicodeError:
#         # char = chr(bytestr)
#         return bytes(bytestr).decode(locale.getpreferredencoding())

# from .compat import is_py2, builtin_str, str

def to_native_string(string, encoding='ascii'):
    """Given a string object, regardless of type, returns a representation of
    that string in the native string type, encoding and decoding where
    necessary. This assumes ASCII unless told otherwise.
    """
    # NOTE: @source: https://github.com/kennethreitz/requests/blob/5c4549493b35f5dbb084d029eaf12b6c7ce22579/requests/_internal_utils.py
    if isinstance(string, compat.text_type):
        out = string
    else:
        # if is_py2:
        #     out = string.encode(encoding)
        # else:
        out = string.decode(encoding)

    return out


def unicode_is_ascii(u_string):
    """Determine if unicode string only contains ASCII characters.
    :param str u_string: unicode string to check. Must be unicode
        and not Python 2 `str`.
    :rtype: bool
    """
    assert isinstance(u_string, compat.text_type)
    try:
        u_string.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False
