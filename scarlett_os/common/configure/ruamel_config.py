#!/usr/bin/env python3  # NOQA
# -*- coding: utf-8 -*-

# TODO: 2/24/2018 - Try to get the most simplified ruamel config working

#################################
# NOTE: basic yaml terminology converted to python primitaves, based on yaml 1.2 docs

# Nodes = A YAML node represents a single native data structure. Such nodes have content of one of three kinds: scalar, sequence, or mapping. In addition, each node has a tag which serves to restrict the set of possible values the content can have.

# sequence = array ... Extended: The content of a sequence node is an ordered series of zero or more nodes. In particular, a sequence may contain the same node more than once. It could even contain itself(directly or indirectly).

# mappings = dict ... Extended: The content of a mapping node is an unordered set of key: value node pairs, with the restriction that each of the keys is unique. YAML places no further restrictions on the nodes. In particular, keys may be arbitrary nodes, the same node may be used as the value of several key: value pairs, and a mapping could even contain itself as a key or a value (directly or indirectly).

# scalar = str or another yaml node obj ... Extended: The content of a scalar node is an opaque datum that can be presented as a series of zero or more Unicode characters.


#################################

from __future__ import absolute_import, unicode_literals

import codecs
import collections
import fnmatch
import logging
import os
import shutil
import sys
import tempfile
import shutil
from collections import OrderedDict
from gettext import gettext as _
from time import time
from typing import Any, Dict, Optional
import uuid

# ruamel.yaml supports round-trip preserving dict ordering,
# comments, etc., which is why we use it instead of the usual yaml
# module. Remember the project file is intended to go into source
# control.
import ruamel.yaml  # pragma: no cover
from ruamel.yaml import YAML  # pragma: no cover
from ruamel.yaml.error import YAMLError  # pragma: no cover
from ruamel.yaml.comments import CommentedMap  # pragma: no cover
from ruamel.yaml.comments import CommentedSeq  # pragma: no cover
from ruamel.yaml.compat import StringIO  # pragma: no cover

import voluptuous as vol
from layeredconfig import Defaults, DictSource, LayeredConfig
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
from scarlett_os.internal.path import mkdir_if_does_not_exist, ensure_dir_exists
from scarlett_os.internal.rename import rename_over_existing
from scarlett_os.utility import dt as date_util
from scarlett_os.utility import location as loc_util

import xdg


# SOURCE: Ruamel docs, "Output of dump() as a string"
class MyYAML(YAML):  # pragma: no cover
    """[More memory efficent YAML dump]
    """

    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()

logger = logging.getLogger(__name__)

# NOTE: (bytes, int, str, str)
SCALARS = (bytes,) + integer_types + string_types + (text_type,)

# yaml = YAML()
# TODO: Do we want to use this or not? See ruamel section "Output of dump() as a string"
# TODO: #
yaml = MyYAML() # or typ='safe'/'unsafe' etc
yaml.explicit_start = True
yaml.indent = 4
yaml.block_seq_indent = 2
yaml.version = (1, 2)  # set yaml version to 1.2
# yaml.allow_unicode = False

# FIXME: YANGNI
if ruamel.yaml.version_info < (0, 15):
    logger.error("ruamel version less than 0.15.x!")
else:
    logger.error("ruamel version greater than 0.15.x!")

# source: ruamel.yaml test_collections.py
# class TestOrderedDict:
#     def test_ordereddict(self):
#         assert ruamel.yaml.dump(OrderedDict()) == '!!omap []\n'


# NOTE: We are using https://github.com/srstevenson/xdg
# NOTE: This enforces the [XDG Base Directory Specification]
# https://specifications.freedesktop.org/basedir-spec/basedir-spec-0.6.html

# NOTEL Shamelesssly borrowed from udiskie
# source: https://github.com/coldfix/udiskie/blob/master/udiskie/config.py

YAML_CONFIG_FILE = 'config.yaml'
CONFIG_DIR_NAME = 'scarlett'
VERSION_FILE = '.SCARLETT_VERSION'

