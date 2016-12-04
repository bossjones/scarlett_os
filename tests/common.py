"""Test the helper method for writing tests."""
import os

import contextlib
import gc
import tempfile
import unittest
from unittest import mock

# from datetime import timedelta
from unittest.mock import patch
from io import StringIO
import logging
import threading
from contextlib import contextmanager

from scarlett_os.internal.gi import GLib, Gio, GObject, Gst

from scarlett_os import core as s, loader
from scarlett_os.utility.unit_system import METRIC_SYSTEM
import scarlett_os.utility.dt as date_utility
import scarlett_os.utility.yaml as yaml
from scarlett_os.const import (
    STATE_ON, STATE_OFF, DEVICE_DEFAULT_NAME, EVENT_TIME_CHANGED,
    EVENT_STATE_CHANGED, EVENT_PLATFORM_DISCOVERED, ATTR_SERVICE,
    ATTR_DISCOVERED, SERVER_PORT)
# from scarlett_os.automations import sun, mqtt

_TEST_INSTANCE_PORT = SERVER_PORT
logger = logging.getLogger(__name__)


def clean_scarlett_os_subprocess_mock(sub_p):
    sub_p.process = None
    sub_p.pid = None


def create_scarlett_os_subprocess_mock(sub_p):
    sub_p = mock.MagicMock()

    return sub_p


# def create_pitivi_mock(**settings):
#     app = mock.MagicMock()
#
#     app.write_action = mock.MagicMock(spec=Pitivi.write_action)
#     check.check_requirements()
#
#     app.settings = __create_settings(**settings)
#     app.proxy_manager = ProxyManager(app)
#
#     return app


def get_test_config_dir(*add_path):
    """Return a path to a test config dir."""
    return os.path.join(os.path.dirname(__file__), "testing_config", *add_path)


def get_test_scarlett_os(num_threads=None):
    """Return a ScarlettOS object pointing at test config dir."""
    # loop = asyncio.new_event_loop()
    loop = None

    if num_threads:
        orig_num_threads = s.MIN_WORKER_THREAD
        s.MIN_WORKER_THREAD = num_threads

    ss = s.ScarlettSystem()

    if num_threads:
        s.MIN_WORKER_THREAD = orig_num_threads

    orig_start = ss.start
    orig_stop = ss.stop

    def start_ss(*mocks):
        """Helper to start ss."""
        orig_start()
        # ss.block_till_done()

    def stop_ss():
        """Stop ss."""
        orig_stop()
        # stop_event.wait()

    ss.start = start_ss
    ss.stop = stop_ss

    return ss


# @asyncio.coroutine
def async_test_scarlett_os(loop):
    """Return a ScarlettOS object pointing at test config dir."""
    # loop._thread_ident = threading.get_ident()

    ss = s.ScarlettSystem(loop)

    ss.config.location_name = 'test scarlett'
    ss.config.config_dir = get_test_config_dir()
    ss.config.latitude = 32.87336
    ss.config.longitude = -117.22743
    ss.config.elevation = 0
    ss.config.time_zone = date_utility.get_time_zone('US/Pacific')
    ss.config.units = METRIC_SYSTEM
    ss.config.skip_pip = True

    # if 'custom_automations.test' not in loader.AVAILABLE_COMPONENTS:
    #     yield from loop.run_in_executor(None, loader.prepare, ss)

    ss.state = s.CoreState.running

    return ss


def load_fixture(filename):
    """Helper to load a fixture."""
    path = os.path.join(os.path.dirname(__file__), 'fixtures', filename)
    with open(path) as fptr:
        return fptr.read()


def patch_yaml_files(files_dict, endswith=True):
    """Patch load_yaml with a dictionary of yaml files."""
    # match using endswith, start search with longest string
    matchlist = sorted(list(files_dict.keys()), key=len) if endswith else []

    def mock_open_f(fname, **_):
        """Mock open() in the yaml module, used by load_yaml."""
        # Return the mocked file on full match
        if fname in files_dict:
            logger.debug('patch_yaml_files match %s', fname)
            res = StringIO(files_dict[fname])
            setattr(res, 'name', fname)
            return res

        # Match using endswith
        for ends in matchlist:
            if fname.endswith(ends):
                logger.debug('patch_yaml_files end match %s: %s', ends, fname)
                res = StringIO(files_dict[ends])
                setattr(res, 'name', fname)
                return res

        # Fallback for ss.automations (i.e. services.yaml)
        if 'scarlett_os/automations' in fname:
            logger.debug('patch_yaml_files using real file: %s', fname)
            return open(fname, encoding='utf-8')

        # Not found
        raise FileNotFoundError('File not found: {}'.format(fname))

    return patch.object(yaml, 'open', mock_open_f, create=True)
