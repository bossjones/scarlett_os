#!/usr/bin/env python3  # NOQA
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

# source: https://docs.python.org/3/library/codecs.html
import codecs
import collections
import fnmatch
import logging
import os
import shutil
import sys
import tempfile
from collections import OrderedDict
from gettext import gettext as _
from time import time
from typing import Any, Dict, Optional

import ruamel.yaml
import voluptuous as vol
from layeredconfig import Defaults, DictSource, LayeredConfig
from ruamel.yaml import YAML  # defaults to round-trip
from voluptuous.humanize import humanize_error

import scarlett_os.helpers.config_validation as cv
from scarlett_os.compat import (basestring, bytes, integer_types, string_types,
                                text_type)
from scarlett_os.const import (CONF_CUSTOMIZE, CONF_CUSTOMIZE_DOMAIN,
                               CONF_CUSTOMIZE_GLOB, CONF_ELEVATION,
                               CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME,
                               CONF_OWNERS_NAME, CONF_PACKAGES,
                               CONF_TEMPERATURE_UNIT, CONF_TIME_ZONE,
                               CONF_UNIT_SYSTEM, CONF_UNIT_SYSTEM_IMPERIAL,
                               CONF_UNIT_SYSTEM_METRIC, TEMP_CELSIUS,
                               __version__)
from scarlett_os.internal import path as path_internal
from scarlett_os.internal.path import mkdir_if_does_not_exist
from scarlett_os.utility import dt as date_util
from scarlett_os.utility import location as loc_util

logger = logging.getLogger(__name__)

# NOTE: (bytes, int, str, str)
SCALARS = (bytes,) + integer_types + string_types + (text_type,)

yaml = YAML()
yaml.explicit_start = True
yaml.indent = 4
yaml.block_seq_indent = 2
yaml.version = (1, 2)

# source: ruamel.yaml test_collections.py
# class TestOrderedDict:
#     def test_ordereddict(self):
#         assert ruamel.yaml.dump(OrderedDict()) == '!!omap []\n'


# NOTE: We are using https://github.com/srstevenson/xdg
# NOTE: This enforces the [XDG Base Directory Specification] https://specifications.freedesktop.org/basedir-spec/basedir-spec-0.6.html

# NOTEL Shamelesssly borrowed from udiskie
# source: https://github.com/coldfix/udiskie/blob/master/udiskie/config.py

YAML_CONFIG_FILE = 'config.yaml'
CONFIG_DIR_NAME = 'scarlett'
VERSION_FILE = '.SCARLETT_VERSION'

CoordinatesTuple = collections.namedtuple('Coordinates', ['latitude', 'longitude'])

DEFAULT_CORE_CONFIG = (
    # Tuples (attribute, default, auto detect property, description)
    (CONF_NAME, 'Scarlett Home', None, 'Name of the location where Home Assistant is '
     'running'),
    (CONF_LATITUDE, 0, 'latitude', 'Location required to calculate the time'
     ' the sun rises and sets'),
    (CONF_LONGITUDE, 0, 'longitude', None),
    (CONF_ELEVATION, 0, None, 'Impacts weather/sunrise data'
                              ' (altitude above sea level in meters)'),
    (CONF_UNIT_SYSTEM, CONF_UNIT_SYSTEM_METRIC, None,
     '{} for Metric, {} for Imperial'.format(CONF_UNIT_SYSTEM_METRIC,
                                             CONF_UNIT_SYSTEM_IMPERIAL)),
    (CONF_TIME_ZONE, 'UTC', 'time_zone', 'Pick yours from here: http://en.wiki'
     'pedia.org/wiki/List_of_tz_database_time_zones'),
)  # type: Tuple[Tuple[str, Any, Any, str], ...]

# NOTE: This is how you get a functions name automatically
# source: https://stackoverflow.com/questions/251464/how-to-get-a-function-name-as-a-string-in-python
# sys._getframe().f_code.co_name

DEFAULT_CONFIG = """
# Omitted values in this section will be auto detected using freegeoip.io

# Name for Scarlett to call user
owners_name: 'Hair Ron Jones'

pocketsphinx:
    hmm: /home/pi/.virtualenvs/scarlett_os/share/pocketsphinx/model/en-us/en-us
    lm: /home/pi/dev/bossjones-github/scarlett_os/static/speech/lm/1473.lm
    dict: /home/pi/dev/bossjones-github/scarlett_os/static/speech/dict/1473.dic
    silprob: 0.1
    wip: 1e-4
    bestpath: 0

keywords_list:
- 'scarlett'
- 'SCARLETT'

features:
- time
- help
- party
"""


