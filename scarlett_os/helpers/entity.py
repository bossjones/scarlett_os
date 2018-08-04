"""An abstract class for entities."""
import logging

from typing import Any, Optional, List, Dict

from scarlett_os.const import (
    ATTR_ASSUMED_STATE,
    ATTR_FRIENDLY_NAME,
    ATTR_HIDDEN,
    ATTR_ICON,
    ATTR_UNIT_OF_MEASUREMENT,
    DEVICE_DEFAULT_NAME,
    STATE_OFF,
    STATE_ON,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
    ATTR_ENTITY_PICTURE,
)

# Entity attributes that we will overwrite
_OVERWRITE = {}  # type: Dict[str, Any]

logger = logging.getLogger(__name__)


def set_customize(customize: Dict[str, Any]) -> None:
    """Overwrite all current customize settings.

    Async friendly.
    """
    global _OVERWRITE

    _OVERWRITE = {key.lower(): val for key, val in customize.items()}
