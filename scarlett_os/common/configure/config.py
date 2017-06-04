#!/usr/bin/env python3  # NOQA
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging
import os
import sys
import fnmatch
import tempfile
import shutil

import collections
from collections import OrderedDict

from scarlett_os.compat import basestring

from gettext import gettext as _

import voluptuous as vol
from voluptuous.humanize import humanize_error

from time import time
from typing import Any, Optional, Dict
import voluptuous as vol

from scarlett_os.const import (
    CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME, CONF_PACKAGES, CONF_UNIT_SYSTEM,
    CONF_TIME_ZONE, CONF_ELEVATION, CONF_UNIT_SYSTEM_METRIC,
    CONF_UNIT_SYSTEM_IMPERIAL, CONF_TEMPERATURE_UNIT, TEMP_CELSIUS,
    __version__, CONF_CUSTOMIZE, CONF_CUSTOMIZE_DOMAIN, CONF_CUSTOMIZE_GLOB, CONF_OWNERS_NAME)

import scarlett_os.helpers.config_validation as cv
from scarlett_os.utility import dt as date_util, location as loc_util
from scarlett_os.internal import path as path_internal

from scarlett_os.internal.path import isReadable
from scarlett_os.internal.path import path_from_uri
from scarlett_os.internal.path import get_parent_dir
from scarlett_os.internal.path import mkdir_if_does_not_exist
from scarlett_os.internal.path import fname_exists
from scarlett_os.internal.path import touch_empty_file

logger = logging.getLogger(__name__)

# NOTE: We are using https://github.com/srstevenson/xdg
# NOTE: This enforces the [XDG Base Directory Specification] https://specifications.freedesktop.org/basedir-spec/basedir-spec-0.6.html

# NOTEL Shamelesssly borrowed from udiskie
# source: https://github.com/coldfix/udiskie/blob/master/udiskie/config.py


# __all__ = ['match_config',
#            'Config']

YAML_CONFIG_FILE = 'config.yaml'
CONFIG_DIR_NAME = 'scarlett'
VERSION_FILE = '.SCARLETT_VERSION'

CoordinatesTuple = collections.namedtuple('Coordinates', ['latitude', 'longitude'])

# DATA_PERSISTENT_ERRORS = 'bootstrap_persistent_errors'
# HA_COMPONENT_URL = '[{}](https://home-assistant.io/components/{}/)'
# YAML_CONFIG_FILE = 'configuration.yaml'
# VERSION_FILE = '.HA_VERSION'
# CONFIG_DIR_NAME = '.homeassistant'
# DATA_CUSTOMIZE = 'hass_customize'

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
    (CONF_OWNERS_NAME, 'Hair Ron Jones', 'owner_name', 'Name for Scarlett to call user'),
)  # type: Tuple[Tuple[str, Any, Any, str], ...]

# DEFAULT_CONFIG = """
# # Show links to resources in log and frontend
# introduction:

# # Enables the frontend
# frontend:

# # Enables configuration UI
# config:

# http:
#   # Uncomment this to add a password (recommended!)
#   # api_password: PASSWORD
#   # Uncomment this if you are using SSL or running in Docker etc
#   # base_url: example.duckdns.org:8123

# # Checks for available updates
# # Note: This component will send some information about your system to
# # the developers to assist with development of Home Assistant.
# # For more information, please see:
# # https://home-assistant.io/blog/2016/10/25/explaining-the-updater/
# updater:

# # Discover some devices automatically
# discovery:

# # Allows you to issue voice commands from the frontend in enabled browsers
# conversation:

# # Enables support for tracking state changes over time.
# history:

# # View all events in a logbook
# logbook:

# # Track the sun
# sun:

# # Weather Prediction
# sensor:
#   platform: yr

# # Text to speech
# tts:
#   platform: google

# group: !include groups.yaml
# automation: !include automations.yaml
# """

# NOTE: This is how you get a functions name automatically
# source: https://stackoverflow.com/questions/251464/how-to-get-a-function-name-as-a-string-in-python
# sys._getframe().f_code.co_name

