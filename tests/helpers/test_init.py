"""Test component helpers."""
# pylint: disable=protected-access,too-many-public-methods
from collections import OrderedDict
import unittest

from scarlett_os import helpers

from tests.common import get_test_scarlett_os

# FIXME: Turn this into pytest
# FIXME: Make sure we need to use this guy at the moment, otherwise, exclude it for now
# FIXME: 5/10/2017
class TestHelpers(unittest.TestCase):
    """Tests scarlett_os.helpers module."""

    def setUp(self):  # pylint: disable=invalid-name
        """Init needed objects."""
        self.ss = get_test_scarlett_os()

    def tearDown(self):  # pylint: disable=invalid-name
        """Stop everything that was started."""
        self.ss.stop()

    def test_extract_domain_configs(self):
        """Test the extraction of domain configuration."""
        config = {
            'zone': None,
            'zoner': None,
            'zone ': None,
            'zone Hallo': None,
            'zone 100': None,
        }

        self.assertEqual(set(['zone', 'zone Hallo', 'zone 100']),
                         set(helpers.extract_domain_configs(config, 'zone')))

    def test_config_per_platform(self):
        """Test config per platform method."""
        config = OrderedDict([
            ('zone', {'platform': 'hello'}),
            ('zoner', None),
            ('zone Hallo', [1, {'platform': 'hello 2'}]),
            ('zone 100', None),
        ])

        assert [
            ('hello', config['zone']),
            (None, 1),
            ('hello 2', config['zone Hallo'][1]),
        ] == list(helpers.config_per_platform(config, 'zone'))
