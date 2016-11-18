# from __future__ import absolute_import, unicode_literals

import platform
import sys
import unittest

# import mock
import unittest.mock as mock

import pkg_resources

from scarlett_os.internal import deps
from scarlett_os.internal.gi import Gst, gi

from scarlett_os.const import (
    PROJECT_NAME, PROJECT_PACKAGE_NAME)

import pprint
pp = pprint.PrettyPrinter(indent=4)


class DepsTest(unittest.TestCase):

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

        self.assertIn('Python: FooPython 3.5.2', result)

        self.assertIn('Platform: Loonix 4.0.1', result)

        self.assertIn('Pykka: 1.1 from /foo/bar', result)
        self.assertNotIn('/baz.py', result)
        self.assertIn('Detailed information: Quux', result)

        self.assertIn('Foo: not found', result)

        self.assertIn('ScarlettOS: 0.5.1', result)
        self.assertIn('  pylast: 0.5', result)
        self.assertIn('    setuptools: 0.6', result)

    def test_executable_info(self):
        result = deps.executable_info()

        self.assertEqual('Executable', result['name'])
        self.assertIn(sys.argv[0], result['version'])

    def test_platform_info(self):
        result = deps.platform_info()

        self.assertEqual('Platform', result['name'])
        self.assertIn(platform.platform(), result['version'])

    def test_python_info(self):
        result = deps.python_info()

        self.assertEqual('Python', result['name'])
        self.assertIn(platform.python_implementation(), result['version'])
        self.assertIn(platform.python_version(), result['version'])
        self.assertIn('python', result['path'])
        self.assertNotIn('platform.py', result['path'])

    def test_gstreamer_info(self):
        result = deps.gstreamer_info()

        self.assertEqual('GStreamer', result['name'])
        self.assertEqual(
            '.'.join(map(str, Gst.version())), result['version'])
        self.assertIn('gi', result['path'])
        self.assertNotIn('__init__.py', result['path'])
        self.assertIn('Python wrapper: python-gi', result['other'])
        self.assertIn(gi.__version__, result['other'])
        self.assertIn('Relevant elements:', result['other'])

    @mock.patch('pkg_resources.get_distribution')
    def test_pkg_info(self, get_distribution_mock):
        # NOTE: To find out requirements, run this pkg_resources.get_distribution("pydbus").requires()
        dist_scarlett_os = mock.Mock()
        dist_scarlett_os.project_name = PROJECT_PACKAGE_NAME
        dist_scarlett_os.version = '0.5.1'
        dist_scarlett_os.location = '/tmp/example/scarlett_os'
        dist_scarlett_os.requires.return_value = [
            'pydbus>=0.5.0'
        ]

        dist_pydbus = mock.Mock()
        dist_pydbus.project_name = 'pydbus'
        dist_pydbus.version = '0.5.1'
        dist_pydbus.location = '/tmp/example/pydbus'
        dist_pydbus.requires.return_value = ['setuptools']

        dist_colorlog = mock.Mock()
        dist_colorlog.project_name = 'colorlog'
        dist_colorlog.version = '2.7.0'
        dist_colorlog.location = '/tmp/example/colorlog'
        dist_colorlog.requires.return_value = []

        dist_click = mock.Mock()
        dist_click.project_name = 'click'
        dist_click.version = '6.6'
        dist_click.location = '/tmp/example/click'
        dist_click.requires.return_value = []

        #  pkg_resources.get_distribution("setuptools").__dict__
        dist_setuptools = mock.Mock()
        dist_setuptools.project_name = 'setuptools'
        dist_setuptools.version = '0.6'
        dist_setuptools.location = '/tmp/example/setuptools'
        dist_setuptools.requires.return_value = []

        # side_effect allows you to perform side effects, including raising an exception when a mock is called
        get_distribution_mock.side_effect = [
            dist_scarlett_os, dist_pydbus, dist_setuptools]

        result = deps.pkg_info()
        print('****** deps.pkg_info() ****')
        # {'dependencies': [], 'path': '/tmp/example/pydbus', 'name': 'ScarlettOS', 'version': '0.5.1'}
        pp.pprint(result)

        self.assertEqual(PROJECT_NAME, result['name'])
        self.assertEqual('0.5.1', result['version'])
        self.assertIn('scarlett_os', result['path'])

        dep_info_pydbus = result['dependencies'][0]
        self.assertEqual('pydbus>=0.5.0', dep_info_pydbus['name'])
        self.assertEqual('0.5.1', dep_info_pydbus['version'])

        dep_info_setuptools = dep_info_pydbus['dependencies'][0]
        self.assertEqual('setuptools', dep_info_setuptools['name'])
        self.assertEqual('0.6', dep_info_setuptools['version'])

    @mock.patch('pkg_resources.get_distribution')
    def test_pkg_info_for_missing_dist(self, get_distribution_mock):
        get_distribution_mock.side_effect = pkg_resources.DistributionNotFound

        result = deps.pkg_info()

        self.assertEqual(PROJECT_NAME, result['name'])  # ScarlettOS
        self.assertNotIn('version', result)
        self.assertNotIn('path', result)

    @mock.patch('pkg_resources.get_distribution')
    def test_pkg_info_for_wrong_dist_version(self, get_distribution_mock):
        get_distribution_mock.side_effect = pkg_resources.VersionConflict

        result = deps.pkg_info()

        self.assertEqual(PROJECT_NAME, result['name'])
        self.assertNotIn('version', result)
        self.assertNotIn('path', result)
