"""
Core component of ScarlettOS.

ScarlettOS is a Home Automation framework for observing the state
of entities and react to changes.
"""
# pylint: disable=unused-import, too-many-lines
# from concurrent.futures import ThreadPoolExecutor
import enum
import logging
import os
import re
import signal
import sys
import threading
import time

from types import MappingProxyType
from typing import Optional, Any, Callable, List  # noqa

import voluptuous as vol
from voluptuous.humanize import humanize_error

from scarlett_os.const import (
    ATTR_DOMAIN,
    ATTR_FRIENDLY_NAME,
    ATTR_NOW,
    ATTR_SERVICE,
    ATTR_SERVICE_CALL_ID,
    ATTR_SERVICE_DATA,
    EVENT_CALL_SERVICE,
    EVENT_SCARLETT_OS_START,
    EVENT_SCARLETT_OS_STOP,
    EVENT_SERVICE_EXECUTED,
    EVENT_SERVICE_REGISTERED,
    EVENT_STATE_CHANGED,
    EVENT_TIME_CHANGED,
    MATCH_ALL,
    RESTART_EXIT_CODE,
    SERVICE_SCARLETT_OS_RESTART,
    SERVICE_SCARLETT_OS_STOP,
    __version__,
)
from scarlett_os.exceptions import ScarlettError, InvalidEntityFormatError
import scarlett_os.utility as utility
import scarlett_os.utility.dt as dt_utility
import scarlett_os.utility.location as location
from scarlett_os.utility.unit_system import UnitSystem, METRIC_SYSTEM  # noqa

DOMAIN = "scarlett_os"

# How often time_changed event should fire
TIMER_INTERVAL = 1  # seconds

# How long we wait for the result of a service call
SERVICE_CALL_LIMIT = 10  # seconds

# Define number of MINIMUM worker threads.
# During bootstrap of HA (see bootstrap._setup_component()) worker threads
# will be added for each component that polls devices.
MIN_WORKER_THREAD = 2

# Pattern for validating entity IDs (format: <domain>.<entity>)
ENTITY_ID_PATTERN = re.compile(r"^(\w+)\.(\w+)$")

# Interval at which we check if the pool is getting busy
MONITOR_POOL_INTERVAL = 30

logger = logging.getLogger(__name__)


def split_entity_id(entity_id):
    """Split a state entity_id into domain, object_id."""
    return entity_id.split(".", 1)


def valid_entity_id(entity_id):
    """Test if an entity ID is a valid format."""
    return ENTITY_ID_PATTERN.match(entity_id) is not None


class CoreState(enum.Enum):
    """Represent the current state of ScarlettOS."""

    not_running = "NOT_RUNNING"
    starting = "STARTING"
    running = "RUNNING"
    stopping = "STOPPING"

    def __str__(self):
        """Return the event."""
        return self.value


class ScarlettSystem(object):
    """Root object of the ScarlettOS home automation."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self, loop=None):
        """Initialize new ScarlettOS object."""
        # self.loop = loop or asyncio.get_event_loop()
        # self.executor = ThreadPoolExecutor(max_workers=5)
        # self.loop.set_default_executor(self.executor)
        # self.loop.set_exception_handler(self._async_exception_handler)
        # self.pool = create_worker_pool()
        # self.bus = EventBus(self)
        # self.services = ServiceRegistry(self.bus, self.add_job, self.loop)
        # self.states = StateMachine(self.bus, self.loop)
        # self.config = Config()  # type: Config
        self.state = CoreState.not_running
        # self.exit_code = None
        # self._websession = None

    @property
    def is_running(self):
        """Return if ScarlettOS is running."""
        return self.state in (CoreState.starting, CoreState.running)

    def start(self):
        """Start Scarlett System."""
        logger.info("Starting ScarlettOS core loop")

    def stop(self):
        """Stop ScarlettOS and shuts down all threads."""
        # run_coroutine_threadsafe(self.async_stop(), self.loop)
        logger.info("Stop ScarlettOS core loop")


# class Config(object):
#     """Configuration settings for ScarlettOS."""

#     # pylint: disable=too-many-instance-attributes
#     def __init__(self):
#         """Initialize a new config object."""
#         self.latitude = None  # type: Optional[float]
#         self.longitude = None  # type: Optional[float]
#         self.elevation = None  # type: Optional[int]
#         self.location_name = None  # type: Optional[str]
#         self.time_zone = None  # type: Optional[str]
#         self.units = METRIC_SYSTEM  # type: UnitSystem

#         # If True, pip install is skipped for requirements on startup
#         self.skip_pip = False  # type: bool

#         # List of loaded automations
#         self.automations = []

#         # Remote.API object pointing at local API
#         self.api = None

#         # Directory that holds the configuration
#         self.config_dir = None

#     def distance(self: object, lat: float, lon: float) -> float:
#         """Calculate distance from ScarlettOS.

#         Async friendly.
#         """
#         return self.units.length(
#             location.distance(self.latitude, self.longitude, lat, lon), 'm')

#     def path(self, *path):
#         """Generate path to the file within the config dir.

#         Async friendly.
#         """
#         if self.config_dir is None:
#             raise ScarlettError("config_dir is not set")
#         return os.path.join(self.config_dir, *path)

#     def as_dict(self):
#         """Create a dict representation of this dict.

#         Async friendly.
#         """
#         time_zone = self.time_zone or dt_utility.UTC

#         return {
#             'latitude': self.latitude,
#             'longitude': self.longitude,
#             'unit_system': self.units.as_dict(),
#             'location_name': self.location_name,
#             'time_zone': time_zone.zone,
#             'automations': self.automations,
#             'config_dir': self.config_dir,
#             'version': __version__
#         }
