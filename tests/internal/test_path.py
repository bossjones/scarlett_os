# encoding: utf-8

import os
import shutil
import tempfile
import unittest

from gettext import gettext as _

import unittest.mock as mock

import pytest

import scarlett_os
from scarlett_os import compat
from scarlett_os import exceptions
from scarlett_os.internal import path as s_path
from scarlett_os.internal.gi import GLib
from scarlett_os.internal.gi import Gst

import tests

import imp  # Library to help us reload our tasker module


@pytest.fixture(scope='function')
def path_mocker_stopall(mocker):
    "Stop previous mocks, yield mocker plugin obj, then stopall mocks again"
    print('Called [setup]: mocker.stopall()')
    mocker.stopall()
    print('Called [setup]: imp.reload(s_path)')
    imp.reload(s_path)
    yield mocker
    print('Called [teardown]: mocker.stopall()')
    mocker.stopall()
    print('Called [setup]: imp.reload(s_path)')
    imp.reload(s_path)


def bad_read():
    raise UnicodeDecodeError('utf-8', b'0x80', 0, 1, 'invalid start byte')


@pytest.mark.scarlettonly
@pytest.mark.unittest
@pytest.mark.scarlettonlyunittest
@pytest.mark.pathtest
class TestPathToFileURI(object):

    def test_get_parent_dir(self, path_mocker_stopall):
        # mock
        mock_logger_info = path_mocker_stopall.MagicMock(name="mock_logger_info")
        # patch
        path_mocker_stopall.patch.object(scarlett_os.subprocess.logging.Logger, 'info', mock_logger_info)

        path = '/home/pi/dev/bossjones-github/scarlett_os/_debug/generator-player.dot'

        # run test
        result = s_path.get_parent_dir(path)

        assert mock_logger_info.call_count == 1

        mock_logger_info.assert_any_call("get_parent_dir: {}".format(path))
        assert result == '/home/pi/dev/bossjones-github/scarlett_os/_debug'

    def test_mkdir_p(self, path_mocker_stopall):
        # mock
        mock_logger_info = path_mocker_stopall.MagicMock(name="mock_logger_info")
        mock_dir_exists = path_mocker_stopall.MagicMock(name="mock_dir_exists")
        mock_path = path_mocker_stopall.MagicMock(name="mock_path")
        # patch
        path_mocker_stopall.patch.object(scarlett_os.subprocess.logging.Logger, 'info', mock_logger_info)
        path_mocker_stopall.patch.object(scarlett_os.internal.path, 'dir_exists', mock_dir_exists)
        path_mocker_stopall.patch.object(scarlett_os.internal.path, 'Path', mock_path)

        path = '/home/pi/dev/bossjones-github/scarlett_os/_debug'

        mock_dir_exists.return_value = True

        # run test
        s_path.mkdir_p(path)

        # assert
        assert mock_logger_info.call_count == 1
        mock_path.assert_called_once_with(path)
        # from scarlett_os.internal.debugger import dump
        mock_path().mkdir.assert_any_call(parents=True, exist_ok=True)
        mock_logger_info.assert_any_call("Verify mkdir_p ran: {}".format(mock_dir_exists.return_value))

    def test_dir_exists_false(self, path_mocker_stopall):
        # mock
        mock_logger_error = path_mocker_stopall.MagicMock(name="mock_logger_error")
        mock_path = path_mocker_stopall.MagicMock(name="mock_path")
        # patch
        path_mocker_stopall.patch.object(scarlett_os.subprocess.logging.Logger, 'error', mock_logger_error)
        path_mocker_stopall.patch.object(scarlett_os.internal.path, 'Path', mock_path)

        path = '/home/pi/dev/bossjones-github/scarlett_os/_debug'

        mock_path_instance = mock_path()

        mock_path_instance.is_dir.return_value = False

        # run test
        s_path.dir_exists(path)

        # assert
        assert mock_logger_error.call_count == 1
        assert mock_path_instance.is_dir.call_count == 2
        mock_logger_error.assert_any_call("This is not a dir: {}".format(path))

    def test_dir_exists_true(self, path_mocker_stopall):
        # mock
        mock_logger_error = path_mocker_stopall.MagicMock(name="mock_logger_error")
        mock_path = path_mocker_stopall.MagicMock(name="mock_path")
        # patch
        path_mocker_stopall.patch.object(scarlett_os.subprocess.logging.Logger, 'error', mock_logger_error)
        path_mocker_stopall.patch.object(scarlett_os.internal.path, 'Path', mock_path)

        path = '/home/pi/dev/bossjones-github/scarlett_os/_debug'

        mock_path_instance = mock_path()
        #
        mock_path_instance.is_dir.return_value = True

        # run test
        s_path.dir_exists(path)

        # assert
        assert mock_logger_error.call_count == 0
        assert mock_path_instance.is_dir.call_count == 2
        mock_logger_error.assert_not_called()

    def test_mkdir_if_does_not_exist_false(self, path_mocker_stopall):
        # mock
        mock_mkdir_p = path_mocker_stopall.MagicMock(name="mock_mkdir_p")
        mock_dir_exists = path_mocker_stopall.MagicMock(name="mock_dir_exists", return_value=False)
        # patch
        path_mocker_stopall.patch.object(scarlett_os.internal.path, 'mkdir_p', mock_mkdir_p)
        path_mocker_stopall.patch.object(scarlett_os.internal.path, 'dir_exists', mock_dir_exists)

        path = '/home/pi/dev/bossjones-github/scarlett_os/_debug'

        # run test
        result = s_path.mkdir_if_does_not_exist(path)

        # assert
        assert mock_mkdir_p.call_count == 1
        assert mock_dir_exists.call_count == 1
        assert result == True

    def test_mkdir_if_does_not_exist_true(self, path_mocker_stopall):
        # mock
        mock_mkdir_p = path_mocker_stopall.MagicMock(name="mock_mkdir_p")
        mock_dir_exists = path_mocker_stopall.MagicMock(name="mock_dir_exists", return_value=True)
        # patch
        path_mocker_stopall.patch.object(scarlett_os.internal.path, 'mkdir_p', mock_mkdir_p)
        path_mocker_stopall.patch.object(scarlett_os.internal.path, 'dir_exists', mock_dir_exists)

        path = '/home/pi/dev/bossjones-github/scarlett_os/_debug'

        # run test
        result = s_path.mkdir_if_does_not_exist(path)

        # assert
        assert mock_mkdir_p.call_count == 0
        assert mock_dir_exists.call_count == 1
        assert result == False

    def test_fname_exists_true(self, path_mocker_stopall):
        # mock
        mock_path = path_mocker_stopall.MagicMock(name="mock_path")
        # patch
        path_mocker_stopall.patch.object(scarlett_os.internal.path, 'Path', mock_path)

        path = '/home/pi/dev/bossjones-github/scarlett_os/_debug/generator.dot'

        mock_path_instance = mock_path()

        mock_path_instance.exists.return_value = True

        # run test
        result = s_path.fname_exists(path)

        assert mock_path_instance.exists.call_count == 1
        mock_path.assert_any_call(path)
        assert result == True

    def test_fname_exists_false(self, path_mocker_stopall):
        # mock
        mock_path = path_mocker_stopall.MagicMock(name="mock_path")
        # patch
        path_mocker_stopall.patch.object(scarlett_os.internal.path, 'Path', mock_path)

        path = '/home/pi/dev/bossjones-github/scarlett_os/_debug/generator.dot'

        mock_path_instance = mock_path()

        mock_path_instance.exists.return_value = False

        # run test
        result = s_path.fname_exists(path)

        assert mock_path_instance.exists.call_count == 1
        mock_path_instance.exists.assert_called_once_with()
        mock_path.assert_any_call(path)
        assert result == False

    def test_dir_isWritable(self, path_mocker_stopall):
        # mock
        mock_os_access = path_mocker_stopall.MagicMock(name="mock_os_access")
        mock_os_path_isdir = path_mocker_stopall.MagicMock(name="mock_os_path_isdir")
        # patch
        path_mocker_stopall.patch.object(scarlett_os.internal.path.os, 'access', mock_os_access)
        path_mocker_stopall.patch.object(scarlett_os.internal.path.os.path, 'isdir', mock_os_path_isdir)

        path = 'file:///tmp'

        # patch return values
        mock_os_path_isdir.return_value = True
        mock_os_access.return_value = True

        # run test
        result = s_path.isWritable(path)

        # tests
        mock_os_path_isdir.assert_called_once_with('file:///tmp')
        mock_os_access.assert_called_once_with('file:///tmp', os.W_OK)
        assert result == True

    def test_file_isWritable(self, path_mocker_stopall):
        # mock
        mock_os_access = path_mocker_stopall.MagicMock(name="mock_os_access")
        mock_os_path_isdir = path_mocker_stopall.MagicMock(name="mock_os_path_isdir")
        # patch
        path_mocker_stopall.patch.object(scarlett_os.internal.path.os, 'access', mock_os_access)
        path_mocker_stopall.patch.object(scarlett_os.internal.path.os.path, 'isdir', mock_os_path_isdir)

        path = 'file:///tmp/fake_file'

        # patch return values
        mock_os_path_isdir.return_value = False
        mock_os_access.return_value = True

        # run test
        result = s_path.isWritable(path)

        # tests
        mock_os_path_isdir.assert_called_once_with('file:///tmp/fake_file')
        mock_os_access.assert_called_once_with('file:///tmp', os.W_OK)
        assert result == True

    # TODO: Need to figure out how to throw a fake UnicodeDecodeError
    # @mock.patch('scarlett_os.internal.path.os.access')
    # def test_dir_isReadable_unicode_error(self, mock_os_access):
    #     # path = u'\x11/ip/addres\xc5\x82/print\x05first\x06second'
    #     path = u'file:///tmp/fake_file'
    #
    #     # b'\x80abc'.decode("utf-8", "strict")
    #     # tmpdir = tempfile.mkdtemp('.scarlett_os-tests')
    #
    #     mock_os_access.name = 'mock_os_access'
    #     mock_os_access.side_effect = UnicodeDecodeError('', b'', 1, 0, '')
    #
    #     with pytest.raises(UnicodeDecodeError):
    #         result = s_path.isReadable(path)
    #

    def test_dir_isReadable(self):
        tmpdir = tempfile.mkdtemp('.scarlett_os-tests')

        try:
            # run test
            result = s_path.isReadable(tmpdir)

            # tests
            assert result == True
        finally:
            # nuke
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_file_isReadable(self):
        fd_unused, path = tempfile.mkstemp(suffix=".wav")

        try:
            # run test
            result = s_path.isReadable(path)

            # tests
            assert result
        finally:
            os.remove(path)

    def test_unicode_decode_error_isWritable(self, path_mocker_stopall):

        # mock
        mock_os_path_isdir = path_mocker_stopall.MagicMock(name="mock_os_path_isdir")
        mock_os_access = path_mocker_stopall.MagicMock(name="mock_os_access")
        mock_unicode_error_dialog = path_mocker_stopall.MagicMock(name="mock_unicode_error_dialog")
        mock_logger_error = path_mocker_stopall.MagicMock(name="mock_logger_error")

        # patch
        path_mocker_stopall.patch.object(scarlett_os.internal.path.os.path, 'isdir', mock_os_path_isdir)
        path_mocker_stopall.patch.object(scarlett_os.internal.path.os, 'access', mock_os_access)
        path_mocker_stopall.patch.object(scarlett_os.internal.path, 'unicode_error_dialog', mock_unicode_error_dialog)
        path_mocker_stopall.patch.object(scarlett_os.subprocess.logging.Logger, 'error', mock_logger_error)


        path = b'file:///tmp/fake_file'

        # patch return values
        mock_os_path_isdir.side_effect = UnicodeDecodeError('', b'', 1, 0, '')
        s_path.isWritable(path)

        assert mock_unicode_error_dialog.call_count == 1

    def test_unicode_error_dialog(self, path_mocker_stopall):
        # mock
        mock_logger_error = path_mocker_stopall.MagicMock(name="mock_logger_error")
        # patch
        path_mocker_stopall.patch.object(scarlett_os.subprocess.logging.Logger, 'error', mock_logger_error)

        s_path.unicode_error_dialog()

        assert mock_logger_error.call_count == 1

        _message = _("The system's locale that you are using is not UTF-8 capable. "
                     "Unicode support is required for Python3 software like Pitivi. "
                     "Please correct your system settings; if you try to use Pitivi "
                     "with a broken locale, weird bugs will happen.")

        mock_logger_error.assert_any_call(_message)

    def test_path_to_uri(self):
        result = s_path.path_to_uri('/etc/fstab')
        assert result == b'file:///etc/fstab'
        assert type(result) == compat.bytes

    def test_uri_is_valid_bytes(self):
        uri = b'file:///etc/fstab'
        assert s_path.uri_is_valid(uri)

    def test_path_from_uri_bytes(self):
        raw_uri = b'file:///etc/fstab'
        result = s_path.path_from_uri(raw_uri)
        assert result == '/etc/fstab'

    def test_filename_from_uri_bytes(self):
        uri = b'file:///etc/fstab'
        result = s_path.filename_from_uri(uri)
        assert result == 'fstab'

    def test_filename_from_uri_str(self):
        uri = 'file:///etc/fstab'
        result = s_path.filename_from_uri(uri)
        assert result == 'fstab'

    def test_quote_uri_byte_to_str(self):
        uri = b'file:///etc/fstab'
        result = s_path.quote_uri(uri)
        assert result == 'file:///etc/fstab'
        assert type(result) == compat.text_type

    def test_quantize(self):
        result = s_path.quantize(100.00, 3.00)
        assert result == 99.0

    def test_binary_search_EmptyList(self):
        assert s_path.binary_search([], 10) == -1

    def test_binary_search_Existing(self):
        A = [10, 20, 30]
        for index, element in enumerate(A):
            assert s_path.binary_search([10, 20, 30], element) == index

    def test_binary_search_MissingLeft(self):
        assert s_path.binary_search([10, 20, 30], 1) == 0
        assert s_path.binary_search([10, 20, 30], 16) == 1
        assert s_path.binary_search([10, 20, 30], 29) == 2

    def test_binary_search_MissingRight(self):
        assert s_path.binary_search([10, 20, 30], 11) == 0
        assert s_path.binary_search([10, 20, 30], 24) == 1
        assert s_path.binary_search([10, 20, 30], 40) == 2

    def test_uri_to_path_str(self):
        uri = 'file:///etc/fstab'
        result = s_path.uri_to_path(uri)
        assert result == '/etc/fstab'

    def test_uri_to_path_bytes(self):
        uri = b'file:///etc/fstab'
        result = s_path.uri_to_path(uri)
        assert result == '/etc/fstab'

