#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ruamel_config
----------------------------------
"""

import builtins  # pylint: disable=W0611
import imp
import os.path
import sys  # pylint: disable=W0611
import unittest  # pylint: disable=W0611
import unittest.mock as mock  # pylint: disable=W0611

import tempfile
import shutil

import pytest

import scarlett_os  # pylint: disable=W0611
from scarlett_os.common.configure import ruamel_config

# from ruamel_config import logging

from tests.conftest import dict_compare
from tests import COMMON_MOCKED_CONFIG


# source:
# https://github.com/YosaiProject/yosai/blob/master/test/isolated_tests/core/conf/conftest.py
@pytest.fixture(scope="function")
def ruamel_config_unit_mocker_stopall(mocker):
    "Stop previous mocks, yield mocker plugin obj, then stopall mocks again"
    print("Called [setup]: mocker.stopall()")
    mocker.stopall()
    print("Called [setup]: imp.reload(ruamel_config)")
    imp.reload(ruamel_config)
    yield mocker
    print("Called [teardown]: mocker.stopall()")
    mocker.stopall()
    print("Called [setup]: imp.reload(ruamel_config)")
    imp.reload(ruamel_config)


@pytest.fixture(scope="function")
def fake_config():
    """Create a temporary config file."""
    base = tempfile.mkdtemp()
    config_file = os.path.join(base, "config.yaml")

    with open(config_file, "wt") as f:
        f.write(ruamel_config.DEFAULT_CONFIG)

    temp_config = ruamel_config.load_config(config_file)

    yield temp_config

    shutil.rmtree(base)


@pytest.fixture(scope="function")
def fake_config_no_values():
    """Create a temporary config file."""
    base = tempfile.mkdtemp()
    config_file = os.path.join(base, "config.yaml")

    temp_config = ruamel_config.load_config(config_file)

    yield temp_config

    shutil.rmtree(base)


@pytest.fixture(scope="function")
def fake_config_empty():
    """Create a temporary config file."""
    base = tempfile.mkdtemp()
    config_file = os.path.join(base, "config.yaml")

    with open(config_file, "wt") as f:
        f.write(
            """
---
"""
        )
    temp_config = ruamel_config.load_config(config_file)

    yield temp_config

    shutil.rmtree(base)


@pytest.fixture(scope="function")
def fake_config_russian_encoding():
    """Create a temporary config file."""
    base = tempfile.mkdtemp()
    config_file = os.path.join(base, "config.yaml")

    with open(config_file, "wt") as f:
        f.write(
            """
---
# Name of the location where ScarlettOS Assistant is running
name: Бага

