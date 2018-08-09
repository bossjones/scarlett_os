"""Module to help with parsing and generating configuration files."""
import logging
import os
import shutil

# NOTE: Eventually, we want to just delete this whole file.
from types import MappingProxyType

# pylint: disable=unused-import
from typing import Any, Tuple  # noqa

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
from scarlett_os.core import valid_entity_id
from scarlett_os.exceptions import ScarlettError

# from scarlett_os.utility.yaml import load_yaml
import scarlett_os.helpers.config_validation as cv
from scarlett_os.helpers.entity import set_customize
from scarlett_os.utility import dt as date_utility, location as loc_utility
from scarlett_os.utility.unit_system import IMPERIAL_SYSTEM, METRIC_SYSTEM

logger = logging.getLogger(__name__)

YAML_CONFIG_FILE = "configuration.yaml"
VERSION_FILE = ".SC_OS_VERSION"
CONFIG_DIR_NAME = ".scarlett_os"

# NOTE: YAGNI 8/5/2018
# DEFAULT_CORE_CONFIG = (
#     # Tuples (attribute, default, auto detect property, description)
#     (CONF_NAME, "Home", None, "Name of the location where ScarlettOS is " "running"),
#     (
#         CONF_LATITUDE,
#         0,
#         "latitude",
#         "Location required to calculate the time" " the sun rises and sets",
#     ),
#     (CONF_LONGITUDE, 0, "longitude", None),
#     (
#         CONF_ELEVATION,
#         0,
#         None,
#         "Impacts weather/sunrise data" " (altitude above sea level in meters)",
#     ),
#     (
#         CONF_UNIT_SYSTEM,
#         CONF_UNIT_SYSTEM_METRIC,
#         None,
#         "{} for Metric, {} for Imperial".format(
#             CONF_UNIT_SYSTEM_METRIC, CONF_UNIT_SYSTEM_IMPERIAL
#         ),
#     ),
#     (
#         CONF_TIME_ZONE,
#         "UTC",
#         "time_zone",
#         "Pick yours from here: http://en.wiki"
#         "pedia.org/wiki/List_of_tz_database_time_zones",
#     ),
# )  # type: Tuple[Tuple[str, Any, Any, str], ...]
# DEFAULT_CONFIG = """
# # Show links to resources in log and frontend
# introduction:

# # Enables the frontend
# frontend:

# http:
#   # Uncomment this to add a password (recommended!)
#   # api_password: PASSWORD

# # Checks for available updates
# updater:

# # Discover some devices automatically
# discovery:

# # Allows you to issue voice commands from the frontend in enabled browsers
# conversation:

# # Enables support for tracking state changes over time.
# history:

# # View all events in a logbook
# logbook:

# # Track the sun
# sun:

# # Weather Prediction
# sensor:
#   platform: yr
# """

# NOTE: YAGNI 8/5/2018
# def _valid_customize(value):
#     """Config validator for customize."""
#     if not isinstance(value, dict):
#         raise vol.Invalid("Expected dictionary")

#     for key, val in value.items():
#         if not valid_entity_id(key):
#             raise vol.Invalid("Invalid entity ID: {}".format(key))

#         if not isinstance(val, dict):
#             raise vol.Invalid("Value of {} is not a dictionary".format(key))

#     return value

# NOTE: YAGNI 8/5/2018
# CORE_CONFIG_SCHEMA = vol.Schema(
#     {
#         CONF_NAME: vol.Coerce(str),
#         CONF_LATITUDE: cv.latitude,
#         CONF_LONGITUDE: cv.longitude,
#         CONF_ELEVATION: vol.Coerce(int),
#         vol.Optional(CONF_TEMPERATURE_UNIT): cv.temperature_unit,
#         CONF_UNIT_SYSTEM: cv.unit_system,
#         CONF_TIME_ZONE: cv.time_zone,
#         vol.Required(CONF_CUSTOMIZE, default=MappingProxyType({})): _valid_customize,
#     }
# )

