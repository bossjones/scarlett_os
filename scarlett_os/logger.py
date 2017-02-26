# -*- coding: utf-8 -*-
"""Setup logging."""

from __future__ import absolute_import, unicode_literals

import logging
import logging.config
import logging.handlers

# console_format = "%(asctime)s %(name)-12s (%(threadName)-9s) %(log_color)s%(levelname)-8s%(reset)s (%(funcName)-5s) %(message_log_color)s%(message)s"


def setup_logger():
    from colorlog import ColoredFormatter
    from gettext import gettext as _  # noqa

    try:
        """Return a logging obj with a default ColoredFormatter."""
        formatter = ColoredFormatter(
            "%(asctime)s %(name)-12s (%(threadName)-9s) %(log_color)s%(levelname)-8s%(reset)s (%(funcName)-5s) %(message_log_color)s%(message)s",  # noqa
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
                'TRACE': 'purple'
            },
            secondary_log_colors={
                'message': {
                    'ERROR': 'red',
                    'CRITICAL': 'red',
                    'DEBUG': 'yellow',
                    'INFO': 'yellow,bg_blue'
                }
            },
            style='%'
        )

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logging.getLogger('').addHandler(handler)
        logging.root.setLevel(logging.DEBUG)
    except ImportError:
        # No color available, use default config
        logging.basicConfig(format='%(levelname)s: %(message)s')
        logging.warn("Disabling color, you really want to install colorlog.")