owner: "Б - Бага"
"""
        )
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

        mock_a_string = temp_mocker.MagicMock(name="mock_a_string")
        mock_a_string.return_value = "HELLO"

        assert ruamel_config.lower(mock_a_string.return_value) == "hello"

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

    def test_yaml_unicode_representer(
        self, ruamel_config_unit_mocker_stopall, fake_config_russian_encoding
    ):
        # yield fixture to var
        temp_russian_config = fake_config_russian_encoding
        # perform a yaml dump and store in variable
        output = ruamel_config.dump_in_memory_config_to_var(
            temp_russian_config, stream=False
        )
        # determine if we got the exact output we expected
        assert (
            output
            == "%YAML 1.2\n---\n# Name of the location where ScarlettOS Assistant is running\nname: Бага\n\nowner: Б - Бага\n"
        )

    def test_get_xdg_config_dir_path(self, ruamel_config_unit_mocker_stopall):
        assert ruamel_config.get_xdg_config_dir_path() == os.path.expanduser(
            "~/.config"
        )

    def test_get_xdg_config_dir_path_raise_import_error(
        self, ruamel_config_unit_mocker_stopall, recwarn
    ):
        mock_get_xdg_config_dir_path = ruamel_config_unit_mocker_stopall.patch(
            "scarlett_os.common.configure.ruamel_config.get_xdg_config_dir_path"
        )
        mock_get_xdg_config_dir_path.side_effect = ImportError()

        with pytest.raises(ImportError):
            scarlett_os.common.configure.ruamel_config.get_xdg_config_dir_path()

        # FIXME: For some reason this broke?
        # with pytest.warns(ImportWarning) as record:
        # assert len(recwarn) == 1
        # assert recwarn[0].message.args[0] == "Hey friend - python module xdg.XDG_CONFIG_HOME is not available"

    def test_get_xdg_data_dir_path(self, ruamel_config_unit_mocker_stopall):
        assert ruamel_config.get_xdg_data_dir_path() == os.path.expanduser(
            "~/.local/share"
        )

    def test_get_xdg_cache_dir_path(self, ruamel_config_unit_mocker_stopall):
        assert ruamel_config.get_xdg_cache_dir_path() == os.path.expanduser("~/.cache")

    def test_get_config_sub_dir_path(self, ruamel_config_unit_mocker_stopall):
        assert ruamel_config.get_config_sub_dir_path() == os.path.expanduser(
            "~/.config/scarlett"
        )

    def test_get_config_file_path(self, ruamel_config_unit_mocker_stopall):
        assert ruamel_config.get_config_file_path() == os.path.expanduser(
            "~/.config/scarlett/config.yaml"
        )

    def test_get_version_file_path(self, ruamel_config_unit_mocker_stopall):
        assert ruamel_config.get_version_file_path() == os.path.expanduser(
            "~/.config/scarlett/.SCARLETT_VERSION"
        )

    def test_get_xdg_config_dir_path_override_not_none(
        self, ruamel_config_unit_mocker_stopall
    ):
        temp_mocker = ruamel_config_unit_mocker_stopall

        mock_logger_debug = temp_mocker.patch(
            "scarlett_os.common.configure.ruamel_config.logging.Logger.debug",
            name="mock_logger_debug",
        )

        ruamel_config.get_xdg_config_dir_path(override="SOME_FAKE_OVERRIDE")

        mock_logger_debug.assert_called_with(mock.ANY)


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
        to_flatten = {"a": 1, "c": {"a": 2, "b": {"x": 5, "y": 10}}, "d": [1, 2, 3]}

        expected_flattened = {"a": 1, "c_a": 2, "c_b_x": 5, "d": [1, 2, 3], "c_b_y": 10}

        flattened_result = ruamel_config.flatten(to_flatten)
        added, removed, modified, same = dict_compare(
            flattened_result, expected_flattened
        )

        # assert dicts are exactly the same, meaning modified is equal to empty
        # dict {}
        assert modified == {}

    def test_config_file_not_found(self):
        """test usecase when file not found."""

        base = tempfile.mkdtemp()
        config_file = os.path.join(base, "config.yaml")

        with pytest.raises(FileNotFoundError):
            temp_config = ruamel_config.load_config(config_file)

        shutil.rmtree(base)


@pytest.mark.ruamelconfigonly
@pytest.mark.scarlettonly
@pytest.mark.unittest
@pytest.mark.simpleconfigtest
@pytest.mark.scarlettonlyunittest
class TestConfigManager(object):

    """
    Tests for the scarlett_os.common.configure.ruamel_config.ConfigManager class.
    """

    def test_config_path_base(self):
        config_manager = ruamel_config.ConfigManager("/tmp/config.yaml")
        assert config_manager.config_path_base == "/tmp"

        base = tempfile.mkdtemp()
        config_file = os.path.join(base, "config.yaml")

        config_manager.config_path_base = base
        assert config_manager.config_path_base == base

        shutil.rmtree(base)

    def test_config_path_base_without_args_is_default_config_path(self):
        config_manager = ruamel_config.ConfigManager()
        assert config_manager.config_path_base == "/home/pi/.config/scarlett_os"

    def test_config_manager_env_override(self, monkeypatch):
        base = tempfile.mkdtemp()
        config_file = os.path.join(base, "config.yaml")

        with open(config_file, "wt") as f:
            f.write(COMMON_MOCKED_CONFIG)

        monkeypatch.setenv("SCARLETT_OS_CONFIG_LATITUDE", "300")
        monkeypatch.setenv("SCARLETT_OS_CONFIG_LONGITUDE", "200")
        monkeypatch.setenv(
            "SCARLETT_OS_CONFIG_POCKETSPHINX_HMM", "/tmp/model/en-us/en-us"
        )
        monkeypatch.setenv("SCARLETT_OS_CONFIG_POCKETSPHINX_LM", "/tmp/lm/1473.lm")
        monkeypatch.setenv("SCARLETT_OS_CONFIG_POCKETSPHINX_DICT", "/tmp/dict/1473.dic")
        monkeypatch.setenv("SCARLETT_OS_CONFIG_DEVICE", "plughw:CARD=Device,DEV=0")

        config_manager = ruamel_config.ConfigManager(config_file)
        config_manager.load()

        assert config_manager.cfg["latitude"] == "300"
        assert config_manager.cfg["longitude"] == "200"
        assert config_manager.cfg["pocketsphinx"]["hmm"] == "/tmp/model/en-us/en-us"
        assert config_manager.cfg["pocketsphinx"]["lm"] == "/tmp/lm/1473.lm"
        assert config_manager.cfg["pocketsphinx"]["dict"] == "/tmp/dict/1473.dic"
        assert (
            config_manager.cfg["pocketsphinx"]["device"] == "plughw:CARD=Device,DEV=0"
        )

        shutil.rmtree(base)