CoordinatesTuple = collections.namedtuple(
    'Coordinates', ['latitude', 'longitude'])

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
    # source:
    # https://stackoverflow.com/questions/39463936/python-accessing-yaml-values-using-dot-notation
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
    # source:
    # https://stackoverflow.com/questions/39463936/python-accessing-yaml-values-using-dot-notation
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
    # source:
    # https://github.com/vmfarms/farmer/blob/e3f8b863b51b21dfa2d11d2453eac86ed0ab9bc9/farmer/commands/config.py
    return ruamel.yaml.round_trip_dump(layered_config.dump(layered_config),
                                       default_flow_style=False)


def yaml_unicode_representer(self, data):
    # source:
    # https://github.com/vmfarms/farmer/blob/e3f8b863b51b21dfa2d11d2453eac86ed0ab9bc9/farmer/commands/config.py
    return self.represent_str(data.encode('utf-8'))


ruamel.yaml.representer.Representer.add_representer(
    text_type, yaml_unicode_representer)


#########################################################


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
    logger.debug('Ran {}| config_home={}'.format(
        sys._getframe().f_code.co_name, config_home))
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
    logger.debug('Ran {}| data_home={}'.format(
        sys._getframe().f_code.co_name, data_home))
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
    logger.debug('Ran {}| cache_home={}'.format(
        sys._getframe().f_code.co_name, cache_home))
    return cache_home


def get_config_sub_dir_path():
    """
    Return sub directory for scarlett config files.

    Example: $HOME/.config/scarlett

    :rtype: str
    """
    config_dir = get_xdg_config_dir_path()
    config_sub_dir = os.path.join(config_dir, CONFIG_DIR_NAME)
    logger.debug('Ran {}| config_sub_dir={}'.format(
        sys._getframe().f_code.co_name, config_sub_dir))
    return config_sub_dir


def get_config_file_path():
    # source: home-assistant
    """Look in given directory for supported configuration files.

    EXAMPLE: $HOME/.config/scarlett/config.yaml

    Async friendly.
    """
    config_sub_dir = get_config_sub_dir_path()
    config_file = os.path.join(config_sub_dir, YAML_CONFIG_FILE)
    logger.debug('Ran {}| config_file={}'.format(
        sys._getframe().f_code.co_name, config_file))
    return config_file


def get_version_file_path():
    # source: home-assistant
    """Look in given directory for scarlett version

    EXAMPLE: $HOME/.config/.SCARLETT_VERSION

    Async friendly.
    """
    config_sub_dir = get_config_sub_dir_path()
    version_file = os.path.join(config_sub_dir, VERSION_FILE)
    logger.debug('Ran {}| version_file={}'.format(
        sys._getframe().f_code.co_name, version_file))
    return version_file
#########################################################

def _fake_config():
    """Create a temporary config file."""
    base = tempfile.mkdtemp()
    logger.debug("base tempfile: {}".format(base))
    config_file = os.path.join(base, 'config.yaml')

    #############################################################
    # Example of config_file:
    #############################################################
    #  ⌁ pi@scarlett-ansible-manual1604-2  ~  ll /tmp/tmpnxz2wsa2
    # total 12
    # drwx------  2 pi   pi   4096 Feb 24 15:58 ./
    # drwxrwxrwt 15 root root 4096 Feb 24 15:58 ../
    # -rw-rw-r--  1 pi   pi   1034 Feb 24 15:58 config.yaml
    # ⌁ pi@scarlett-ansible-manual1604-2  ~
    #############################################################

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
    # temp_config = simple_config.SimpleConfig.from_file(config_file)

    # yield temp_config

    # shutil.rmtree(base)

    return base, config_file

def _load_fake_config(yaml_filename):
    """Load a yaml file into memory using ruamel.yaml.round_trip_load

    Arguments:
        yaml_filename {[str]} -- [path to yaml file, eg /tmp/tmpnxz2wsa2/config.yaml]
    """

    # INFO: Important ruamel details
    # INFO: How to set yaml version. Add to top of yaml file: %YAML 1.2 before ---
    # INFO: 1.2 does NOT support - Unquoted Yes and On as alternatives for True and No and Off for False.

    with codecs.open(yaml_filename, encoding='utf-8') as yaml_file:
        source = ruamel.yaml.round_trip_load(yaml_file.read())

    return source

def tr(s):
    """[If you need to transform a string representation of the output provide a function that takes a string as input and returns one]

    Arguments:
        s {[str]} -- [string representation of a ruamel config]

    Returns:
        [str] -- [string that has had all new lines replaced]
    """

    return s.replace('\n', '<\n') # such output is not valid YAML!