# Data validation using voluptious
PACKAGES_CONFIG_SCHEMA = vol.Schema({
    cv.slug: vol.Schema(  # Package names are slugs
        {cv.slug: vol.Any(dict, list)})  # Only slugs for component names
})

CUSTOMIZE_CONFIG_SCHEMA = vol.Schema({
    vol.Optional(CONF_CUSTOMIZE, default={}):
        vol.Schema({cv.entity_id: dict}),
    vol.Optional(CONF_CUSTOMIZE_DOMAIN, default={}):
        vol.Schema({cv.string: dict}),
    vol.Optional(CONF_CUSTOMIZE_GLOB, default={}):
        vol.Schema({cv.string: OrderedDict}),
})

CORE_CONFIG_SCHEMA = CUSTOMIZE_CONFIG_SCHEMA.extend({
    CONF_NAME: vol.Coerce(str),
    CONF_LATITUDE: cv.latitude,
    CONF_LONGITUDE: cv.longitude,
    CONF_ELEVATION: vol.Coerce(int),
    vol.Optional(CONF_TEMPERATURE_UNIT): cv.temperature_unit,
    CONF_UNIT_SYSTEM: cv.unit_system,
    CONF_TIME_ZONE: cv.time_zone,
    vol.Optional(CONF_PACKAGES, default={}): PACKAGES_CONFIG_SCHEMA,
})


def lower(a_string):
    """
    Make string lowercase.

    :rtype: str
    """
    try:
        return a_string.lower()
    except AttributeError:
        return a_string


def mapping_string_access(self, s, delimiter=None, key_delim=None):
    # source: https://stackoverflow.com/questions/39463936/python-accessing-yaml-values-using-dot-notation
    def p(v):
        try:
            v = int(v)
        except:
            pass
        return v
       # possible extend for primitives like float, datetime, booleans, etc.

    if delimiter is None:
        delimiter = '.'
    if key_delim is None:
        key_delim = ','
    try:
        key, rest = s.split(delimiter, 1)
    except ValueError:
        key, rest = s, None
    if key_delim in key:
        key = tuple((p(key) for key in key.split(key_delim)))
    else:
        key = p(key)
    if rest is None:
        return self[key]
    return self[key].string_access(rest, delimiter, key_delim)

# monkeypatch CommentedMap.string_access function
ruamel.yaml.comments.CommentedMap.string_access = mapping_string_access


def sequence_string_access(self, s, delimiter=None, key_delim=None):
    # source: https://stackoverflow.com/questions/39463936/python-accessing-yaml-values-using-dot-notation
    if delimiter is None:
        delimiter = '.'
    try:
        key, rest = s.split(delimiter, 1)
    except ValueError:
        key, rest = s, None
    key = int(key)
    if rest is None:
        return self[key]
    return self[key].string_access(rest, delimiter, key_delim)

# monkeypatch CommentedSeq.string_access function
ruamel.yaml.comments.CommentedSeq.string_access = sequence_string_access


def dump_yaml(layered_config):
    # source: https://github.com/vmfarms/farmer/blob/e3f8b863b51b21dfa2d11d2453eac86ed0ab9bc9/farmer/commands/config.py
    return ruamel.yaml.round_trip_dump(layered_config.dump(layered_config),
                                       default_flow_style=False)


def yaml_unicode_representer(self, data):
    # source: https://github.com/vmfarms/farmer/blob/e3f8b863b51b21dfa2d11d2453eac86ed0ab9bc9/farmer/commands/config.py
    return self.represent_str(data.encode('utf-8'))


ruamel.yaml.representer.Representer.add_representer(text_type, yaml_unicode_representer)


def match_config(filters, device, kind, default):
    """
    Matches devices against multiple :class:`DeviceFilter`s.

    :param default: default value
    :param list filters: device filters
    :param Device device: device to be mounted
    :returns: value of the first matching filter
    """
    if device is None:
        return default
    matches = (f.value(kind, device)
               for f in filters
               if f.has_value(kind) and f.match(device))
    return next(matches, default)


