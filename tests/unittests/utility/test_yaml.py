"""Test ScarlettOS yaml loader."""
import io
import os
import unittest
from unittest.mock import patch

from scarlett_os.config import YAML_CONFIG_FILE, load_yaml_config_file
from scarlett_os.exceptions import ScarlettError
from scarlett_os.utility import yaml
from tests.common import get_test_config_dir, patch_yaml_files


# FIXME: Convert to pytest
# FIXME: 5/10/2017
class TestYaml(unittest.TestCase):
    """Test utility.yaml loader."""
    # pylint: disable=no-self-use,invalid-name

    def test_simple_list(self):
        """Test simple list."""
        conf = "config:\n  - simple\n  - list"
        with io.StringIO(conf) as file:
            doc = yaml.yaml.safe_load(file)
        assert doc['config'] == ["simple", "list"]

    def test_simple_dict(self):
        """Test simple dict."""
        conf = "key: value"
        with io.StringIO(conf) as file:
            doc = yaml.yaml.safe_load(file)
        assert doc['key'] == 'value'

    def test_duplicate_key(self):
        """Test duplicate dict keys."""
        files = {YAML_CONFIG_FILE: 'key: thing1\nkey: thing2'}
        with self.assertRaises(ScarlettError):
            with patch_yaml_files(files):
                load_yaml_config_file(YAML_CONFIG_FILE)

    def test_unhashable_key(self):
        """Test an unhasable key."""
        files = {YAML_CONFIG_FILE: 'message:\n  {{ states.state }}'}
        with self.assertRaises(ScarlettError), \
                patch_yaml_files(files):
            load_yaml_config_file(YAML_CONFIG_FILE)

    def test_no_key(self):
        """Test item without an key."""
        files = {YAML_CONFIG_FILE: 'a: a\nnokeyhere'}
        with self.assertRaises(ScarlettError), \
                patch_yaml_files(files):
            yaml.load_yaml(YAML_CONFIG_FILE)

    def test_enviroment_variable(self):
        """Test config file with enviroment variable."""
        os.environ["PASSWORD"] = "secret_password"
        conf = "password: !env_var PASSWORD"
        with io.StringIO(conf) as file:
            doc = yaml.yaml.safe_load(file)
        assert doc['password'] == "secret_password"
        del os.environ["PASSWORD"]

    def test_invalid_enviroment_variable(self):
        """Test config file with no enviroment variable sat."""
        conf = "password: !env_var PASSWORD"
        with self.assertRaises(ScarlettError):
            with io.StringIO(conf) as file:
                yaml.yaml.safe_load(file)

    def test_include_yaml(self):
        """Test include yaml."""
        with patch_yaml_files({'test.yaml': 'value'}):
            conf = 'key: !include test.yaml'
            with io.StringIO(conf) as file:
                doc = yaml.yaml.safe_load(file)
                assert doc["key"] == "value"

    @patch('scarlett_os.utility.yaml.os.walk')
    def test_include_dir_list(self, mock_walk):
        """Test include dir list yaml."""
        mock_walk.return_value = [
            ['/tmp', [], ['one.yaml', 'two.yaml']],
        ]

        with patch_yaml_files({
            '/tmp/one.yaml': 'one',
            '/tmp/two.yaml': 'two',
        }):
            conf = "key: !include_dir_list /tmp"
            with io.StringIO(conf) as file:
                doc = yaml.yaml.safe_load(file)
                assert sorted(doc["key"]) == sorted(["one", "two"])

    @patch('scarlett_os.utility.yaml.os.walk')
    def test_include_dir_list_recursive(self, mock_walk):
        """Test include dir recursive list yaml."""
        mock_walk.return_value = [
            ['/tmp', ['tmp2', '.ignore', 'ignore'], ['zero.yaml']],
            ['/tmp/tmp2', [], ['one.yaml', 'two.yaml']],
            ['/tmp/ignore', [], ['.ignore.yaml']]
        ]

        with patch_yaml_files({
            '/tmp/zero.yaml': 'zero',
            '/tmp/tmp2/one.yaml': 'one',
            '/tmp/tmp2/two.yaml': 'two'
        }):
            conf = "key: !include_dir_list /tmp"
            with io.StringIO(conf) as file:
                assert '.ignore' in mock_walk.return_value[0][1], \
                    "Expecting .ignore in here"
                doc = yaml.yaml.safe_load(file)
                assert 'tmp2' in mock_walk.return_value[0][1]
                assert '.ignore' not in mock_walk.return_value[0][1]
                assert sorted(doc["key"]) == sorted(["zero", "one", "two"])

    @patch('scarlett_os.utility.yaml.os.walk')
    def test_include_dir_named(self, mock_walk):
        """Test include dir named yaml."""
        mock_walk.return_value = [
            ['/tmp', [], ['first.yaml', 'second.yaml']]
        ]

        with patch_yaml_files({
            '/tmp/first.yaml': 'one',
            '/tmp/second.yaml': 'two'
        }):
            conf = "key: !include_dir_named /tmp"
            correct = {'first': 'one', 'second': 'two'}
            with io.StringIO(conf) as file:
                doc = yaml.yaml.safe_load(file)
                assert doc["key"] == correct

    @patch('scarlett_os.utility.yaml.os.walk')
    def test_include_dir_named_recursive(self, mock_walk):
        """Test include dir named yaml."""
        mock_walk.return_value = [
            ['/tmp', ['tmp2', '.ignore', 'ignore'], ['first.yaml']],
            ['/tmp/tmp2', [], ['second.yaml', 'third.yaml']],
            ['/tmp/ignore', [], ['.ignore.yaml']]
        ]

        with patch_yaml_files({
            '/tmp/first.yaml': 'one',
            '/tmp/tmp2/second.yaml': 'two',
            '/tmp/tmp2/third.yaml': 'three'
        }):
            conf = "key: !include_dir_named /tmp"
            correct = {'first': 'one', 'second': 'two', 'third': 'three'}
            with io.StringIO(conf) as file:
                assert '.ignore' in mock_walk.return_value[0][1], \
                    "Expecting .ignore in here"
                doc = yaml.yaml.safe_load(file)
                assert 'tmp2' in mock_walk.return_value[0][1]
                assert '.ignore' not in mock_walk.return_value[0][1]
                assert doc["key"] == correct

    @patch('scarlett_os.utility.yaml.os.walk')
    def test_include_dir_merge_list(self, mock_walk):
        """Test include dir merge list yaml."""
        mock_walk.return_value = [['/tmp', [], ['first.yaml', 'second.yaml']]]

        with patch_yaml_files({
            '/tmp/first.yaml': '- one',
            '/tmp/second.yaml': '- two\n- three'
        }):
            conf = "key: !include_dir_merge_list /tmp"
            with io.StringIO(conf) as file:
                doc = yaml.yaml.safe_load(file)
                assert sorted(doc["key"]) == sorted(["one", "two", "three"])

    @patch('scarlett_os.utility.yaml.os.walk')
    def test_include_dir_merge_list_recursive(self, mock_walk):
        """Test include dir merge list yaml."""
        mock_walk.return_value = [
            ['/tmp', ['tmp2', '.ignore', 'ignore'], ['first.yaml']],
            ['/tmp/tmp2', [], ['second.yaml', 'third.yaml']],
            ['/tmp/ignore', [], ['.ignore.yaml']]
        ]

        with patch_yaml_files({
            '/tmp/first.yaml': '- one',
            '/tmp/tmp2/second.yaml': '- two',
            '/tmp/tmp2/third.yaml': '- three\n- four'
        }):
            conf = "key: !include_dir_merge_list /tmp"
            with io.StringIO(conf) as file:
                assert '.ignore' in mock_walk.return_value[0][1], \
                    "Expecting .ignore in here"
                doc = yaml.yaml.safe_load(file)
                assert 'tmp2' in mock_walk.return_value[0][1]
                assert '.ignore' not in mock_walk.return_value[0][1]
                assert sorted(doc["key"]) == sorted(["one", "two",
                                                     "three", "four"])

    @patch('scarlett_os.utility.yaml.os.walk')
    def test_include_dir_merge_named(self, mock_walk):
        """Test include dir merge named yaml."""
        mock_walk.return_value = [['/tmp', [], ['first.yaml', 'second.yaml']]]

        with patch_yaml_files({
                '/tmp/first.yaml': 'key1: one',
                '/tmp/second.yaml': 'key2: two\nkey3: three'
        }):
            conf = "key: !include_dir_merge_named /tmp"
            with io.StringIO(conf) as file:
                doc = yaml.yaml.safe_load(file)
                assert doc["key"] == {
                    "key1": "one",
                    "key2": "two",
                    "key3": "three"
                }

    @patch('scarlett_os.utility.yaml.os.walk')
    def test_include_dir_merge_named_recursive(self, mock_walk):
        """Test include dir merge named yaml."""
        mock_walk.return_value = [
            ['/tmp', ['tmp2', '.ignore', 'ignore'], ['first.yaml']],
            ['/tmp/tmp2', [], ['second.yaml', 'third.yaml']],
            ['/tmp/ignore', [], ['.ignore.yaml']]
        ]

        with patch_yaml_files({
            '/tmp/first.yaml': 'key1: one',
            '/tmp/tmp2/second.yaml': 'key2: two',
            '/tmp/tmp2/third.yaml': 'key3: three\nkey4: four'
        }):
            conf = "key: !include_dir_merge_named /tmp"
            with io.StringIO(conf) as file:
                assert '.ignore' in mock_walk.return_value[0][1], \
                    "Expecting .ignore in here"
                doc = yaml.yaml.safe_load(file)
                assert 'tmp2' in mock_walk.return_value[0][1]
                assert '.ignore' not in mock_walk.return_value[0][1]
                assert doc["key"] == {
                    "key1": "one",
                    "key2": "two",
                    "key3": "three",
                    "key4": "four"
                }

    @patch('scarlett_os.utility.yaml.open', create=True)
    def test_load_yaml_encoding_error(self, mock_open):
        """Test raising a UnicodeDecodeError."""
        mock_open.side_effect = UnicodeDecodeError('', b'', 1, 0, '')
        self.assertRaises(ScarlettError, yaml.load_yaml, 'test')


FILES = {}


def load_yaml(fname, string):
    """Write a string to file and return the parsed yaml."""
    FILES[fname] = string
    with patch_yaml_files(FILES):
        return load_yaml_config_file(fname)


class FakeKeyring():  # pylint: disable=too-few-public-methods
    """Fake a keyring class."""

    def __init__(self, secrets_dict):
        """Store keyring dictionary."""
        self._secrets = secrets_dict

    # pylint: disable=protected-access
    def get_password(self, domain, name):
        """Retrieve password."""
        assert domain == yaml._SECRET_NAMESPACE
        return self._secrets.get(name)
