#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# #####################################################
# # NOTE: THIS USE TO BE IN cli.py in ROOT folder
# #####################################################
# from __future__ import absolute_import, division, print_function
#
# # import logging
# import click
#
# from . import __version__
# #####################################################

"""Allow user to run ScarlettOS as a module."""

# Execute with:
# $ python -m scarlett_os

# import scarlett_os
# import scarlett_os.cli
#
#
# if __name__ == '__main__':
#     scarlett_os.cli.main()


# put this inside a bootstrap module
# 
# def enable_logging(hass: core.HomeAssistant, verbose: bool=False,
#                    log_rotate_days=None) -> None:
#     """Setup the logging.
#
#     Async friendly.
#     """
#     logging.basicConfig(level=logging.INFO)
#     fmt = ("%(log_color)s%(asctime)s %(levelname)s (%(threadName)s) "
#            "[%(name)s] %(message)s%(reset)s")
#
#     # suppress overly verbose logs from libraries that aren't helpful
#     logging.getLogger("requests").setLevel(logging.WARNING)
#     logging.getLogger("urllib3").setLevel(logging.WARNING)
#     logging.getLogger("aiohttp.access").setLevel(logging.WARNING)
#
#     try:
#         from colorlog import ColoredFormatter
#         logging.getLogger().handlers[0].setFormatter(ColoredFormatter(
#             fmt,
#             datefmt='%y-%m-%d %H:%M:%S',
#             reset=True,
#             log_colors={
#                 'DEBUG': 'cyan',
#                 'INFO': 'green',
#                 'WARNING': 'yellow',
#                 'ERROR': 'red',
#                 'CRITICAL': 'red',
#             }
#         ))
#     except ImportError:
#         pass
#
#     # Log errors to a file if we have write access to file or config dir
#     err_log_path = hass.config.path(ERROR_LOG_FILENAME)
#     err_path_exists = os.path.isfile(err_log_path)
#
#     # Check if we can write to the error log if it exists or that
#     # we can create files in the containing directory if not.
#     if (err_path_exists and os.access(err_log_path, os.W_OK)) or \
#        (not err_path_exists and os.access(hass.config.config_dir, os.W_OK)):
#
#         if log_rotate_days:
#             err_handler = logging.handlers.TimedRotatingFileHandler(
#                 err_log_path, when='midnight', backupCount=log_rotate_days)
#         else:
#             err_handler = logging.FileHandler(
#                 err_log_path, mode='w', delay=True)
#
#         err_handler.setLevel(logging.INFO if verbose else logging.WARNING)
#         err_handler.setFormatter(
#             logging.Formatter('%(asctime)s %(name)s: %(message)s',
#                               datefmt='%y-%m-%d %H:%M:%S'))
#         logger = logging.getLogger('')
#         logger.addHandler(err_handler)
#         logger.setLevel(logging.INFO)
#
#     else:
#         _LOGGER.error(
#             'Unable to setup error log %s (access denied)', err_log_path)
#
#
# def log_exception(ex, domain, config, hass):
#     """Generate log exception for config validation."""
#     run_callback_threadsafe(
#         hass.loop, async_log_exception, ex, domain, config, hass).result()