# NOTE: YAGNI 8/5/2018
# def get_default_config_dir() -> str:
#     """Put together the default configuration directory based on OS."""
#     data_dir = os.getenv("APPDATA") if os.name == "nt" else os.path.expanduser("~")
#     return os.path.join(data_dir, CONFIG_DIR_NAME)

# NOTE: YAGNI 8/5/2018
# def ensure_config_exists(config_dir: str, detect_location: bool = True) -> str:
#     """Ensure a config file exists in given configuration directory.

#     Creating a default one if needed.
#     Return path to the config file.
#     """
#     config_path = find_config_file(config_dir)

#     if config_path is None:
#         print("Unable to find configuration. Creating default one in", config_dir)
#         config_path = create_default_config(config_dir, detect_location)

#     return config_path

# NOTE: YAGNI 8/5/2018
# def create_default_config(config_dir, detect_location=True):
#     """Create a default configuration file in given configuration directory.

#     Return path to new config file if success, None if failed.
#     This method needs to run in an executor.
#     """
#     config_path = os.path.join(config_dir, YAML_CONFIG_FILE)
#     version_path = os.path.join(config_dir, VERSION_FILE)

#     info = {attr: default for attr, default, _, _ in DEFAULT_CORE_CONFIG}

#     location_info = detect_location and loc_utility.detect_location_info()

#     if location_info:
#         if location_info.use_metric:
#             info[CONF_UNIT_SYSTEM] = CONF_UNIT_SYSTEM_METRIC
#         else:
#             info[CONF_UNIT_SYSTEM] = CONF_UNIT_SYSTEM_IMPERIAL

#         for attr, default, prop, _ in DEFAULT_CORE_CONFIG:
#             if prop is None:
#                 continue
#             info[attr] = getattr(location_info, prop) or default

#         if location_info.latitude and location_info.longitude:
#             info[CONF_ELEVATION] = loc_utility.elevation(
#                 location_info.latitude, location_info.longitude
#             )

#     # Writing files with YAML does not create the most human readable results
#     # So we're hard coding a YAML template.
#     try:
#         with open(config_path, "w") as config_file:
#             config_file.write("scarlett_os:\n")

#             for attr, _, _, description in DEFAULT_CORE_CONFIG:
#                 if info[attr] is None:
#                     continue
#                 elif description:
#                     config_file.write("  # {}\n".format(description))
#                 config_file.write("  {}: {}\n".format(attr, info[attr]))

#             config_file.write(DEFAULT_CONFIG)

#         with open(version_path, "wt") as version_file:
#             version_file.write(__version__)

#         return config_path

#     except IOError:
#         print("Unable to create default configuration file", config_path)
#         return None

# NOTE: YAGNI 8/5/2018
# def find_config_file(config_dir):
#     """Look in given directory for supported configuration files.

#     Async friendly.
#     """
#     config_path = os.path.join(config_dir, YAML_CONFIG_FILE)

#     return config_path if os.path.isfile(config_path) else None

# NOTE: YAGNI 8/5/2018
# def load_yaml_config_file(config_path):
#     """Parse a YAML configuration file.

#     This method needs to run in an executor.
#     """
#     conf_dict = load_yaml(config_path)

#     if not isinstance(conf_dict, dict):
#         msg = "The configuration file {} does not contain a dictionary".format(
#             os.path.basename(config_path)
#         )
#         logger.error(msg)
#         raise ScarlettError(msg)

#     return conf_dict

# NOTE: YAGNI 8/5/2018
# def process_ha_config_upgrade(ss):
#     """Upgrade config if necessary.

#     This method needs to run in an executor.
#     """
#     version_path = ss.config.path(VERSION_FILE)

#     try:
#         with open(version_path, "rt") as inp:
#             conf_version = inp.readline().strip()
#     except FileNotFoundError:
#         # Last version to not have this file
#         conf_version = "0.7.7"

#     if conf_version == __version__:
#         return

#     logger.info("Upgrading config directory from %s to %s", conf_version, __version__)

#     lib_path = ss.config.path("deps")
#     if os.path.isdir(lib_path):
#         shutil.rmtree(lib_path)

#     with open(version_path, "wt") as outp:
#         outp.write(__version__)
