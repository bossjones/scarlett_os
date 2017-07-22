#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_config
----------------------------------
"""

import imp
import os.path
import sys
import unittest
import unittest.mock as mock

import pytest

import tempfile
import shutil

import scarlett_os
from scarlett_os.common.configure import config


# source: https://github.com/YosaiProject/yosai/blob/master/test/isolated_tests/core/conf/conftest.py
@pytest.fixture(scope='function')
def config_unit_mocker_stopall(mocker):
    "Stop previous mocks, yield mocker plugin obj, then stopall mocks again"
    print('Called [setup]: mocker.stopall()')
    mocker.stopall()
    print('Called [setup]: imp.reload(player)')
    imp.reload(config)
    yield mocker
    print('Called [teardown]: mocker.stopall()')
    mocker.stopall()
    print('Called [setup]: imp.reload(player)')
    imp.reload(config)

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
    temp_config = config.Config.from_file(config_file)

    yield temp_config

    shutil.rmtree(base)


@pytest.fixture(scope='function')
def fake_config_no_values():
    """Create a temporary config file."""
    base = tempfile.mkdtemp()
    config_file = os.path.join(base, 'config.yaml')

    temp_config = config.Config.from_file(config_file)

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
    temp_config = config.Config.from_file(config_file)

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
@pytest.mark.configtest
@pytest.mark.scarlettonlyunittest
class TestFilterMatcher(object):
    # Borrowed from udiskie

    """
    Tests for the scarlett_os.common.configure.FilterMatcher class.
    """

    def test_config_from_file(self, fake_config):
        """Test Config object and properties."""
        assert fake_config.scarlett_name == 'ScarlettOS'
        assert fake_config.latitude == 40.7056308
        assert fake_config.longitude == -73.9780034
        assert fake_config.elevation == 665
        assert fake_config.unit_system == 'metric'
        assert fake_config.time_zone == 'America/New_York'
        assert fake_config.owner_name == 'Hair Ron Jones'
        assert fake_config.keyword_list == ['scarlett', 'SCARLETT']
        assert fake_config.features_enabled == ['time']
        # NOTE: If we want to use these values we need to run them through a filter so that they get casted to their proper types
        assert fake_config.pocketsphinx == {'hmm': '/home/pi/.virtualenvs/scarlett_os/share/pocketsphinx/model/en-us/en-us',
                                            'lm': '/home/pi/dev/bossjones-github/scarlett_os/static/speech/lm/1473.lm',
                                            'dict': '/home/pi/dev/bossjones-github/scarlett_os/static/speech/dict/1473.dic',
                                            'silprob': 0.1,
                                            'wip': '1e-4',
                                            'bestpath': 0
                                           }
        assert fake_config.coordinates == (40.7056308, -73.9780034)

    def test_config_file_not_found(self):
        """test usecase when file not found."""

        base = tempfile.mkdtemp()
        config_file = os.path.join(base, 'config.yaml')

        with pytest.raises(FileNotFoundError):
            temp_config = config.Config.from_file(config_file)

        shutil.rmtree(base)

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


        # In [6]: dump(temp_config)
        # obj.__class__ = <class 'scarlett_os.common.configure.config.Config'>
        # obj.__delattr__ = <method-wrapper '__delattr__' of Config object at 0x7f7a8c5336d8>
        # obj.__dict__ = {'_data': {}}
        # obj.__dir__ = <built-in method __dir__ of Config object at 0x7f7a8c5336d8>
        # obj.__doc__ = ScarlettOS config in memory representation.
        # obj.__eq__ = <method-wrapper '__eq__' of Config object at 0x7f7a8c5336d8>
        # obj.__format__ = <built-in method __format__ of Config object at 0x7f7a8c5336d8>
        # obj.__ge__ = <method-wrapper '__ge__' of Config object at 0x7f7a8c5336d8>
        # obj.__getattribute__ = <method-wrapper '__getattribute__' of Config object at 0x7f7a8c5336d8>
        # obj.__gt__ = <method-wrapper '__gt__' of Config object at 0x7f7a8c5336d8>
        # obj.__hash__ = <method-wrapper '__hash__' of Config object at 0x7f7a8c5336d8>
        # obj.__init__ = <bound method Config.__init__ of <scarlett_os.common.configure.config.Config object at 0x7f7a8c5336d8>>
        # obj.__le__ = <method-wrapper '__le__' of Config object at 0x7f7a8c5336d8>
        # obj.__lt__ = <method-wrapper '__lt__' of Config object at 0x7f7a8c5336d8>
        # obj.__module__ = scarlett_os.common.configure.config
        # obj.__ne__ = <method-wrapper '__ne__' of Config object at 0x7f7a8c5336d8>
        # obj.__new__ = <built-in method __new__ of type object at 0x7f7a97455ae0>
        # obj.__reduce__ = <built-in method __reduce__ of Config object at 0x7f7a8c5336d8>
        # obj.__reduce_ex__ = <built-in method __reduce_ex__ of Config object at 0x7f7a8c5336d8>
        # obj.__repr__ = <method-wrapper '__repr__' of Config object at 0x7f7a8c5336d8>
        # obj.__setattr__ = <method-wrapper '__setattr__' of Config object at 0x7f7a8c5336d8>
        # obj.__sizeof__ = <built-in method __sizeof__ of Config object at 0x7f7a8c5336d8>
        # obj.__str__ = <method-wrapper '__str__' of Config object at 0x7f7a8c5336d8>
        # obj.__subclasshook__ = <built-in method __subclasshook__ of type object at 0x3045ca8>
        # obj.__weakref__ = None
        # obj._data = {}
        # obj.coordinates = Coordinates(latitude=0, longitude=0)
        # obj.default_pathes = <bound method Config.default_pathes of <class 'scarlett_os.common.configure.config.Config'>>
        # obj.elevation = 0
        # obj.features_enabled = []
        # obj.from_file = <bound method Config.from_file of <class 'scarlett_os.common.configure.config.Config'>>
        # obj.keyword_list = []
        # obj.latitude = 0
        # obj.longitude = 0
        # obj.owner_name = commander keen
        # obj.pocketsphinx = {}
        # obj.scarlett_name = scarlett
        # obj.time_zone = UTC
        # obj.unit_system = imperial
