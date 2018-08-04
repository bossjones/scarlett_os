
import imp
import unittest
import unittest.mock as mock

import pytest

import scarlett_os
from scarlett_os.internal import encoding


@pytest.fixture(scope="function")
def encoding_mocker_stopall(mocker):
    "Stop previous mocks, yield mocker plugin obj, then stopall mocks again"
    print("Called [setup]: mocker.stopall()")
    mocker.stopall()
    print("Called [setup]: imp.reload(encoding)")
    imp.reload(encoding)
    yield mocker
    print("Called [teardown]: mocker.stopall()")
    mocker.stopall()
    print("Called [setup]: imp.reload(encoding)")
    imp.reload(encoding)


# ipdb> str(bytestr)
# "b'[Errno 98] Adresse d\\xe9j\\xe0 utilis\\xe9e'"


class TestLocaleDecode(object):
    def test_can_decode_utf8_strings_with_french_content(self, encoding_mocker_stopall):
        # mock
        mock_getpreferredencoding = encoding_mocker_stopall.MagicMock(
            name="mock_getpreferredencoding"
        )
        # patch
        encoding_mocker_stopall.patch.object(
            scarlett_os.internal.encoding.locale,
            "getpreferredencoding",
            mock_getpreferredencoding,
        )

        mock.return_value = "UTF-8"

        # source: http://pythoncentral.io/encoding-and-decoding-strings-in-python-3-x/
        # NOTE: In Python 2.x, prefixing a string literal with a "b" (or "B") is legal syntax, but it does nothing special:
        # NOTE: In Python 3.x, however, this prefix indicates the string is a bytes object which differs from the normal string (which as we know is by default a Unicode string), and even the 'b' prefix is preserved:
        result = encoding.locale_decode(
            b"[Errno 98] Adresse d\xc3\xa9j\xc3\xa0 utilis\xc3\xa9e"
        )

        assert (
            "b'[Errno 98] Adresse d\\xc3\\xa9j\\xc3\\xa0 utilis\\xc3\\xa9e'" == result
        )

    # def test_can_decode_an_ioerror_with_french_content(self, mock):
    #     mock.return_value = 'UTF-8'
    #
    #     error = IOError(98, b'Adresse d\xc3\xa9j\xc3\xa0 utilis\xc3\xa9e')
    #     result = encoding.locale_decode(error)
    #     expected = '[Errno 98] Adresse d\xe9j\xe0 utilis\xe9e'
    #
    #     self.assertEqual(
    #         expected, result,
    #         '%r decoded to %r does not match expected %r' % (
    #             error, result, expected))
    #
    # def test_does_not_use_locale_to_decode_unicode_strings(self, mock):
    #     mock.return_value = 'UTF-8'
    #
    #     encoding.locale_decode('abc')
    #
    #     self.assertFalse(mock.called)
    #
    # def test_does_not_use_locale_to_decode_ascii_bytestrings(self, mock):
    #     mock.return_value = 'UTF-8'
    #
    #     encoding.locale_decode('abc')
    #
    #     self.assertFalse(mock.called)
