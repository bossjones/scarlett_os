from __future__ import absolute_import, unicode_literals

import locale

from scarlett_os import compat

# NOTE: python 3 convert byte string variable to regular string
# http://stackoverflow.com/questions/31058055/python-3-convert-byte-string-variable-to-regular-string


def locale_decode(bytestr):
    try:
        return compat.text_type(bytestr)
    except UnicodeError:
        return bytes(bytestr).decode(locale.getpreferredencoding())
