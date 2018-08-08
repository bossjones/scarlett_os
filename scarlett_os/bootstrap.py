"""Provide methods to bootstrap a Scarlett System instance."""
import logging
import os

# pylint: disable=unused-import
from collections import OrderedDict
from typing import Any, Optional, Dict

import voluptuous as vol

from scarlett_os.const import (
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_NAME,
    CONF_UNIT_SYSTEM,
    CONF_TIME_ZONE,
    CONF_CUSTOMIZE,
    CONF_ELEVATION,
    CONF_UNIT_SYSTEM_METRIC,
    CONF_UNIT_SYSTEM_IMPERIAL,
    CONF_TEMPERATURE_UNIT,
    TEMP_CELSIUS,
    __version__,
)

import scarlett_os.core as core
from scarlett_os.exceptions import ScarlettError
# from scarlett_os.utility.yaml import load_yaml
import scarlett_os.helpers.config_validation as cv
from scarlett_os.helpers.entity import set_customize
from scarlett_os.utility import dt as date_utility, location as loc_utility
from scarlett_os.utility.unit_system import IMPERIAL_SYSTEM, METRIC_SYSTEM


# pylint: disable=invalid-name
# pylint: disable=bad-whitespace

logger = logging.getLogger(__name__)

# NOTE: from home-assistant
# import asyncio
# import logging
# import logging.handlers
# import os
# import sys
# from time import time
# from collections import OrderedDict

# from typing import Any, Optional, Dict

# import voluptuous as vol

# import homeassistant.components as core_components
# from homeassistant.components import persistent_notification
# import homeassistant.config as conf_util
# import homeassistant.core as core
# from homeassistant.const import EVENT_HOMEASSISTANT_CLOSE
# from homeassistant.setup import async_setup_component
# import homeassistant.loader as loader
# from homeassistant.util.logging import AsyncHandler
# from homeassistant.util.yaml import clear_secret_cache
# from homeassistant.exceptions import HomeAssistantError
# from homeassistant.helpers.signal import async_register_signal_handling

# _LOGGER = logging.getLogger(__name__)

# ERROR_LOG_FILENAME = 'home-assistant.log'
# FIRST_INIT_COMPONENT = set((
#     'recorder', 'mqtt', 'mqtt_eventstream', 'logger', 'introduction',
#     'frontend', 'history'))

# create config object from dict

# create config from file


# create new scarlett system from config dict
def from_config_dict(
    config: Dict[str, Any],
    scarlett_system: Optional[core.ScarlettSystem] = None,
    config_dir: Optional[str] = None,
    enable_log: bool = True,
    verbose: bool = False,
    skip_pip: bool = False,
    log_rotate_days: Any = None,
) -> Optional[core.ScarlettSystem]:  # pragma: no cover
    """Try to configure ScarlettOS from a config dict.

    Dynamically loads required components and its dependencies.
    """
    if scarlett_system is None:
        scarlett_system = core.ScarlettSystem()
        if config_dir is not None:
            config_dir = os.path.abspath(config_dir)
            scarlett_system.config.config_dir = config_dir
            # mount_local_lib_path(config_dir)

    # TODO: Implement coroutine to load in config in async manner w/ GLib
    # TODO: For now, lets just take some of the parts we need
    # run task
    # scarlett_system = scarlett_system.loop.run_until_complete(
    #     async_from_config_dict(
    #         config, scarlett_system, config_dir, enable_log, verbose, skip_pip,
    #         log_rotate_days)
    # )

    # start = time()
    # core_config = config.get(core.DOMAIN, {})

    return scarlett_system


# Create new scarlett system object from config file
def from_config_file(
    config_path: str,
    scarlett_system: Optional[core.ScarlettSystem] = None,
    verbose: bool = False,
    skip_pip: bool = True,
    log_rotate_days: Any = None,
):  # pragma: no cover
    """Read the configuration file and try to start all the functionality.

    Will add functionality to 'scarlett_system' parameter if given,
    instantiates a new Home Assistant object if 'scarlett_system' is not given.
    """
    if scarlett_system is None:
        scarlett_system = core.ScarlettSystem()

    # run task
    # scarlett_system = scarlett_system.loop.run_until_complete(
    #     async_from_config_file(
    #         config_path, scarlett_system, verbose, skip_pip, log_rotate_days)
    # )

    return scarlett_system