DEFAULT_CONFIG = """
# Omitted values in this section will be auto detected using freegeoip.io

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
    CONF_OWNERS_NAME: vol.Coerce(str),
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


def match_value(value, pattern):
    if isinstance(value, (list, tuple)):
        return any(match_value(v, pattern) for v in value)
    if isinstance(value, basestring) and isinstance(pattern, basestring):
        return fnmatch.fnmatch(value.lower(), pattern.lower())
    return lower(value) == lower(pattern)


def yaml_load(stream):
    """Load YAML document, but load all strings as unicode on py2."""
    import yaml

    class UnicodeLoader(yaml.SafeLoader):
        """Yaml SafeLoader Class, default encoding is UTF-8."""
        pass
    # NOTE:
    # In [2]: yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
    # Out[2]: 'tag:yaml.org,2002:map'
    UnicodeLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_SCALAR_TAG,
        UnicodeLoader.construct_scalar)
    return yaml.load(stream, UnicodeLoader)


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


def get_config_dir_path():
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
    print('Ran {}| config_home={}'.format(sys._getframe().f_code.co_name, config_home))
    return config_home


def get_data_dir_path():
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


def get_cache_dir_path():
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
    config_dir = get_config_dir_path()
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


class Config(object):

    """ScarlettOS config in memory representation."""

    def __init__(self, data):
        """
        Initialize with preparsed data object.

        :param ConfigParser data: config file accessor
        """
        self._data = data or {}

    def _load_default_schema(self):
        """
        If called, this still setup the default in memory dictonary
        object representing a scarlett config
        """
        pass

    def _empty_config(self):
        # source: home-assistant
        """Return an empty config."""
        return {}

    def _get_value(self, data, config_key):
        # source: home-assistant
        """Get value."""
        return data.get(config_key, {})

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
    def ensure_config_exists(cls, config_dir, detect_location):
        # source: home-assistant
        """Ensure a config file exists in given configuration directory.

        Creating a default one if needed.
        Return path to the config file.
        """
        # import pdb;pdb.set_trace()

        config_path = get_config_file_path()

        if config_path is None:
            print("Unable to find configuration. Creating default one in",
                  config_dir)
            config_path = cls.create_default_config(detect_location)

        return config_path

    @classmethod
    def ensure_config_file(cls):
        # NOTE: borrowed from home-assistant
        """
        Ensure actual configuration file exists.

        :rtype str (eg. $HOME/.config/scarlett/config.yaml)

        """

        config_sub_dir_path = get_config_sub_dir_path()
        print('Ran {}| config_sub_dir_path={}'.format(sys._getframe().f_code.co_name, config_sub_dir_path))

        config_path = cls.ensure_config_exists(config_sub_dir_path, True)

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
        # lib_dir = os.path.join(config_dir, 'deps')

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

        # # Test if library directory exists
        # if not os.path.isdir(lib_dir):
        #     try:
        #         os.mkdir(lib_dir)
        #     except OSError:
        #         print(('Fatal Error: Unable to create library '
        #                'directory {} ').format(lib_dir))
        #         sys.exit(1)

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

        # from tuple DEFAULT_CORE_CONFIG create a dictonary of key and default values
        info = {attr: default for attr, default, _, _ in DEFAULT_CORE_CONFIG}

        location_info = detect_location and loc_util.detect_location_info()

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
                config_file.write("---\n")

                for attr, _, _, description in DEFAULT_CORE_CONFIG:
                    if info[attr] is None:
                        continue
                    elif description:
                        config_file.write("  # {}\n".format(description))
                    config_file.write("  {}: {}\n".format(attr, info[attr]))

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

        if not fname_exists(config_home):
            touch_empty_file(config_home)

        if not fname_exists(version_path):
            touch_empty_file(version_path)

        # cls.ensure_config_dir_path(config_sub_dir)

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
        # None => use default
        if path is None:
            for path in cls.default_paths():
                try:
                    return cls.from_file(path)
                except IOError as e:
                    logger.debug(_("Failed to read config file: {0}".format(e)))
                except ImportError as e:
                    logger.warning(_("Failed to read {0!r}: {1}".format(path, e)))
            return cls({})
        # False/'' => no config
        if not path:
            return cls({})
        if os.path.splitext(path)[1].lower() == '.json':
            from json import load
        else:
            load = yaml_load
        with open(path) as f:
            return cls(load(f))

    # @property
    # def device_config(self):
    #     device_config = map(DeviceFilter, self._data.get('device_config', []))
    #     mount_options = map(MountOptions, self._data.get('mount_options', []))
    #     ignore_device = map(IgnoreDevice, self._data.get('ignore_device', []))
    #     return list(device_config) + list(mount_options) + list(ignore_device)

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

    # NOTE: Use this as an example
    # @property
    # def scarlett_dbus(self):
    #     """Get the scarlett dbus proxy object"""
    #     if self.__scarlett_dbus is None:
    #         return None
    #     return self.__scarlett_dbus

    # @scarlett_dbus.setter
    # def scarlett_dbus(self, s_dbus):
    #     """Set the scarlett dbus proxy Object
    #     """
    #     if s_dbus is None:
    #         self.__scarlett_dbus = None
    #         return
    #     else:
    #         # Check that proxy object has a Introspect method
    #         proxy_obj = getattr(s_dbus, "Introspect")
    #         if callable(proxy_obj.Introspect):
    #             self.__scarlett_dbus = s_dbus
    #         else:
    #             raise ValueError("proxy_obj.Introspect '{0} is not callable. Something wrong with proxy object!'")

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

# In [2]: yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
# Out[2]: 'tag:yaml.org,2002:map'

# In [3]:

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

    test_config = Config.create_default_config_and_load()