def get_xdg_config_dir_path():
    # source: home-assistant
    """
    Single directory where user-specific configuration files should be written

    EXAMPLE: $HOME/.config

    :rtype: str
    """
    try:
        # from xdg.BaseDirectory import xdg_config_home as config_home
        from xdg import XDG_CONFIG_HOME as config_home
    except ImportError:
        config_home = os.path.expanduser('~/.config')
    # NOTE: Automatically get function name
    print('Ran {}| config_home={}'.format(sys._getframe().f_code.co_name, config_home))
    return config_home


def get_xdg_data_dir_path():
    # source: home-assistant
    """
    Single directory where user-specific data files should be written.

    EXAMPLE: $HOME/.config/.local/share

    :rtype: str
    """
    try:
        from xdg import XDG_DATA_HOME as data_home
    except ImportError:
        config_home = os.path.expanduser('~/.config')
        data_home = os.path.join(config_home, ".local", "share")
    print('Ran {}| data_home={}'.format(sys._getframe().f_code.co_name, data_home))
    return data_home


def get_xdg_cache_dir_path():
    """
    Single directory where user-specific non-essential (cached) data should be written.

    EXAMPLE: $HOME/.cache

    :rtype: str
    """
    try:
        from xdg import XDG_CACHE_HOME as cache_home
    except ImportError:
        cache_home = os.path.expanduser('~/.cache')
    print('Ran {}| cache_home={}'.format(sys._getframe().f_code.co_name, cache_home))
    return cache_home


def get_config_sub_dir_path():
    """
    Return sub directory for scarlett config files.

    Example: $HOME/.config/scarlett

    :rtype: str
    """
    config_dir = get_xdg_config_dir_path()
    config_sub_dir = os.path.join(config_dir, CONFIG_DIR_NAME)
    print('Ran {}| config_sub_dir={}'.format(sys._getframe().f_code.co_name, config_sub_dir))
    return config_sub_dir


def get_config_file_path():
    # source: home-assistant
    """Look in given directory for supported configuration files.

    EXAMPLE: $HOME/.config/scarlett/config.yaml

    Async friendly.
    """
    config_sub_dir = get_config_sub_dir_path()
    config_file = os.path.join(config_sub_dir, YAML_CONFIG_FILE)
    print('Ran {}| config_file={}'.format(sys._getframe().f_code.co_name, config_file))
    return config_file


def get_version_file_path():
    # source: home-assistant
    """Look in given directory for scarlett version

    EXAMPLE: $HOME/.config/.SCARLETT_VERSION

    Async friendly.
    """
    config_sub_dir = get_config_sub_dir_path()
    version_file = os.path.join(config_sub_dir, VERSION_FILE)
    print('Ran {}| version_file={}'.format(sys._getframe().f_code.co_name, version_file))
    return version_file


def _get_path(yaml_config, path):
    # source: dcos-cli
    """
    :param config: Dict with the configuration values
    :type config: dict
    :param path: Path to the value. E.g. 'path.to.value'
    :type path: str
    :returns: Value stored at the given path
    :rtype: double, int, str, list or dict
    """

    for section in path.split('.'):
        yaml_config = yaml_config[section]

    return yaml_config


def _iterator(parent, dictionary):
    # source: dcos-cli
    """
    :param parent: Path to the value parameter
    :type parent: str
    :param dictionary: Value of the key
    :type dictionary: collection.Mapping
    :returns: An iterator of tuples for each property and value
    :rtype: iterator of (str, any) where any can be str, int, double, list
    """

    for key, value in dictionary.items():

        new_key = key
        if parent is not None:
            new_key = "{}.{}".format(parent, key)

        if not isinstance(value, dict):
            yield (new_key, value)
        else:
            for x in _iterator(new_key, value):
                yield x


def split_key(name):
    # source: dcos-cli
    """
    :param name: the full property path - e.g. marathon.url
    :type name: str
    :returns: the section and property name
    :rtype: (str, str)
    """

    terms = name.split('.', 1)
    if len(terms) != 2:
        raise Exception('Property name must have both a section and '
                            'key: <section>.<key> - E.g. marathon.url')

    return (terms[0], terms[1])


def flatten(d, parent_key='', sep='/'):
    # source: https://github.com/russellballestrini/yaml_consulate/blob/76d74ec7ffe5fd56ee057a619f12dcc8a862b046/yaml_consulate/yaml_consulate.py
    """http://stackoverflow.com/a/6027615"""
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


