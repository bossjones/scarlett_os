"""
This package contains automations that can be plugged into ScarlettOS.

Component design guidelines:
- Each component defines a constant DOMAIN that is equal to its filename.
- Each component that tracks states should create state entity names in the
  format "<DOMAIN>.<OBJECT_ID>".
- Each component should publish services only under its own domain.
"""
import itertools as it
import logging

import scarlett_os.core as s
# from scarlett_os.helpers.service import extract_entity_ids
# from scarlett_os.loader import get_component
from scarlett_os.const import (
    ATTR_ENTITY_ID, SERVICE_TURN_ON, SERVICE_TURN_OFF, SERVICE_TOGGLE)

logger = logging.getLogger(__name__)

SERVICE_RELOAD_CORE_CONFIG = 'reload_core_config'
