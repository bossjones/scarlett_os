#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from setuptools.command.test import test as TestCommand
from setuptools.command import install_lib

PACKAGE_NAME = 'scarlett_os'
MINIMUM_PYTHON_VERSION = 3, 4


def check_python_version():
    """Exit when the Python version is too low."""
    if sys.version_info < MINIMUM_PYTHON_VERSION:
        sys.exit("Python {}.{}+ is required.".format(*MINIMUM_PYTHON_VERSION))

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


def read_requirements(filename):
    content = open(os.path.join(here, filename)).read()
    requirements = map(lambda r: r.strip(), content.splitlines())
    return requirements


requirements = [
    'Click>=6.0',
    'click-plugins',
    'pydbus>=0.5.0',
    'colorlog>=2.7',
    'psutil>=4.3.0',
    'six',
    'Fabric3==1.12.post1',
    'PyYAML>=3.0'
]


test_requirements = [
    'pytest>=3.0',
    'pip>=7.0',
    'bumpversion>=0.5.3',
    'wheel>=0.29.0',
    'watchdog>=0.8.3',
    'flake8>=2.6.2',
    'flake8-docstrings>=0.2.8',
    'coverage>=4.1',
    'Sphinx>=1.4.5',
    'cryptography==1.5.2',
    'PyYAML>=3.11',
    'pydocstyle>=1.0.0',
    'mypy-lang>=0.4',
    'pylint>=1.5.6',
    'coveralls>=1.1',
    'ipython>=5.1.0',
    'gnureadline>=6.3.0'

]


# Pytest
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests', '--ignore', 'tests/sandbox', '--verbose']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


check_python_version()


setup(
    name='scarlett_os',
    version='0.1.0',
    description="S.C.A.R.L.E.T.T is Tony Darks artificially programmed intelligent computer. She is programmed to speak with a female voice in a British accent.",
    long_description=readme + '\n\n' + history,
    author="Malcolm Jones",
    author_email='bossjones@theblacktonystark.com',
    url='https://github.com/bossjones/scarlett_os',
    packages=[
        'scarlett_os',
    ],
    package_dir={'scarlett_os':
                 'scarlett_os'},
    #              ,
    # entry_points={
    #     'console_scripts': [
    #         'hass = homeassistant.__main__:main'
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
        'test': ['coveralls', 'pytest>=3.0', 'pytest-cov'],
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='scarlett_os',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass={'test': PyTest}
)