class SimpleConfig(object):

    """ScarlettOS config in memory representation."""

    def __init__(self, data):
        """
        Initialize with preparsed data object.

        :param ConfigParser data: config file accessor
        """
        self._data = data or {}

        self._scarlett_name = None
        self._coordinates = None
        self._longitude = None
        self._latitude = None
        self._pocketsphinx = None
        self._elevation = None
        self._unit_system = None
        self._time_zone = None
        self._owner_name = None
        self._keyword_list = None
        self._features_enabled = None
        # self._units = METRIC_SYSTEM  # type: UnitSystem

    # FIXME: Figure out if we want to use this or not
    # def as_dict(self):
    #     """Create a dictionary representation of this dict.
    #     """
    #     time_zone = self._time_zone or date_util.UTC

    #     return {
    #         'scarlett_name': self._scarlett_name,
    #         'pocketsphinx': self._pocketsphinx,
    #         'latitude': self._latitude,
    #         'longitude': self._longitude,
    #         'elevation': self._elevation,
    #         # 'unit_system': self._units.as_dict(),
    #         'unit_system': self._unit_system,
    #         'owner_name': self._owner_name,
    #         'keyword_list': self._keyword_list,
    #         'features_enabled': self._features_enabled,
    #         # 'location_name': self._location_name,
    #         'time_zone': time_zone.zone,
    #         'version': __version__
    #     }

    def dump_config(self):
        return dump_yaml(self._data)

    def _empty_config(self):
        # source: home-assistant
        """Return an empty config."""
        return {}

    def _get_value(self, data, config_key):
        # source: home-assistant
        """Get value."""
        return data.get(config_key, {})

    # FIXME: I want to use this guy ... but since self._data is a layeredconfig obj, we can't currently.
    # def get_value(self, path, **kw):
    #     # source: https://stackoverflow.com/questions/39463936/python-accessing-yaml-values-using-dot-notation
    #     """
    #     Get configuration variables using dot notation.

    #     :param path: path to value inside yaml config. Eg. 'scarlett.pocketsphinx.hmm'
    #     :type name: str

    #     :param *kw: Keyword arguments expected by ruamel.yaml CommentMap.string_access(). eg [delimiter=None, key_delim=None]
    #     :type name: keyword arguments

    #     """
    #     return self._data.string_access(path, **kw)

    def _write_value(self, data, config_key, new_value):
        # source: home-assistant
        """Set value."""
        # NOTE: dict.setdefault(key, default)
        # key -- This is the key to be searched.
        # default -- This is the Value to be returned in case key is not found.
        # source: https://www.tutorialspoint.com/python/dictionary_setdefault.htm
        # NOTE: dict.update(dict2)
        # DESCRIPTION: The method update() adds dictionary dict2's key-values pairs in to dict.
        # This function does not return anything.
        # dict2 -- This is the dictionary to be added into dict.
        # source: https://www.tutorialspoint.com/python/dictionary_update.htm
        data.setdefault(config_key, {}).update(new_value)

    @classmethod
    def ensure_config_exists(cls, detect_location):
        # source: home-assistant
        """Ensure a config file exists in given configuration directory.

        Creating a default one if needed.
        Return path to the config file.
        """

        config_path = get_config_file_path()

        # if file doesn't exist, create it
        if not os.path.isfile(config_path):
            print("Unable to find configuration. Creating default one in",
                  config_path)
            config_path = cls.create_default_config(detect_location)

        return config_path

    @classmethod
    def ensure_config_file(cls):
        # NOTE: borrowed from home-assistant
        """
        Ensure actual configuration file exists.

        :rtype str (eg. $HOME/.config/scarlett/config.yaml)

        """

        config_file_path = get_config_file_path()
        print('Ran {}| config_file_path={}'.format(sys._getframe().f_code.co_name, config_file_path))

        config_path = cls.ensure_config_exists(True)
        # NOTE: Below is how dcos-cli does it
        # util.ensure_file_exists(path)
        # util.enforce_file_permissions(path)

        # FIXME: This condition never gets met, fix it
        if config_path is None:
            print('Error getting configuration path')
            # FIXME: I don't think we want to exit on error
            sys.exit(1)

        return config_path

    # check if config exists
    @classmethod
    def ensure_config_dir_path(cls, config_dir: str) -> None:
        # NOTE: borrowed from home-assistant
        """Validate the configuration directory."""

        # Test if configuration directory exists
        if not os.path.isdir(config_dir):
            if config_dir != get_config_sub_dir_path():
                print(('Fatal Error: Specified configuration directory does '
                       'not exist {} ').format(config_dir))
                # FIXME: Do we want this to exit?
                sys.exit(1)

            try:
                print('Ran {}| os.mkdir(config_dir)={}'.format(sys._getframe().f_code.co_name, config_dir))
                mkdir_if_does_not_exist(config_dir)
            except OSError:
                print(('Fatal Error: Unable to create default configuration '
                       'directory {} ').format(config_dir))
                # FIXME: Do we want this to exit?
                sys.exit(1)

    @classmethod
    def create_default_config(cls, detect_location=True):
        # source: home-assistant
        """Create a default configuration file in given configuration directory.

        Return path to new config file if success, None if failed.
        This method needs to run in an executor.
        """
        config_path = get_config_file_path()
        version_path = get_version_file_path()
        # group_yaml_path = os.path.join(config_dir, GROUP_CONFIG_PATH)
        # automation_yaml_path = os.path.join(config_dir, AUTOMATION_CONFIG_PATH)

        from scarlett_os.internal.debugger import dump
        from scarlett_os.internal.debugger import pprint_color

        # from tuple DEFAULT_CORE_CONFIG create a dictonary of key and default values
        info = {attr: default for attr, default, _, _ in DEFAULT_CORE_CONFIG}

        print('[info]')
        dump(info)
        print('[pprint_color(info)]')
        pprint_color(info)

        location_info = detect_location and loc_util.detect_location_info()

        print('[location_info]')
        dump(location_info)

        if location_info:
            if location_info.use_metric:
                info[CONF_UNIT_SYSTEM] = CONF_UNIT_SYSTEM_METRIC
            else:
                info[CONF_UNIT_SYSTEM] = CONF_UNIT_SYSTEM_IMPERIAL

            for attr, default, prop, _ in DEFAULT_CORE_CONFIG:
                if prop is None:
                    continue
                info[attr] = getattr(location_info, prop) or default

            if location_info.latitude and location_info.longitude:
                info[CONF_ELEVATION] = loc_util.elevation(location_info.latitude,
                                                          location_info.longitude)

        # Writing files with YAML does not create the most human readable results
        # So we're hard coding a YAML template.
        try:
            with open(config_path, 'w') as config_file:
                # NOTE: This use to have 'homeautomation:'
                # NOTE: We replaced it with ---
                # FIXME: Should we try using http://yaml.org/type/omap.html ?
                # config_file.write("scarlett: !!omap\n")
                config_file.write("scarlett:\n")

                for attr, _, _, description in DEFAULT_CORE_CONFIG:
                    print("attr:{}".format(attr))
                    print("info:{}".format(info))
                    if info[attr] is None:
                        continue
                    elif description:
                        print("description:{}".format(description))
                        config_file.write("  # {}\n".format(description))  # NOTE: Removed 2 white spaces to make yaml file flat
                    config_file.write("  {}: {}\n".format(attr, info[attr]))  # NOTE: Removed 2 white spaces to make yaml file flat

                config_file.write(DEFAULT_CONFIG)

            # NOTE: Write version file next
            # NOTE: wt = write/text-mode
            # source: https://stackoverflow.com/questions/23051062/open-files-in-rt-and-wt-modes
            with open(version_path, 'wt') as version_file:
                version_file.write(__version__)

            # TODO: Re-enable this eventually? This allows for multiple yaml files diff configs
            # with open(group_yaml_path, 'w'):
            #     pass

            # with open(automation_yaml_path, 'wt') as fil:
            #     fil.write('[]')

            return config_path

        except IOError:
            print('Unable to create default configuration file', config_path)
            return None

    @classmethod
    def create_default_config_and_load(cls):
        """Create a default configuration file then load it into memory.

        Return dictonary describing config data if success, None if failed.
        """

        # FIXME: Move these guys into their own classmethod
        # Step 1: get $HOME/.config/scarlett dir
        config_sub_dir = get_config_sub_dir_path()
        config_home = get_config_file_path()
        version_path = get_version_file_path()

        # Step 2: Make sure that folder is created already
        mkdir_if_does_not_exist(config_sub_dir)

        # Step 3. Make sure $HOME/.config/scarlett dir exists.
        # If it doesn't exists, then it creates a default one
        config_file_path = cls.ensure_config_file()

        # Step 4. load in config file to dict
        config_dict = cls.from_file(config_file_path)

        return config_dict

    @classmethod
    def default_paths(cls):
        """
        Return the default config file paths.

        EXAMPLE: $HOME/.config/scarlett/config.yaml

        :rtype: list
        """
        config_home = get_config_file_path()

        return [config_home]

    # FIXME: Enable this guy
    # NOTE: Malcolm start to finish classmethod
    @classmethod
    def from_dict_with_checks(cls, config_dict={}):
        """
        Read config file from disk.
        """
        pass

    @classmethod
    def from_file(cls, path=None):
        """
        Read config file.

        :param str path: YAML config file name
        :returns: configuration object
        :rtype: Config
        :raises IOError: if the path does not exist
        """
        # NOTE: path not defined, use default config locations
        if path is None:
            for path in cls.default_paths():
                try:
                    print('Ran {}| cls.from_file(path)'.format(sys._getframe().f_code.co_name))
                    return cls.from_file(path)
                except IOError as e:
                    logger.debug(_("Failed to read config file: {0}".format(e)))
                    print('Ran {}| IOError'.format(sys._getframe().f_code.co_name))
                except ImportError as e:
                    logger.warning(_("Failed to read {0!r}: {1}".format(path, e)))
                    print('Ran {}| ImportError'.format(sys._getframe().f_code.co_name))
            print('Ran {}| cls(EMPTY_DICT)'.format(sys._getframe().f_code.co_name))
            return cls({})
        # False/'' => no config
        if not path:
            print('Ran {}| if not path | cls(EMPTY_DICT)'.format(sys._getframe().f_code.co_name))
            return cls({})
        # if os.path.splitext(path)[1].lower() == '.json':
        #     from json import load
        # else:
        #     load = yaml_load
        print('Ran {}| with open(path) as f: | return cls(LayeredConfig(RoundTripYAMLFile(path)))'.format(sys._getframe().f_code.co_name))
        # load = LayeredConfig(RoundTripYAMLFile(path))
        # with open(path) as f:
        return cls(LayeredConfig(RoundTripYAMLFile(path)))

    @property
    def scarlett_name(self):
        """Get ScarlettOS name setting."""
        return self._data.get('name', 'Scarlett Home')

    @property
    def coordinates(self):
        """Get latitude and longitude setting. Return type is a tuple."""
        # classmethod somenamedtuple._make(iterable)
        # Class method that makes a new instance from an existing sequence or iterable.
        return CoordinatesTuple._make([self.latitude, self.longitude])

    @property
    def longitude(self):
        """Get longitude setting."""
        return self._data.get('longitude', 0)

    @property
    def latitude(self):
        """Get latitude setting."""
        return self._data.get('latitude', 0)

    @property
    def pocketsphinx(self):
        # NOTE: copy()
        # Return a shallow copy of x.
        # source: https://docs.python.org/3/library/copy.html
        """Get pocketsphinx speech to text settings."""
        return self._data.get('pocketsphinx', {}).copy()

    @property
    def elevation(self):
        """Get elevation settings."""
        return self._data.get('elevation', 0)

    @property
    def unit_system(self):
        """Get unit system settings."""
        return self._data.get('unit_system', 'imperial')

    @property
    def time_zone(self):
        """Get time zone settings."""
        return self._data.get('time_zone', 'UTC')

    @property
    def owner_name(self):
        """Get owner name settings."""
        return self._data.get('owner', 'commander keen')

    @property
    def keyword_list(self):
        """Get keyword list settings."""
        return self._data.get('keywords_list', [])

    @property
    def features_enabled(self):
        """Get features settings."""
        return self._data.get('features', [])


