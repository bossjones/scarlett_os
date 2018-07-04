#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_package
----------------------------------

Tests for `scarlett_os` module.
"""

# import ipdb

# import mock
import builtins
import imp
import os
import signal
import sys
import unittest
import unittest.mock as mock

# import threading
import pytest

import scarlett_os
from scarlett_os.tools import package  # Module with our thing to test

from contextlib import contextmanager

# source: https://github.com/YosaiProject/yosai/blob/master/test/isolated_tests/core/conf/conftest.py
# FIXME: Since we currently have an issue with mocks leaking into other tests,
# this fixture ensures that we isolate the patched object, stop mocks,
# and literally re-import modules to set environment back to normal.
# It's possible this will all get fixed when we upgrade to a later version of python past 3.5.2
@pytest.fixture(scope='function')
def package_unit_mocker_stopall(mocker):
    "Stop previous mocks, yield mocker plugin obj, then stopall mocks again"
    print('Called [setup]: mocker.stopall()')
    mocker.stopall()
    print('Called [setup]: imp.reload(package)')
    imp.reload(package)
    yield mocker
    print('Called [teardown]: mocker.stopall()')
    mocker.stopall()
    print('Called [setup]: imp.reload(package)')
    imp.reload(package)

# SOURCE: https://github.com/ansible/ansible/blob/370a7ace4b3c8ffb6187900f37499990f1b976a2/test/units/module_utils/basic/test_atomic_move.py
@pytest.fixture
def sys_and_site_mocks(package_unit_mocker_stopall):
    environ = dict()
    mocks = {
        # 'environ': package_unit_mocker_stopall.patch('scarlett_os.tools.package.os.environ', environ),
        # 'getlogin': package_unit_mocker_stopall.patch('scarlett_os.tools.package.os.getlogin'),
        # 'getuid': package_unit_mocker_stopall.patch('scarlett_os.tools.package.os.getuid'),
        # 'getpass': package_unit_mocker_stopall.patch('scarlett_os.tools.package.getpass')
    }

    # mocks['getlogin'].return_value = 'root'
    # mocks['getuid'].return_value = 0
    # mocks['getpass'].getuser.return_value = 'root'

    # mocks['environ']['LOGNAME'] = 'root'
    # mocks['environ']['USERNAME'] = 'root'
    # mocks['environ']['USER'] = 'root'
    # mocks['environ']['LNAME'] = 'root'

    yield mocks


@pytest.fixture
def fake_stat(package_unit_mocker_stopall):
    stat1 = package_unit_mocker_stopall.MagicMock()
    stat1.st_mode = 0o0644
    stat1.st_uid = 0
    stat1.st_gid = 0
    yield stat1

@pytest.mark.unittest
@pytest.mark.scarlettonly
@pytest.mark.scarlettonlyunittest
class TestPackage(object):

    # @contextmanager
    # def assertNotRaises(self, exc_type):
    #     try:
    #         yield None
    #     except exc_type:
    #         raise self.failureException('{} raised'.format(exc_type.__name__))

    # pytest -s -p no:timeout -k test_get_uniq_list --pdb
    def test_get_uniq_list(self, sys_and_site_mocks):
        seq = ['/usr/local/share/jhbuild/sitecustomize', '/usr/lib/python3.5/dist-packages', '/usr/lib/python3.5/site-packages']

        assert scarlett_os.tools.package.get_uniq_list(seq) == ['/usr/local/share/jhbuild/sitecustomize', '/usr/lib/python3.5/dist-packages', '/usr/lib/python3.5/site-packages']

    def test_get_uniq_list_with_dups(self, sys_and_site_mocks):
        seq = ['/usr/local/share/jhbuild/sitecustomize', '/usr/lib/python3.5/dist-packages', '/usr/lib/python3.5/site-packages', '/usr/local/share/jhbuild/sitecustomize', '/usr/lib/python3.5/dist-packages', '/usr/lib/python3.5/site-packages', '/usr/local/share/jhbuild/sitecustomize', '/usr/lib/python3.5/dist-packages', '/usr/lib/python3.5/site-packages', '/usr/local/share/jhbuild/sitecustomize', '/usr/lib/python3.5/dist-packages', '/usr/lib/python3.5/site-packages']

        assert scarlett_os.tools.package.get_uniq_list(seq) == ['/usr/local/share/jhbuild/sitecustomize', '/usr/lib/python3.5/dist-packages', '/usr/lib/python3.5/site-packages']

    def test_check_gi(self, sys_and_site_mocks, package_unit_mocker_stopall):
        sys_and_site_mocks['gi'] = package_unit_mocker_stopall.patch('scarlett_os.tools.package.get_gi_module')
        sys_and_site_mocks['add_gi_packages'] = package_unit_mocker_stopall.patch('scarlett_os.tools.package.add_gi_packages')

        # Since everythin is valid, we should not get any type of warning at all
        with pytest.warns(None) as record:
            scarlett_os.tools.package.check_gi()

        assert len(record) == 0

    def test_check_gi_import_error(self, sys_and_site_mocks, package_unit_mocker_stopall):
        sys_and_site_mocks['gi'] = package_unit_mocker_stopall.patch('scarlett_os.tools.package.get_gi_module')
        sys_and_site_mocks['add_gi_packages'] = package_unit_mocker_stopall.patch('scarlett_os.tools.package.add_gi_packages')

        sys_and_site_mocks['gi'].side_effect = ImportError()

        with pytest.warns(ImportWarning) as record:
            scarlett_os.tools.package.check_gi()

        assert len(record) == 1
        assert record[0].message.args[0] == "PyGI library is not available"

    def test_add_gi_packages(self, sys_and_site_mocks, package_unit_mocker_stopall):
        sys_and_site_mocks['os'] = package_unit_mocker_stopall.patch('scarlett_os.tools.package.get_os_module')
        sys_and_site_mocks['os'].environ = dict()

        sys_and_site_mocks['sys'] = package_unit_mocker_stopall.patch('scarlett_os.tools.package.get_sys_module')
        sys_and_site_mocks['sys'].version.return_value = '3.6.5 (default, Apr 25 2018, 14:22:56) \n[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.42.1)]'

        sys_and_site_mocks['get_python_lib'] = package_unit_mocker_stopall.patch('scarlett_os.tools.package.get_distutils_sysconfig_function_get_python_lib')
        sys_and_site_mocks['get_python_lib'].return_value = lambda: '/usr/local/lib/python3.6/site-packages'

        sys_and_site_mocks['flatpak_site_packages'] = package_unit_mocker_stopall.patch('scarlett_os.tools.package.get_flatpak_site_packages')

        sys_and_site_mocks['package_list_with_dups'] = package_unit_mocker_stopall.patch('scarlett_os.tools.package.create_list_with_dups')

        sys_and_site_mocks['uniq_package_list'] = package_unit_mocker_stopall.patch('scarlett_os.tools.package.get_uniq_list')

        sys_and_site_mocks['create_package_symlinks'] = package_unit_mocker_stopall.patch('scarlett_os.tools.package.create_package_symlinks')

        scarlett_os.tools.package.add_gi_packages()

        # Make sure sys.version[:3] returns 3.6 for this example
        assert sys_and_site_mocks['sys'].version.return_value[:3] == '3.6'
