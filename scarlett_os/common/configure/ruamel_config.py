#!/usr/bin/env python3  # NOQA
# -*- coding: utf-8 -*-

"""ruamel_config, yaml based config object using the ruamel python module"""

# pylint: disable=line-too-long
# pylint: disable=W1202

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
import re
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

RE_ASCII = re.compile(r"\033\[[^m]*m")  # source: home-assistant

# FIXME: YANGNI
if ruamel.yaml.version_info < (0, 15):
    logger.error("ruamel version less than 0.15.x!")
else:
    logger.error("ruamel version greater than 0.15.x!")

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
    (CONF_NAME, 'Scarlett Home', None, 'Name of the location where Scarlett System is '
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

# FIXME: Old defaults 2/25/2018
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

DEFAULT_CONFIG = """
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
"""


def lower(a_string):
    """[Make string lowercase.]

    Arguments:
        a_string {[str]} -- [takes string and converts all characters to lowercase]

    Returns:
        [str] -- [returns transformed string, in all lowercase]
    """
    try:
        return a_string.lower()
    except AttributeError:
        return a_string


def flatten(d, parent_key='', sep='/'):
    # source: http://stackoverflow.com/a/6027615
    # source:
    # https://github.com/russellballestrini/yaml_consulate/blob/76d74ec7ffe5fd56ee057a619f12dcc8a862b046/yaml_consulate/yaml_consulate.py
    """[summary]

    Arguments:
        d {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# FIXME: add valid docblock
def mapping_string_access(self, s, delimiter=None, key_delim=None):
    """[summary]

    Arguments:
        s {[type]} -- [description]

    Keyword Arguments:
        delimiter {[type]} -- [description] (default: {None})
        key_delim {[type]} -- [description] (default: {None})

    Returns:
        [type] -- [description]
    """

    # FIXME: Make this into a real docstring
    # source:
    # https://stackoverflow.com/questions/39463936/python-accessing-yaml-values-using-dot-notation
    def p(v):
        """[summary]

        Arguments:
            v {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        try:
            v = int(v)
        except Exception:
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

# FIXME: add valid docblock
def sequence_string_access(self, s, delimiter=None, key_delim=None):
    """[summary]

    Arguments:
        s {[type]} -- [description]

    Keyword Arguments:
        delimiter {[type]} -- [description] (default: {None})
        key_delim {[type]} -- [description] (default: {None})

    Returns:
        [type] -- [description]
    """

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

# def dump_yaml(layered_config):
#     """[summary]

#     Arguments:
#         layered_config {[type]} -- [description]

#     Returns:
#         [type] -- [description]
#     """

#     # source:
#     # https://github.com/vmfarms/farmer/blob/e3f8b863b51b21dfa2d11d2453eac86ed0ab9bc9/farmer/commands/config.py
#     return ruamel.yaml.round_trip_dump(layered_config.dump(layered_config),
#                                        default_flow_style=False)

def yaml_unicode_representer(self, data):
    """[Override ruamel.yaml.representer.Representer ]

    Arguments:
        data {[str]} -- [In memory yaml representation of yaml file]

    Returns:
        [str] -- [str data in utf-8 format]
    """

    # source:
    # https://github.com/vmfarms/farmer/blob/e3f8b863b51b21dfa2d11d2453eac86ed0ab9bc9/farmer/commands/config.py
    return self.represent_str(data.encode('utf-8'))

ruamel.yaml.representer.Representer.add_representer(
    text_type, yaml_unicode_representer)


#########################################################

# TODO: Allow us to override this value purely for testing purposes 2/25/2018
def get_xdg_config_dir_path(override=None):
    # source: home-assistant
    """
    Single directory where user-specific configuration files should be written

    EXAMPLE: $HOME/.config

    :rtype: str
    """
    # Force location to value provided by kwarg override
    if override is not None:
        config_home = override
        logger.debug('Ran {}| config_home={}'.format(sys._getframe().f_code.co_name, config_home))
        return config_home

    try:
        # from xdg.BaseDirectory import xdg_config_home as config_home
        from xdg import XDG_CONFIG_HOME as config_home
    except ImportError:
        config_home = os.path.expanduser('~/.config')
    # NOTE: Automatically get function name
    logger.debug('Ran {}| config_home={}'.format(
        sys._getframe().f_code.co_name, config_home))
    return config_home

# TODO: Allow us to override this value purely for testing purposes 2/25/2018
def get_xdg_data_dir_path(override=None):
    # source: home-assistant
    """
    Single directory where user-specific data files should be written.

    EXAMPLE: $HOME/.config/.local/share

    :rtype: str
    """

    # Force location to value provided by kwarg override
    if override is not None:
        data_home = override
        logger.debug('Ran {}| data_home={}'.format(
        sys._getframe().f_code.co_name, data_home))
        return data_home

    try:
        from xdg import XDG_DATA_HOME as data_home
    except ImportError:
        config_home = os.path.expanduser('~/.config')
        data_home = os.path.join(config_home, ".local", "share")
    logger.debug('Ran {}| data_home={}'.format(
        sys._getframe().f_code.co_name, data_home))
    return data_home

# TODO: Allow us to override this value purely for testing purposes 2/25/2018


def get_xdg_cache_dir_path(override=None):
    """
    Single directory where user-specific non-essential (cached) data should be written.

    EXAMPLE: $HOME/.cache

    :rtype: str
    """

    # Force location to value provided by kwarg override
    if override is not None:
        cache_home = override
        logger.debug('Ran {}| cache_home={}'.format(
            sys._getframe().f_code.co_name, cache_home))
        return cache_home

    try:
        from xdg import XDG_CACHE_HOME as cache_home
    except ImportError:
        cache_home = os.path.expanduser('~/.cache')
    logger.debug('Ran {}| cache_home={}'.format(
        sys._getframe().f_code.co_name, cache_home))
    return cache_home

# TODO: Allow us to override this value purely for testing purposes 2/25/2018


def get_config_sub_dir_path(override=None):
    """
    Return sub directory for scarlett config files.

    Example: $HOME/.config/scarlett

    :rtype: str
    """
    # Force location to value provided by kwarg override
    if override is not None:
        config_sub_dir = override
        logger.debug('Ran {}| config_sub_dir={}'.format(sys._getframe().f_code.co_name, config_sub_dir))
        return config_sub_dir

    config_dir = get_xdg_config_dir_path()
    config_sub_dir = os.path.join(config_dir, CONFIG_DIR_NAME)
    logger.debug('Ran {}| config_sub_dir={}'.format(sys._getframe().f_code.co_name, config_sub_dir))
    return config_sub_dir

# TODO: Allow us to override this value purely for testing purposes 2/25/2018


def get_config_file_path(override=None):
    # source: home-assistant
    """Look in given directory for supported configuration files.

    EXAMPLE: $HOME/.config/scarlett/config.yaml

    Async friendly.
    """
    # Force location to value provided by kwarg override
    if override is not None:
        config_file = override
        logger.debug('Ran {}| config_file={}'.format(
            sys._getframe().f_code.co_name, config_file))
        return config_file

    config_sub_dir = get_config_sub_dir_path()
    config_file = os.path.join(config_sub_dir, YAML_CONFIG_FILE)
    logger.debug('Ran {}| config_file={}'.format(
        sys._getframe().f_code.co_name, config_file))
    return config_file

# TODO: Allow us to override this value purely for testing purposes 2/25/2018


def get_version_file_path(override=None):
    # source: home-assistant
    """Look in given directory for scarlett version

    EXAMPLE: $HOME/.config/.SCARLETT_VERSION

    Async friendly.
    """
    # Force location to value provided by kwarg override
    if override is not None:
        version_file = override
        logger.debug('Ran {}| version_file={}'.format(
            sys._getframe().f_code.co_name, version_file))
        return version_file

    config_sub_dir = get_config_sub_dir_path()
    version_file = os.path.join(config_sub_dir, VERSION_FILE)
    logger.debug('Ran {}| version_file={}'.format(
        sys._getframe().f_code.co_name, version_file))
    return version_file
#########################################################

def _fake_config(override=None):
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

    if override is not None:
        with open(config_file, 'wt') as f:
            f.write(override)
        return base, config_file

    with open(config_file, 'wt') as f:
        f.write(DEFAULT_CONFIG)

    return base, config_file

def load_fake_config(yaml_filename):
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
    """[Insert a key into a CommentedMap at a particular position, while optionally adding a comment]

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

def get_config_key_position(data, key_name):
    """Return position value of a key in a ruamel CommentedMap

    Arguments:
        data {[ruamel.yaml.comments.CommentedMap]} -- [CommentedMap returned via a roundtrip load]
        key_name {[str]} -- [string value for key value, eg 'Full Name']

    Returns:
        [ANY, tuple] -- [Return a tuple of where node object is located in yaml document or return None]
    """

    # EXAMPLE: Output
    # pdb> in_memory_config.lc.key('pocketsphinx')
    # (9, 0)
    # pdb> in_memory_config.lc.key('pocketsphinxa')
    # *** KeyError: 'pocketsphinxa'
    # pdb>
    try:
        pos = data.lc.key(key_name)
    except KeyError:
        logger.error('Tried to find {} but failed! Setting position return value to None'.format(key_name))
        pos = None

    return pos

def get_config_value_position(data, key_name):
    """Return position value of a key in a ruamel CommentedMap

    Arguments:
        data {[ruamel.yaml.comments.CommentedMap]} -- [CommentedMap returned via a roundtrip load]
        key_name {[str]} -- [string value for key value, eg 'Full Name']

    Returns:
        [ANY, tuple] -- [Return a tuple of where node object is located in yaml document or return None]
    """

    # EXAMPLE: Output
    # pdb> in_memory_config.lc.value('pocketsphinx')
    # (10, 4)
    # pdb> in_memory_config.lc.value('pocketsphinxa')
    # *** KeyError: 'pocketsphinxa'
    # pdb>
    try:
        pos = data.lc.value(key_name)
    except KeyError:
        logger.error('Tried to find {} but failed! Setting position return value to None'.format(key_name))
        pos = None

    return pos

# FIXME: YANGNI
# def get_config_item_position(data, item_pos):
#     """Return position value of a key in a ruamel CommentedMap

#     Arguments:
#         data {[ruamel.yaml.comments.CommentedMap]} -- [CommentedMap returned via a roundtrip load]
#         item_pos {[int]} -- [int value position within scalar]

#     Returns:
#         [ANY, tuple] -- [Return a tuple of where node object is located in yaml document or return None]
#     """

#     # EXAMPLE: Output
#     # pdb> in_memory_config.lc.item(1)
#     # FIXME: GET A REAL RETURN VALUE
#     # pdb> in_memory_config.lc.item(1)
#     # *** KeyError: 1
#     # pdb>
#     try:
#         pos = data.lc.item(item_pos)
#     except KeyError:
#         logger.error('Tried to find {} but failed! Setting position return item to None'.format(item_pos))
#         pos = None

#     return pos

# check if config exists
def ensure_config_dir_path(config_dir: str) -> None:
    # NOTE: borrowed from home-assistant
    """Validate the configuration directory."""

    # Test if configuration directory exists
    if not os.path.isdir(config_dir):
        try:
            print('Ran {}| os.mkdir(config_dir)={}'.format(sys._getframe().f_code.co_name, config_dir))
            mkdir_if_does_not_exist(config_dir)
        except OSError:
            print(('Fatal Error: Unable to create default configuration '
                    'directory {} ').format(config_dir))
            # FIXME: Do we want this to exit?
            sys.exit(1)


# source: chamberlain
def prep_default_config(homedir=None):
    """[setup config.yaml defaults]

    Keyword Arguments:
        homedir {[str]} -- [path to sub directory containing config.yaml file, eg $HOME/.config/scarlett/config.yaml] (default: {None})


    Returns:
        [str] -- [home, eg $HOME/.config/scarlett]
        [str] -- [default_cfg, eg $HOME/.config/scarlett/config.yaml]
    """

    # Step 1. Get sub directory path for config
    if homedir is None:
        home = get_config_sub_dir_path()
    else:
        # override for things like tests
        home = homedir

    # Step 2. ensure sub directory actually exists
    ensure_config_dir_path(home)

    # if not os.path.exists(home):
    #     os.makedirs(home)
    # default_cfg = os.path.join(home, "config.json")

    # FIXME: ? Do we want to make this a function that returns the default_cfg value?
    # Step 3. Set location of config.yaml file
    default_cfg = os.path.join(home, 'config.yaml')

    # Step 4. check if config file exists, if it doesnt, create a default config
    if not os.path.exists(default_cfg):
        # FIXME: Make this default config more dynamically configured, or start using ruamel primitives to override defaults if they aren't set
        with open(default_cfg, 'wt') as f:
            f.write(DEFAULT_CONFIG)

    return home, default_cfg

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

    import imp  # pylint: disable=W0611
    import os.path
    import sys

    import tempfile
    import shutil

    import scarlett_os
    # from scarlett_os.common.configure import ruamel_config

    from scarlett_os.internal.debugger import dump  # pylint: disable=W0611
    from scarlett_os.internal.debugger import pprint_color  # pylint: disable=W0611

    fake_config_file_path_base, fake_config_file_path = _fake_config()

    in_memory_config = load_fake_config(fake_config_file_path)

    # import pdb
    # pdb.set_trace()  # pylint: disable=no-member

    # TODO: Figure out best way to use ruamel to load this in, and use it correctly

    _dump_in_memory_config_to_stdout_and_transform(in_memory_config)

    # cleanup temporary folder when finished
    shutil.rmtree(fake_config_file_path_base)
