#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright bossjones
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import platform
import re
import warnings
import pprint
pp = pprint.PrettyPrinter(indent=4)


# Don't force people to install setuptools unless
# we have to.
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

from setuptools import setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
from setuptools.command import install_lib

from scarlett_os.const import __version__
from scarlett_os.const import PROJECT_PACKAGE_NAME
from scarlett_os.const import PROJECT_LICENSE
from scarlett_os.const import PROJECT_URL
from scarlett_os.const import PROJECT_EMAIL
from scarlett_os.const import PROJECT_DESCRIPTION
from scarlett_os.const import PROJECT_CLASSIFIERS
from scarlett_os.const import GITHUB_URL
from scarlett_os.const import PROJECT_AUTHOR


HERE = os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_URL = ('{}/archive/'
                '{}.zip'.format(GITHUB_URL, __version__))

# PACKAGES = find_packages(exclude=['tests', 'tests.*'])
PACKAGE_NAME = PROJECT_PACKAGE_NAME

print('Current Python Version, B: {}'.format(sys.version_info))

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

static = {}

for root, dirs, files in os.walk('static'):
    for filename in files:
        filepath = os.path.join(root, filename)

        if root not in static:
            static[root] = []

        static[root].append(filepath)

# Might use this later
try:
    here = os.path.abspath(os.path.dirname(__file__))
except:
    pass

# FIXME: This does not handle git+ssh packages
# source: https://github.com/dave-shawley/python-cookiecutter/blob/844e6bfcf8639eab4feef0c2a83ac61f3aea412c/%7B%7Bcookiecutter.package_name%7D%7D/setup.py
def read_requirements(name):
    requirements = []
    try:
        with open(name) as req_file:
            for line in req_file:
                # source: http://www.diveintopython.net/native_data_types/lists.html
                if '#' in line:
                    line = line[:line.index('#')]
                line = line.strip()
                if line.startswith('-r'):
                    requirements.extend(read_requirements(line[2:].strip()))
                elif not line.startswith('-'):
                    if line is '':
                      continue
                    requirements.append(line)
    except IOError:
        pass

    return requirements

requirements = read_requirements('requirements.txt')
requirements_dev = read_requirements('requirements_dev.txt')
requirements_test = read_requirements('requirements_test.txt')
requirements_test_experimental = read_requirements('requirements_test_experimental.txt')

# source: http://stackoverflow.com/questions/14399534/how-can-i-reference-requirements-txt-for-the-install-requires-kwarg-in-setuptool

# Pytest
class PyTest(TestCommand):

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests', '--ignore', 'tests/sandbox', '--verbose']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name=PROJECT_PACKAGE_NAME,
    version=__version__,
    description=PROJECT_DESCRIPTION,
    long_description=readme + '\n\n' + history,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    url=PROJECT_URL,
    download_url=DOWNLOAD_URL,
    packages=[
        'scarlett_os',
    ],
    package_dir={'scarlett_os':
                 'scarlett_os'},
    #              ,
    # entry_points={
    #     'console_scripts': [
    #         'ss = scarlett_os.__main__:main'
    #     ]
    # },
    # entry_points={
    #     'console_scripts': [
    #         'scarlett_os=scarlett_os.cli:main'
    #     ]
    # },
    # source: mapbox-cli-py
    entry_points="""
    [console_scripts]
    scarlett_os=scarlett_os.scripts.cli:main_group

    [scarlett_os.scarlett_os_commands]
    config=scarlett_os.scripts.config:config
    """,
    # geocoding=mapboxcli.scripts.geocoding:geocoding
    # directions=mapboxcli.scripts.directions:directions
    # distance=mapboxcli.scripts.distance:distance
    # mapmatching=mapboxcli.scripts.mapmatching:match
    # upload=mapboxcli.scripts.uploads:upload
    # staticmap=mapboxcli.scripts.static:staticmap
    # surface=mapboxcli.scripts.surface:surface
    # dataset=mapboxcli.scripts.datasets:datasets
    extras_require={
        'test': requirements_test,
        'experimental': requirements_test_experimental,
        'dev': requirements_dev,
    },
    include_package_data=True,
    install_requires=requirements,
    license=PROJECT_LICENSE,
    zip_safe=False,
    keywords='scarlett_os',
    classifiers=PROJECT_CLASSIFIERS,
    test_suite='tests',
    tests_require=requirements_test,
    # dependency_links = ['https://github.com/mverteuil/pytest-ipdb/tarball/master#egg=pytest-ipdb-0.1.dev2'],
    cmdclass={'test': PyTest}
)