class RoundTripYAMLFile(DictSource):
    # source: https://github.com/vmfarms/farmer/blob/9c7ce44e64b6df98a8b4d311cd43900d5060e282/farmer/config.py

    def __init__(self, yaml_filename=None, writable=True, **kwargs):
        """
        Loads and optionally saves configuration files in YAML
        format using the ruamel.yaml RoundTripLoader, which preserves comments.
        Args:
            yamlfile (str): The name of a YAML file. Nested
                            sections are turned into nested config objects.
            writable (bool): Whether changes to the LayeredConfig object
                             that has this YAMLFile object amongst its
                             sources should be saved in the YAML file.
        """
        super(RoundTripYAMLFile, self).__init__(**kwargs)
        if yaml_filename is None and 'parent' in kwargs and hasattr(kwargs['parent'], 'yaml_filename'):
            yaml_filename = kwargs['parent'].yaml_filename
        if 'defaults' in kwargs:
            self.source = kwargs['defaults']
        elif kwargs.get('empty', False):
            self.source = {}
        else:
            with codecs.open(yaml_filename, encoding='utf-8') as yaml_file:
                self.source = ruamel.yaml.round_trip_load(yaml_file.read())
        self.yaml_filename = yaml_filename
        self.dirty = False
        self.writable = writable
        self.encoding = 'utf-8'

    def save(self):
        if self.yaml_filename:
            with codecs.open(self.yaml_filename, 'w', encoding=self.encoding) as yaml_file:
                ruamel.yaml.round_trip_dump(self.source, yaml_file, default_flow_style=False)