##################################################################################
# Pitivi - BEGIN
##################################################################################
    # def testMakeBackupUri(self):
    #     uri = "file:///tmp/x.xges"
    #     self.assertEqual(uri + "~", self.manager._makeBackupURI(uri))
    #
    # def testBackupProject(self):
    #     self.manager.newBlankProject()
    #
    #     # Assign an uri to the project where it's saved by default.
    #     unused, xges_path = tempfile.mkstemp(suffix=".xges")
    #     uri = "file://" + os.path.abspath(xges_path)
    #     self.manager.current_project.uri = uri
    #     # This is where the automatic backup file is saved.
    #     backup_uri = self.manager._makeBackupURI(uri)
    #
    #     # Save the backup
    #     self.assertTrue(self.manager.saveProject(
    #         self.manager.current_project, backup=True))
    #     self.assertTrue(os.path.isfile(path_from_uri(backup_uri)))
    #
    #     self.manager.closeRunningProject()
    #     self.assertFalse(os.path.isfile(path_from_uri(backup_uri)),
    #                      "Backup file not deleted when project closed")
##################################################################################
# Pitivi - BEGIN
##################################################################################

#     def test_space_in_path(self):
#         result = path.path_to_uri('/tmp/test this')
#         self.assertEqual(result, 'file:///tmp/test%20this')
#
#     def test_unicode_in_path(self):
#         result = path.path_to_uri('/tmp/æøå')
#         self.assertEqual(result, 'file:///tmp/%C3%A6%C3%B8%C3%A5')
#
#     def test_utf8_in_path(self):
#         result = path.path_to_uri('/tmp/æøå'.encode('utf-8'))
#         self.assertEqual(result, 'file:///tmp/%C3%A6%C3%B8%C3%A5')
#
#     def test_latin1_in_path(self):
#         result = path.path_to_uri('/tmp/æøå'.encode('latin-1'))
#         self.assertEqual(result, 'file:///tmp/%E6%F8%E5')
#
#
# class UriToPathTest(unittest.TestCase):
#
#     def test_simple_uri(self):
#         result = path.uri_to_path('file:///etc/fstab')
#         self.assertEqual(result, '/etc/fstab'.encode('utf-8'))
#
#     def test_space_in_uri(self):
#         result = path.uri_to_path('file:///tmp/test%20this')
#         self.assertEqual(result, '/tmp/test this'.encode('utf-8'))
#
#     def test_unicode_in_uri(self):
#         result = path.uri_to_path('file:///tmp/%C3%A6%C3%B8%C3%A5')
#         self.assertEqual(result, '/tmp/æøå'.encode('utf-8'))
#
#     def test_latin1_in_uri(self):
#         result = path.uri_to_path('file:///tmp/%E6%F8%E5')
#         self.assertEqual(result, '/tmp/æøå'.encode('latin-1'))
#
#
# class SplitPathTest(unittest.TestCase):
#
#     def test_empty_path(self):
#         self.assertEqual([], path.split_path(''))
#
#     def test_single_dir(self):
#         self.assertEqual(['foo'], path.split_path('foo'))
#
#     def test_dirs(self):
#         self.assertEqual(['foo', 'bar', 'baz'], path.split_path('foo/bar/baz'))
#
#     def test_initial_slash_is_ignored(self):
#         self.assertEqual(
#             ['foo', 'bar', 'baz'], path.split_path('/foo/bar/baz'))
#
#     def test_only_slash(self):
#         self.assertEqual([], path.split_path('/'))
#
#
# class FindMTimesTest(unittest.TestCase):
#     maxDiff = None
#
#     def setUp(self):  # noqa: N802
#         self.tmpdir = tempfile.mkdtemp(b'.scarlett_os-tests')
#
#     def tearDown(self):  # noqa: N802
#         shutil.rmtree(self.tmpdir, ignore_errors=True)
#
#     def mkdir(self, *args):
#         name = os.path.join(self.tmpdir, *[bytes(a) for a in args])
#         os.mkdir(name)
#         return name
#
#     def touch(self, *args):
#         name = os.path.join(self.tmpdir, *[bytes(a) for a in args])
#         open(name, 'w').close()
#         return name
#
#     def test_names_are_bytestrings(self):
#         """We shouldn't be mixing in unicode for paths."""
#         result, errors = path.find_mtimes(tests.path_to_data_dir(''))
#         for name in list(result.keys()) + list(errors.keys()):
#             self.assertEqual(name, tests.IsA(bytes))
#
#     def test_nonexistent_dir(self):
#         """Non existent search roots are an error"""
#         missing = os.path.join(self.tmpdir, 'does-not-exist')
#         result, errors = path.find_mtimes(missing)
#         self.assertEqual(result, {})
#         self.assertEqual(errors, {missing: tests.IsA(exceptions.FindError)})
#
#     def test_empty_dir(self):
#         """Empty directories should not show up in results"""
#         self.mkdir('empty')
#
#         result, errors = path.find_mtimes(self.tmpdir)
#         self.assertEqual(result, {})
#         self.assertEqual(errors, {})
#
#     def test_file_as_the_root(self):
#         """Specifying a file as the root should just return the file"""
#         single = self.touch('single')
#
#         result, errors = path.find_mtimes(single)
#         self.assertEqual(result, {single: tests.any_int})
#         self.assertEqual(errors, {})
#
#     def test_nested_directories(self):
#         """Searching nested directories should find all files"""
#
#         # Setup foo/bar and baz directories
#         self.mkdir('foo')
#         self.mkdir('foo', 'bar')
#         self.mkdir('baz')
#
#         # Touch foo/file foo/bar/file and baz/file
#         foo_file = self.touch('foo', 'file')
#         foo_bar_file = self.touch('foo', 'bar', 'file')
#         baz_file = self.touch('baz', 'file')
#
#         result, errors = path.find_mtimes(self.tmpdir)
#         self.assertEqual(result, {foo_file: tests.any_int,
#                                   foo_bar_file: tests.any_int,
#                                   baz_file: tests.any_int})
#         self.assertEqual(errors, {})
#
#     def test_missing_permission_to_file(self):
#         """Missing permissions to a file is not a search error"""
#         target = self.touch('no-permission')
#         os.chmod(target, 0)
#
#         result, errors = path.find_mtimes(self.tmpdir)
#         self.assertEqual({target: tests.any_int}, result)
#         self.assertEqual({}, errors)
#
#     def test_missing_permission_to_directory(self):
#         """Missing permissions to a directory is an error"""
#         directory = self.mkdir('no-permission')
#         os.chmod(directory, 0)
#
#         result, errors = path.find_mtimes(self.tmpdir)
#         self.assertEqual({}, result)
#         self.assertEqual({directory: tests.IsA(exceptions.FindError)}, errors)
#
#     def test_symlinks_are_ignored(self):
#         """By default symlinks should be treated as an error"""
#         target = self.touch('target')
#         link = os.path.join(self.tmpdir, 'link')
#         os.symlink(target, link)
#
#         result, errors = path.find_mtimes(self.tmpdir)
#         self.assertEqual(result, {target: tests.any_int})
#         self.assertEqual(errors, {link: tests.IsA(exceptions.FindError)})
#
#     def test_symlink_to_file_as_root_is_followed(self):
#         """Passing a symlink as the root should be followed when follow=True"""
#         target = self.touch('target')
#         link = os.path.join(self.tmpdir, 'link')
#         os.symlink(target, link)
#
#         result, errors = path.find_mtimes(link, follow=True)
#         self.assertEqual({link: tests.any_int}, result)
#         self.assertEqual({}, errors)
#
#     def test_symlink_to_directory_is_followed(self):
#         pass
#
#     def test_symlink_pointing_at_itself_fails(self):
#         """Symlink pointing at itself should give as an OS error"""
#         link = os.path.join(self.tmpdir, 'link')
#         os.symlink(link, link)
#
#         result, errors = path.find_mtimes(link, follow=True)
#         self.assertEqual({}, result)
#         self.assertEqual({link: tests.IsA(exceptions.FindError)}, errors)
#
#     def test_symlink_pointing_at_parent_fails(self):
#         """We should detect a loop via the parent and give up on the branch"""
#         os.symlink(self.tmpdir, os.path.join(self.tmpdir, 'link'))
#
#         result, errors = path.find_mtimes(self.tmpdir, follow=True)
#         self.assertEqual({}, result)
#         self.assertEqual(1, len(errors))
#         self.assertEqual(tests.IsA(Exception), list(errors.values())[0])
#
#     def test_indirect_symlink_loop(self):
#         """More indirect loops should also be detected"""
#         # Setup tmpdir/directory/loop where loop points to tmpdir
#         directory = os.path.join(self.tmpdir, b'directory')
#         loop = os.path.join(directory, b'loop')
#
#         os.mkdir(directory)
#         os.symlink(self.tmpdir, loop)
#
#         result, errors = path.find_mtimes(self.tmpdir, follow=True)
#         self.assertEqual({}, result)
#         self.assertEqual({loop: tests.IsA(Exception)}, errors)
#
#     def test_symlink_branches_are_not_excluded(self):
#         """Using symlinks to make a file show up multiple times should work"""
#         self.mkdir('directory')
#         target = self.touch('directory', 'target')
#         link1 = os.path.join(self.tmpdir, b'link1')
#         link2 = os.path.join(self.tmpdir, b'link2')
#
#         os.symlink(target, link1)
#         os.symlink(target, link2)
#
#         expected = {target: tests.any_int,
#                     link1: tests.any_int,
#                     link2: tests.any_int}
#
#         result, errors = path.find_mtimes(self.tmpdir, follow=True)
#         self.assertEqual(expected, result)
#         self.assertEqual({}, errors)
#
#     def test_gives_mtime_in_milliseconds(self):
#         fname = self.touch('foobar')
#
#         os.utime(fname, (1, 3.14159265))
#
#         result, errors = path.find_mtimes(fname)
#
#         self.assertEqual(len(result), 1)
#         mtime, = list(result.values())
#         self.assertEqual(mtime, 3141)
#         self.assertEqual(errors, {})
#
#
# class TestIsPathInsideBaseDir(object):
#     def test_when_inside(self):
#         assert path.is_path_inside_base_dir(
#             '/æ/øå'.encode('utf-8'),
#             '/æ'.encode('utf-8'))
#
#     def test_when_outside(self):
#         assert not path.is_path_inside_base_dir(
#             '/æ/øå'.encode('utf-8'),
#             '/ø'.encode('utf-8'))
#
#     def test_byte_inside_str_fails(self):
#         with pytest.raises(ValueError):
#             path.is_path_inside_base_dir('/æ/øå'.encode('utf-8'), '/æ')
#
#     def test_str_inside_byte_fails(self):
#         with pytest.raises(ValueError):
#             path.is_path_inside_base_dir('/æ/øå', '/æ'.encode('utf-8'))
#
#     def test_str_inside_str_fails(self):
#         with pytest.raises(ValueError):
#             path.is_path_inside_base_dir('/æ/øå', '/æ')
#
#
# # TODO: kill this in favour of just os.path.getmtime + mocks
# class MtimeTest(unittest.TestCase):
#
#     def tearDown(self):  # noqa: N802
#         path.mtime.undo_fake()
#
#     def test_mtime_of_current_dir(self):
#         mtime_dir = int(os.stat('.').st_mtime)
#         self.assertEqual(mtime_dir, path.mtime('.'))
#
#     def test_fake_time_is_returned(self):
#         path.mtime.set_fake_time(123456)
#         self.assertEqual(path.mtime('.'), 123456)
