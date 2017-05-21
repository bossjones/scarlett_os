"""Test the entity helper."""
# pylint: disable=protected-access,too-many-public-methods
from unittest.mock import MagicMock

import pytest

from scarlett_os.const import ATTR_HIDDEN
import scarlett_os.helpers.entity as entity
from tests.common import get_test_scarlett_os
