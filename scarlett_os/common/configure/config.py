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

from scarlett_os.compat import basestring

from gettext import gettext as _

logger = logging.getLogger(__name__)

# NOTE: We are using https://github.com/srstevenson/xdg
# NOTE: This enforces the [XDG Base Directory Specification] https://specifications.freedesktop.org/basedir-spec/basedir-spec-0.6.html

# NOTEL Shamelesssly borrowed from udiskie
# source: https://github.com/coldfix/udiskie/blob/master/udiskie/config.py


__all__ = ['match_config',
           'Config']

CoordinatesTuple = collections.namedtuple('Coordinates', ['latitude', 'longitude'])

def lower(s):
    try:
        return s.lower()
    except AttributeError:
        return s


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
        pass
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


class Config(object):

    """ScarlettOS config in memory representation."""

    def __init__(self, data):
        """
        Initialize with preparsed data object.

        :param ConfigParser data: config file accessor
        """
        self._data = data or {}

    @classmethod
    def default_pathes(cls):
        """
        Return the default config file pathes.

        :rtype: list
        """
        try:
            # from xdg.BaseDirectory import xdg_config_home as config_home
            from xdg import XDG_CONFIG_HOME as config_home
        except ImportError:
            config_home = os.path.expanduser('~/.config')
        return [os.path.join(config_home, 'scarlett', 'config.yml'),
                os.path.join(config_home, 'scarlett', 'config.json')]

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
            for path in cls.default_pathes():
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

    # @property
    # def program_options(self):
    #     """Get the program options dictionary from the config file."""
    #     # NOTE: copy()
    #     # Return a shallow copy of x.
    #     # source: https://docs.python.org/3/library/copy.html
    #     return self._data.get('program_options', {}).copy()

    # @property
    # def notifications(self):
    #     """Get the notification timeouts dictionary from the config file."""
    #     # NOTE: copy()
    #     # Return a shallow copy of x.
    #     # source: https://docs.python.org/3/library/copy.html
    #     return self._data.get('notifications', {}).copy()

    # @property
    # def icon_names(self):
    #     """Get the icon names dictionary from the config file."""
    #     # NOTE: copy()
    #     # Return a shallow copy of x.
    #     # source: https://docs.python.org/3/library/copy.html
    #     return self._data.get('icon_names', {}).copy()

    # @property
    # def notification_actions(self):
    #     """Get the notification actions dictionary from the config file."""
    #     # NOTE: copy()
    #     # Return a shallow copy of x.
    #     # source: https://docs.python.org/3/library/copy.html
    #     return self._data.get('notification_actions', {}).copy()

    @property
    def scarlett_name(self):
        """Get ScarlettOS name setting."""
        # NOTE: copy()
        # Return a shallow copy of x.
        # source: https://docs.python.org/3/library/copy.html
        return self._data.get('name', 'scarlett')

    @property
    def coordinates(self):
        """Get latitude and longitude setting. Return type is a tuple."""
        # classmethod somenamedtuple._make(iterable)
        # Class method that makes a new instance from an existing sequence or iterable.
        return CoordinatesTuple._make([self.latitude, self.longitude])

    @property
    def longitude(self):
        """Get longitude setting."""
        # NOTE: copy()
        # Return a shallow copy of x.
        # source: https://docs.python.org/3/library/copy.html
        return self._data.get('longitude', 0)

    @property
    def latitude(self):
        """Get latitude setting."""
        # NOTE: copy()
        # Return a shallow copy of x.
        # source: https://docs.python.org/3/library/copy.html
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
        # NOTE: copy()
        # Return a shallow copy of x.
        # source: https://docs.python.org/3/library/copy.html
        return self._data.get('elevation', 0)

    @property
    def unit_system(self):
        """Get unit system settings."""
        # NOTE: copy()
        # Return a shallow copy of x.
        # source: https://docs.python.org/3/library/copy.html
        return self._data.get('unit_system', 0)

    @property
    def time_zone(self):
        """Get time zone settings."""
        # NOTE: copy()
        # Return a shallow copy of x.
        # source: https://docs.python.org/3/library/copy.html
        return self._data.get('time_zone', 'UTC')

    @property
    def owner_name(self):
        """Get owner name settings."""
        # NOTE: copy()
        # Return a shallow copy of x.
        # source: https://docs.python.org/3/library/copy.html
        return self._data.get('owner', 'commander keen')

    @property
    def keyword_list(self):
        """Get keyword list settings."""
        # NOTE: copy()
        # Return a shallow copy of x.
        # source: https://docs.python.org/3/library/copy.html
        return self._data.get('keywords_list', [])

    @property
    def features_enabled(self):
        """Get features settings."""
        # NOTE: copy()
        # Return a shallow copy of x.
        # source: https://docs.python.org/3/library/copy.html
        return self._data.get('features', [])
