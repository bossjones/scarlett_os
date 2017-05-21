"""Test component helpers."""
import imp
import unittest
import unittest.mock as mock
# pylint: disable=protected-access,too-many-public-methods
from collections import OrderedDict

import pytest

from scarlett_os import helpers
from tests.common import get_test_scarlett_os


@pytest.fixture(scope='function')
def get_ss():
    ss = get_test_scarlett_os()
    yield ss
    ss.stop()


class TestHelpers(object):
    """Tests scarlett_os.helpers module."""

    def test_extract_domain_configs(self, get_ss):
        """Test the extraction of domain configuration."""
        config = {
            'zone': None,
            'zoner': None,
            'zone ': None,
            'zone Hallo': None,
            'zone 100': None,
        }

        assert set(['zone', 'zone Hallo', 'zone 100']) == \
                         set(helpers.extract_domain_configs(config, 'zone'))

    def test_config_per_platform(self, get_ss):
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
