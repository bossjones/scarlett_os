#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_simple_config
----------------------------------
"""

import builtins
import imp
import os.path
import sys
import unittest
import unittest.mock as mock

import pytest

import tempfile
import shutil

import scarlett_os
from scarlett_os.common.configure import simple_config


# source: https://github.com/YosaiProject/yosai/blob/master/test/isolated_tests/core/conf/conftest.py
@pytest.fixture(scope='function')
def simple_config_unit_mocker_stopall(mocker):
    "Stop previous mocks, yield mocker plugin obj, then stopall mocks again"
    print('Called [setup]: mocker.stopall()')
    mocker.stopall()
    print('Called [setup]: imp.reload(simple_config)')
    imp.reload(simple_config)
    yield mocker
    print('Called [teardown]: mocker.stopall()')
    mocker.stopall()
    print('Called [setup]: imp.reload(simple_config)')
    imp.reload(simple_config)

@pytest.fixture(scope='function')
def fake_config():
    """Create a temporary config file."""
    base = tempfile.mkdtemp()
    config_file = os.path.join(base, 'config.yaml')

    with open(config_file, 'wt') as f:
        f.write('''
# Omitted values in this section will be auto detected using freegeoip.io

# Location required to calculate the time the sun rises and sets.
# Coordinates are also used for location for weather related automations.
# Google Maps can be used to determine more precise GPS coordinates.
latitude: 40.7056308
longitude: -73.9780034

pocketsphinx:
    hmm: /home/pi/.virtualenvs/scarlett_os/share/pocketsphinx/model/en-us/en-us
    lm: /home/pi/dev/bossjones-github/scarlett_os/static/speech/lm/1473.lm
    dict: /home/pi/dev/bossjones-github/scarlett_os/static/speech/dict/1473.dic
    silprob: 0.1
    wip: 1e-4
    bestpath: 0

# Impacts weather/sunrise data
elevation: 665

# 'metric' for Metric System, 'imperial' for imperial system
unit_system: metric

# Pick yours from here:
# http://en.wikipedia.org/wiki/List_of_tz_database_time_zones
time_zone: America/New_York

# Name of the location where ScarlettOS Assistant is running
name: ScarlettOS

owner: "Hair Ron Jones"

keywords_list:
- 'scarlett'
- 'SCARLETT'

features:
- time
''')
    temp_config = simple_config.SimpleConfig.from_file(config_file)

    yield temp_config

    shutil.rmtree(base)


@pytest.fixture(scope='function')
def fake_config_no_values():
    """Create a temporary config file."""
    base = tempfile.mkdtemp()
    config_file = os.path.join(base, 'config.yaml')

    temp_config = simple_config.SimpleConfig.from_file(config_file)

    yield temp_config

    shutil.rmtree(base)

@pytest.fixture(scope='function')
def fake_config_empty():
    """Create a temporary config file."""
    base = tempfile.mkdtemp()
    config_file = os.path.join(base, 'config.yaml')

    with open(config_file, 'wt') as f:
        f.write('''
---
''')
    temp_config = simple_config.SimpleConfig.from_file(config_file)

    yield temp_config

    shutil.rmtree(base)

# pylint: disable=R0201
# pylint: disable=C0111
# pylint: disable=C0123
# pylint: disable=C0103
# pylint: disable=W0212
# pylint: disable=W0621
# pylint: disable=W0612
@pytest.mark.scarlettonly
@pytest.mark.unittest
@pytest.mark.simpleconfigtest
@pytest.mark.scarlettonlyunittest
class TestSimpleConfigLower(object):
    # Borrowed from udiskie

    """
    Tests for the scarlett_os.common.configure.FilterMatcher class.
    """

    def test_lower(self, simple_config_unit_mocker_stopall):
        temp_mocker = simple_config_unit_mocker_stopall

        mock_a_string = temp_mocker.MagicMock(name='mock_a_string')
        mock_a_string.return_value = 'HELLO'

        assert simple_config.lower(mock_a_string.return_value) == 'hello'

    def test_to_lowercase_empty_string(self):
        assert simple_config.lower("") == ""

    def test_lower_AttributeError(self):
        assert simple_config.lower([1,2,3]) == [1,2,3]


# pylint: disable=R0201
# pylint: disable=C0111
# pylint: disable=C0123
# pylint: disable=C0103
# pylint: disable=W0212
# pylint: disable=W0621
# pylint: disable=W0612
@pytest.mark.scarlettonly
@pytest.mark.unittest
@pytest.mark.simpleconfigtest
@pytest.mark.scarlettonlyunittest
class TestGetXdgConfigDirPath(object):

    """
    Validate get_xdg_config_dir_path
    """

    # def test_yaml_unicode_representer(self, simple_config_unit_mocker_stopall):
    #     # '<b class="boldest">Б - Бага</b>'
    #     pass

    def test_get_xdg_config_dir_path(self, simple_config_unit_mocker_stopall):
        assert simple_config.get_xdg_config_dir_path() == '/home/pi/.config'

    def test_get_xdg_data_dir_path(self, simple_config_unit_mocker_stopall):
        assert simple_config.get_xdg_data_dir_path() == '/home/pi/.local/share'

    def test_get_xdg_cache_dir_path(self, simple_config_unit_mocker_stopall):
        assert simple_config.get_xdg_cache_dir_path() == '/home/pi/.cache'

    def test_get_config_sub_dir_path(self, simple_config_unit_mocker_stopall):
        assert simple_config.get_config_sub_dir_path() == '/home/pi/.config/scarlett'

    def test_get_config_file_path(self, simple_config_unit_mocker_stopall):
        assert simple_config.get_config_file_path() == '/home/pi/.config/scarlett/config.yaml'

# pylint: disable=R0201
# pylint: disable=C0111
# pylint: disable=C0123
# pylint: disable=C0103
# pylint: disable=W0212
# pylint: disable=W0621
# pylint: disable=W0612
@pytest.mark.scarlettonly
@pytest.mark.unittest
@pytest.mark.simpleconfigtest
@pytest.mark.scarlettonlyunittest
class TestSimpleFilterMatcher(object):
    # Borrowed from udiskie

    """
    Tests for the scarlett_os.common.configure.FilterMatcher class.
    """

    # def test_config_from_file(self, fake_config):
    #     """Test Config object and properties."""
    #     assert fake_config.scarlett_name == 'ScarlettOS'
    #     assert fake_config.latitude == 40.7056308
    #     assert fake_config.longitude == -73.9780034
    #     assert fake_config.elevation == 665
    #     assert fake_config.unit_system == 'metric'
    #     assert fake_config.time_zone == 'America/New_York'
    #     assert fake_config.owner_name == 'Hair Ron Jones'
    #     assert fake_config.keyword_list == ['scarlett', 'SCARLETT']
    #     assert fake_config.features_enabled == ['time']
    #     # NOTE: If we want to use these values we need to run them through a filter so that they get casted to their proper types
    #     assert fake_config.pocketsphinx == {'hmm': '/home/pi/.virtualenvs/scarlett_os/share/pocketsphinx/model/en-us/en-us',
    #                                         'lm': '/home/pi/dev/bossjones-github/scarlett_os/static/speech/lm/1473.lm',
    #                                         'dict': '/home/pi/dev/bossjones-github/scarlett_os/static/speech/dict/1473.dic',
    #                                         'silprob': 0.1,
    #                                         'wip': '1e-4',
    #                                         'bestpath': 0
    #                                        }
    #     assert fake_config.coordinates == (40.7056308, -73.9780034)

    # def test_config_file_not_found(self):
    #     """test usecase when file not found."""

    #     base = tempfile.mkdtemp()
    #     config_file = os.path.join(base, 'config.yaml')

    #     with pytest.raises(FileNotFoundError):
    #         temp_config = simple_config.SimpleConfig.from_file(config_file)

    #     shutil.rmtree(base)

    # def test_config_from_file_no_values_set(self, fake_config_empty):
    #     """Test Config object and properties."""
    #     # assert fake_config_no_values.scarlett_name == 'scarlett'
    #     # assert fake_config_no_values.latitude == 0
    #     assert fake_config_no_values.longitude == 0
    #     assert fake_config_no_values.elevation == 0
    #     assert fake_config_no_values.unit_system == 'imperial'
    #     assert fake_config_no_values.time_zone == 'UTC'
    #     assert fake_config_no_values.owner_name == 'commander keen'
    #     assert fake_config_no_values.keyword_list == []
    #     assert fake_config_no_values.features_enabled == []
    #     assert fake_config_no_values.pocketsphinx == {}
    #     assert fake_config_no_values.coordinates == (0, 0)