# def load_config():
#     # source: https://github.com/vmfarms/farmer/blob/9c7ce44e64b6df98a8b4d311cd43900d5060e282/farmer/config.py
#     """
#     Searches a standard set of locations for .farmer.yml, and parses the first
#     match.
#     """
#     pwd = os.getcwd()
#     paths = [os.path.join(pwd, '.farmer.yml'),
#              os.path.join(pwd, '.farmer', 'farmer.yml'),
#              os.path.join(DEFAULT_CONFIG_DIR, 'farmer.yml')]
#     config_file = None
#     for path in paths:
#         if os.path.exists(path):
#             config_file = path
#             break
#     return LayeredConfig(Defaults(DEFAULTS), RoundTripYAMLFile(config_file))


if __name__ == "__main__":
    import signal
    if os.environ.get('SCARLETT_DEBUG_MODE'):
        import faulthandler
        faulthandler.register(signal.SIGUSR2, all_threads=True)

        from scarlett_os.internal.debugger import init_debugger
        init_debugger()

        from scarlett_os.internal.debugger import enable_remote_debugging
        enable_remote_debugging()

    from scarlett_os.logger import setup_logger
    setup_logger()

    import imp
    import os.path
    import sys

    import tempfile
    import shutil

    import scarlett_os
    from scarlett_os.common.configure import smart_config

    from scarlett_os.internal.debugger import dump
    from scarlett_os.internal.debugger import pprint_color

    temp_config = smart_config.Config.create_default_config_and_load()

    print(temp_config.dump_config())


