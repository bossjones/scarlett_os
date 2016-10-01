# -*- coding: utf-8 -*-

from __future__ import absolute_import
from .tools import package as ts_package
from .tools import verify as ts_verify

__author__ = 'Malcolm Jones'
__email__ = 'bossjones@theblacktonystark.com'
__version__ = '0.1.0'

# source: timeside
ts_verify.check_python3_installed()

# Check Availability of Gstreamer python bindings
ts_package.check_gi()

# Check Availability of sphinxbase, pocketsphinx, gst-plugins-espeak
# _WITH_SPHINXBASE = ts_package.check_sphinxbase()
# _WITH_POCKETSPHINX = ts_package.check_pocketsphinx()
# _WITH_GST_ESPEAK = ts_package.check_gst_espeak()

# __all__ = ['api', 'processor']

# ts_package.discover_modules('plugins', 'scarlett_os') #__name__)

# Clean-up
del ts_package
del absolute_import

# Import psutil
try:
    from psutil import __version__ as psutil_version
except ImportError:
    print('PSutil library not found. ScarlettOS cannot start.')
    sys.exit(1)


def main():
    """Main entry point for ScarlettOS.

    Select the mode (standalone, client or server)
    Run it...
    """

    # TODO: Grabe values from cli, setup correct logging.
    # TODO: For now we'll default to scarlett_os.logger

    import platform
    import scarlett_os.logger
    import logging
    logger = logging.getLogger('scarlettlogger')

    # Log ScarlettOS and PSutil version
    logger.info('Start ScarlettOS {}'.format(__version__))
    logger.info('{} {} and PSutil {} detected'.format(
        platform.python_implementation(),
        platform.python_version(),
        psutil_version))

    # Share global var
    global core, dbus_server, listener, tasker, check_all_services

    # Create the ScarlettOS main instance
    # source: Glances
    # core = ScarlettOSMain()
