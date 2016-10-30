"""
Provides methods for loading ScarlettOS automations.

This module has quite some complex parts. I have tried to add as much
documentation as possible to keep it understandable.

Components are loaded by calling get_component('switch') from your code.
If you want to retrieve a platform that is part of a component, you should
call get_component('switch.your_platform'). In both cases the config directory
is checked to see if it contains a user provided version. If not available it
will check the built-in automations and platforms.
"""
import importlib
import logging
import os
import pkgutil
import sys

from types import ModuleType
# pylint: disable=unused-import
from typing import Optional, Sequence, Set, Dict  # NOQA

from scarlett_os.const import PLATFORM_FORMAT
from scarlett_os.utility import OrderedSet

# Typing imports
# pylint: disable=using-constant-test,unused-import
if False:
    from scarlett_os.core import ScarlettSystem  # NOQA

PREPARED = False

# List of available automations
AVAILABLE_COMPONENTS = []  # type: List[str]

# Dict of loaded automations mapped name => module
_COMPONENT_CACHE = {}  # type: Dict[str, ModuleType]

logger = logging.getLogger(__name__)


# def get_platform(domain: str, platform: str) -> Optional[ModuleType]:
#     """Try to load specified platform.
#
#     Async friendly.
#     """
#     return get_component(PLATFORM_FORMAT.format(domain, platform))