# FIXME: Playing around w/ ruamel output and defaults
# In [7]: temp_config = ruamel.yaml.round_trip_load(DEFAULT_CONFIG)

# In [8]: temp_config
# Out[8]:
# CommentedMap([('owners_name', 'Hair Ron Jones'),
#               ('pocketsphinx',
#                CommentedMap([('hmm',
#                               '/home/pi/.virtualenvs/scarlett_os/share/pocketsphinx/model/en-us/en-us'),
#                              ('lm',
#                               '/home/pi/dev/bossjones-github/scarlett_os/static/speech/lm/1473.lm'),
#                              ('dict',
#                               '/home/pi/dev/bossjones-github/scarlett_os/static/speech/dict/1473.dic'),
#                              ('silprob', 0.1),
#                              ('wip', 0.0001),
#                              ('bestpath', 0)])),
#               ('keywords_list', ['scarlett', 'SCARLETT']),
#               ('features', ['time', 'help', 'party'])])

# In [9]:


# DEFAULT_CONFIG = """
# # Omitted values in this section will be auto detected using freegeoip.io

# # Name for Scarlett to call user
# owners_name: 'Hair Ron Jones'

# pocketsphinx:
#     hmm: /home/pi/.virtualenvs/scarlett_os/share/pocketsphinx/model/en-us/en-us
#     lm: /home/pi/dev/bossjones-github/scarlett_os/static/speech/lm/1473.lm
#     dict: /home/pi/dev/bossjones-github/scarlett_os/static/speech/dict/1473.dic
#     silprob: 0.1
#     wip: 1e-4
#     bestpath: 0

# keywords_list:
# - 'scarlett'
# - 'SCARLETT'

# features:
# - time
# - help
# - party
# """