def _dump_in_memory_config_to_stdout_and_transform(data, stream=None):
    """[dump in memory config and use tr function to transform the data dynamically]

    Arguments:
        data {[ruamel.yaml.comments.CommentedMap]} -- [CommentedMap object]
    """

    if stream is None:
        inefficient = True
        yaml.dump(data, sys.stdout, transform=tr)
        print()  # or sys.stdout.write('\n')
    else:
        inefficient = False
        print(yaml.dump(data, transform=tr))

    logger.debug('Ran {} | stream={} | inefficient={}'.format(sys._getframe().f_code.co_name, stream, inefficient))


def _dump_in_memory_config_to_stdout(data, stream=None):
    """[dump in memory config]

    Arguments:
        data {[ruamel.yaml.comments.CommentedMap]} -- [CommentedMap object]
    """

    # NOTE: on ruamel.yaml.comments.CommentedMap
    # The CommentedMap, which is the dict like construct one gets when
    # round-trip loading, supports insertion of a key into a particular position, while optionally adding a comment:

    if stream is None:
        inefficient = True
        yaml.dump(data, sys.stdout)
        print()  # or sys.stdout.write('\n')
    else:
        inefficient = False
        print(yaml.dump(data))

    logger.debug('Ran {} | stream={} | inefficient={}'.format(sys._getframe().f_code.co_name, stream, inefficient))

def _insert_key_to_commented_map(data, position, key_name, key_value, comment=None):
    # type: (Any, Any, Any, Optional[Any]) -> ruamel.yaml.comments.CommentedMap
    """[summary]

    Arguments:
        data {[ruamel.yaml.comments.CommentedMap]} -- [CommentedMap returned via a roundtrip load]
        position {[int]} -- [int providing position where to insert value, eg 1]
        key_name {[str]} -- [string value for key value, eg 'Full Name']
        key_value {[str]} -- [string value for key value, eg 'Malcolm Jones']

    Keyword Arguments:
        comment {[ANY,str]} -- [Optional inline comment] (default: {None})

    Returns:
        [ruamel.yaml.comments.CommentedMap] -- [Modified ruamel.yaml.comments.CommentedMap]
    """

    # TODO: Validation
    # 1. assert position is valid number
    # 2. assert key_name in string format
    # 3. assert key_value in string format
    # 4. assert comment is kwarg with value in string format
    data.insert(position, key_name, key_value, comment=comment)

    # EXAMPLE: taken directly from ruamel docs
    # data.insert(1, 'last name', 'Vandelay', comment="new key")
    return data

# INFO: ruamel: Indentation of block sequences
# INFO: It is best to always have sequence >= offset + 2 but this is not
# enforced. Depending on your structure, not following this advice might lead to invalid output.

##########################################################################
# INFO: ruamel: extending round trip capabilities
# There are normally six files involved when extending the roundtrip capabilities: the reader, parser, composer and
# constructor to go from YAML to Python and the resolver, representer, serializer and emitter to go the other way.
#################################################################################

##########################################################################
# TODO: 2/24/2018
# FIXME: Make a convience function to pull back values in a generic way similar to the following
# EXAMPLE: ruamel: extracting exact values from yaml in memory
# yaml_str = """\
# a:
# - b:
# c: 42
# - d:
# f: 196
# e:
# g: 3.14
# """
# data = yaml.load(yaml_str)
# INFO: mlget = multi-level get that expects dicts within dicts
# assert data.mlget(['a', 1, 'd', 'f'], list_ok=True) == 196
##########################################################################


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
    # from scarlett_os.common.configure import ruamel_config

    from scarlett_os.internal.debugger import dump
    from scarlett_os.internal.debugger import pprint_color

    # temp_config = ruamel_config.Config.create_default_config_and_load()

    fake_config_file_path_base, fake_config_file_path = _fake_config()

    in_memory_config = _load_fake_config(fake_config_file_path)

    # import pdb
    # pdb.set_trace()  # pylint: disable=no-member

    # TODO: Figure out best way to use ruamel to load this in, and use it correctly

    _dump_in_memory_config_to_stdout_and_transform(in_memory_config)

    # logger.debug(temp_config.dump_config())

    # cleanup temporary folder when finished
    shutil.rmtree(fake_config_file_path_base)
