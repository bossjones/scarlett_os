#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ruamel_config
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
from scarlett_os.common.configure import ruamel_config

from tests.conftest import dict_compare


# source:
# https://github.com/YosaiProject/yosai/blob/master/test/isolated_tests/core/conf/conftest.py
@pytest.fixture(scope='function')
def ruamel_config_unit_mocker_stopall(mocker):
    "Stop previous mocks, yield mocker plugin obj, then stopall mocks again"
    print('Called [setup]: mocker.stopall()')
    mocker.stopall()
    print('Called [setup]: imp.reload(ruamel_config)')
    imp.reload(ruamel_config)
    yield mocker
    print('Called [teardown]: mocker.stopall()')
    mocker.stopall()
    print('Called [setup]: imp.reload(ruamel_config)')
    imp.reload(ruamel_config)


@pytest.fixture(scope='function')
def fake_config():
    """Create a temporary config file."""
    base = tempfile.mkdtemp()
    config_file = os.path.join(base, 'config.yaml')

    with open(config_file, 'wt') as f:
        f.write(ruamel_config.DEFAULT_CONFIG)

    temp_config = ruamel_config.load_config(config_file)

    yield temp_config

    shutil.rmtree(base)


@pytest.fixture(scope='function')
def fake_config_no_values():
    """Create a temporary config file."""
    base = tempfile.mkdtemp()
    config_file = os.path.join(base, 'config.yaml')

    temp_config = ruamel_config.load_config(config_file)

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
    temp_config = ruamel_config.load_config(config_file)

    yield temp_config

    shutil.rmtree(base)


@pytest.fixture(scope='function')
def fake_config_russian_encoding():
    """Create a temporary config file."""
    base = tempfile.mkdtemp()
    config_file = os.path.join(base, 'config.yaml')

    with open(config_file, 'wt') as f:
        f.write('''
---
# Name of the location where ScarlettOS Assistant is running
name: Бага

owner: "Б - Бага"
''')
    temp_russian_config = ruamel_config.load_config(config_file)

    yield temp_russian_config

    shutil.rmtree(base)

# pylint: disable=R0201
# pylint: disable=C0111
# pylint: disable=C0123
# pylint: disable=C0103
# pylint: disable=W0212
# pylint: disable=W0621
# pylint: disable=W0612


@pytest.mark.ruamelconfigonly
@pytest.mark.scarlettonly
@pytest.mark.unittest
@pytest.mark.simpleconfigtest
@pytest.mark.scarlettonlyunittest
class TestSimpleConfigLower(object):
    # Borrowed from udiskie

    """
    Tests for the scarlett_os.common.configure.FilterMatcher class.
    """

    def test_lower(self, ruamel_config_unit_mocker_stopall):
        temp_mocker = ruamel_config_unit_mocker_stopall

        mock_a_string = temp_mocker.MagicMock(name='mock_a_string')
        mock_a_string.return_value = 'HELLO'

        assert ruamel_config.lower(mock_a_string.return_value) == 'hello'

    def test_to_lowercase_empty_string(self):
        assert ruamel_config.lower("") == ""

    def test_lower_AttributeError(self):
        assert ruamel_config.lower([1, 2, 3]) == [1, 2, 3]

# pylint: disable=R0201
# pylint: disable=C0111
# pylint: disable=C0123
# pylint: disable=C0103
# pylint: disable=W0212
# pylint: disable=W0621
# pylint: disable=W0612


@pytest.mark.ruamelconfigonly
@pytest.mark.scarlettonly
@pytest.mark.unittest
@pytest.mark.simpleconfigtest
@pytest.mark.scarlettonlyunittest
class TestGetXdgConfigDirPath(object):

    """
    Validate get_xdg_config_dir_path
    """

    def test_yaml_unicode_representer(self, ruamel_config_unit_mocker_stopall, fake_config_russian_encoding):
        # yield fixture to var
        temp_russian_config = fake_config_russian_encoding
        # perform a yaml dump and store in variable
        output = ruamel_config.dump_in_memory_config_to_var(temp_russian_config, stream=False)
        # determine if we got the exact output we expected
        assert output == '%YAML 1.2\n---\n# Name of the location where ScarlettOS Assistant is running\nname: Бага\n\nowner: Б - Бага\n'

    def test_get_xdg_config_dir_path(self, ruamel_config_unit_mocker_stopall):
        assert ruamel_config.get_xdg_config_dir_path() == '/home/pi/.config'

    def test_get_xdg_data_dir_path(self, ruamel_config_unit_mocker_stopall):
        assert ruamel_config.get_xdg_data_dir_path() == '/home/pi/.local/share'

    def test_get_xdg_cache_dir_path(self, ruamel_config_unit_mocker_stopall):
        assert ruamel_config.get_xdg_cache_dir_path() == '/home/pi/.cache'

    def test_get_config_sub_dir_path(self, ruamel_config_unit_mocker_stopall):
        assert ruamel_config.get_config_sub_dir_path() == '/home/pi/.config/scarlett'

    def test_get_config_file_path(self, ruamel_config_unit_mocker_stopall):
        assert ruamel_config.get_config_file_path(
        ) == '/home/pi/.config/scarlett/config.yaml'

    def test_get_version_file_path(self, ruamel_config_unit_mocker_stopall):
        assert ruamel_config.get_version_file_path() == '/home/pi/.config/scarlett/.SCARLETT_VERSION'

# pylint: disable=R0201
# pylint: disable=C0111
# pylint: disable=C0123
# pylint: disable=C0103
# pylint: disable=W0212
# pylint: disable=W0621
# pylint: disable=W0612


@pytest.mark.ruamelconfigonly
@pytest.mark.scarlettonly
@pytest.mark.unittest
@pytest.mark.simpleconfigtest
@pytest.mark.scarlettonlyunittest
class TestFlatten(object):

    """
    Test Flatten Function
    """

    def test_flatten(self, ruamel_config_unit_mocker_stopall):
        to_flatten = {'a': 1,
                      'c': {'a': 2,
                            'b': {'x': 5,
                                  'y': 10}},
                      'd': [1, 2, 3]}

        expected_flattened = {'a': 1, 'c_a': 2,
                              'c_b_x': 5, 'd': [1, 2, 3], 'c_b_y': 10}

        flattened_result = ruamel_config.flatten(to_flatten)
        added, removed, modified, same = dict_compare(
            flattened_result, expected_flattened)

        # assert dicts are exactly the same, meaning modified is equal to empty
        # dict {}
        assert modified == {}


# pylint: disable=R0201
# pylint: disable=C0111
# pylint: disable=C0123
# pylint: disable=C0103
# pylint: disable=W0212
# pylint: disable=W0621
# pylint: disable=W0612
@pytest.mark.ruamelconfigonly
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
    #         temp_config = ruamel_config.SimpleConfig.from_file(config_file)

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
