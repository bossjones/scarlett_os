# from __future__ import absolute_import, unicode_literals

import imp
import platform
import pprint
import sys
import unittest
import unittest.mock as mock

import pkg_resources
import pytest

import scarlett_os
from scarlett_os.const import PROJECT_NAME, PROJECT_PACKAGE_NAME
from scarlett_os.internal import deps
from scarlett_os.internal.gi import Gst, gi

pp = pprint.PrettyPrinter(indent=4)


@pytest.fixture(scope='function')
def deps_mocker_stopall(mocker):
    "Stop previous mocks, yield mocker plugin obj, then stopall mocks again"
    print('Called [setup]: mocker.stopall()')
    mocker.stopall()
    print('Called [setup]: imp.reload(deps)')
    imp.reload(deps)
    yield mocker
    print('Called [teardown]: mocker.stopall()')
    mocker.stopall()
    print('Called [setup]: imp.reload(deps)')
    imp.reload(deps)


class TestDeps(object):

    def test_format_dependency_list(self):
        adapters = [
            lambda: dict(name='Python', version='FooPython 3.5.2'),
            lambda: dict(name='Platform', version='Loonix 4.0.1'),
            lambda: dict(
                name='Pykka', version='1.1',
                path='/foo/bar', other='Quux'),
            lambda: dict(name='Foo'),
            lambda: dict(name='ScarlettOS', version='0.5.1', dependencies=[
                dict(name='pylast', version='0.5', dependencies=[
                    dict(name='setuptools', version='0.6')
                ])
            ])
        ]

        result = deps.format_dependency_list(adapters)

        assert 'Python: FooPython 3.5.2' in result

        assert 'Platform: Loonix 4.0.1' in result

        assert 'Pykka: 1.1 from /foo/bar' in result
        assert '/baz.py' not in result
        assert 'Detailed information: Quux' in result

        assert 'Foo: not found' in result

        assert 'ScarlettOS: 0.5.1' in result
        assert '  pylast: 0.5' in result
        assert '    setuptools: 0.6' in result

    def test_executable_info(self):
        result = deps.executable_info()

        assert 'Executable' == result['name']
        assert sys.argv[0] in result['version']

    def test_platform_info(self):
        result = deps.platform_info()

        assert 'Platform' == result['name']
        assert platform.platform() in result['version']

    def test_python_info(self):
        result = deps.python_info()

        assert 'Python' == result['name']
        assert platform.python_implementation() in result['version']
        assert platform.python_version() in result['version']
        assert 'python' in result['path']
        assert 'platform.py' not in result['path']

    def test_gstreamer_info(self):
        result = deps.gstreamer_info()

        assert 'GStreamer' == result['name']
        assert '.'.join(map(str, Gst.version())) == result['version']
        assert 'gi' in result['path']
        assert '__init__.py' not in result['path']
        assert 'Python wrapper: python-gi' in result['other']
        assert gi.__version__ in result['other']
        assert 'Relevant elements:' in result['other']

    def test_pkg_info(self, deps_mocker_stopall):
        # mock
        mock_get_distribution = deps_mocker_stopall.MagicMock(name="mock_get_distribution")
        # patch
        deps_mocker_stopall.patch.object(pkg_resources, 'get_distribution', mock_get_distribution)

        # NOTE: To find out requirements, run this pkg_resources.get_distribution("pydbus").requires()
        dist_scarlett_os = deps_mocker_stopall.Mock()
        dist_scarlett_os.project_name = PROJECT_PACKAGE_NAME
        dist_scarlett_os.version = '0.5.1'
        dist_scarlett_os.location = '/tmp/example/scarlett_os'
        dist_scarlett_os.requires.return_value = [
            'pydbus>=0.5.0'
        ]

        dist_pydbus = deps_mocker_stopall.Mock()
        dist_pydbus.project_name = 'pydbus'
        dist_pydbus.version = '0.5.1'
        dist_pydbus.location = '/tmp/example/pydbus'
        dist_pydbus.requires.return_value = ['setuptools']

        dist_colorlog = deps_mocker_stopall.Mock()
        dist_colorlog.project_name = 'colorlog'
        dist_colorlog.version = '2.7.0'
        dist_colorlog.location = '/tmp/example/colorlog'
        dist_colorlog.requires.return_value = []

        dist_click = deps_mocker_stopall.Mock()
        dist_click.project_name = 'click'
        dist_click.version = '6.6'
        dist_click.location = '/tmp/example/click'
        dist_click.requires.return_value = []

        #  pkg_resources.get_distribution("setuptools").__dict__
        dist_setuptools = deps_mocker_stopall.Mock()
        dist_setuptools.project_name = 'setuptools'
        dist_setuptools.version = '0.6'
        dist_setuptools.location = '/tmp/example/setuptools'
        dist_setuptools.requires.return_value = []

        # side_effect allows you to perform side effects, including raising an exception when a mock is called
        mock_get_distribution.side_effect = [
            dist_scarlett_os, dist_pydbus, dist_setuptools]

        result = deps.pkg_info()
        print('****** deps.pkg_info() ****')
        # {'dependencies': [], 'path': '/tmp/example/pydbus', 'name': 'ScarlettOS', 'version': '0.5.1'}
        pp.pprint(result)

        assert PROJECT_NAME == result['name']
        assert '0.5.1' == result['version']
        assert 'scarlett_os' in result['path']

        dep_info_pydbus = result['dependencies'][0]
        assert 'pydbus>=0.5.0' == dep_info_pydbus['name']
        assert '0.5.1' == dep_info_pydbus['version']

        dep_info_setuptools = dep_info_pydbus['dependencies'][0]
        assert 'setuptools' == dep_info_setuptools['name']
        assert '0.6' == dep_info_setuptools['version']

    def test_pkg_info_for_missing_dist(self, deps_mocker_stopall):
        # mock
        mock_get_distribution = deps_mocker_stopall.MagicMock(name="mock_get_distribution")
        # patch
        deps_mocker_stopall.patch.object(pkg_resources, 'get_distribution', mock_get_distribution)
        mock_get_distribution.side_effect = pkg_resources.DistributionNotFound

        result = deps.pkg_info()

        assert PROJECT_NAME == result['name']  # ScarlettOS
        assert 'version' not in result
        assert 'path' not in result

    def test_pkg_info_for_wrong_dist_version(self, deps_mocker_stopall):
        # mock
        mock_get_distribution = deps_mocker_stopall.MagicMock(name="mock_get_distribution")
        # patch
        deps_mocker_stopall.patch.object(pkg_resources, 'get_distribution', mock_get_distribution)
        mock_get_distribution.side_effect = pkg_resources.VersionConflict

        result = deps.pkg_info()

        assert PROJECT_NAME == result['name']
        assert 'version' not in result
        assert 'path' not in result
