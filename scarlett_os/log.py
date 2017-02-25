# -*- coding: utf-8 -*-
"""Scarlett log module. Some code borrowed from Mopidy."""

# pragma: no cover

import logging
import logging.config
import logging.handlers
import platform

from scarlett_os.compat import iteritems
from scarlett_os.compat import listitems


LOG_LEVELS = {
    -1: dict(root=logging.ERROR, scarlett_os=logging.WARNING),
    0: dict(root=logging.ERROR, scarlett_os=logging.INFO),
    1: dict(root=logging.WARNING, scarlett_os=logging.DEBUG),
    2: dict(root=logging.INFO, scarlett_os=logging.DEBUG),
    3: dict(root=logging.DEBUG, scarlett_os=logging.DEBUG),
    4: dict(root=logging.NOTSET, scarlett_os=logging.NOTSET),
}

# Custom log level which has even lower priority than DEBUG
TRACE_LOG_LEVEL = 5
logging.addLevelName(TRACE_LOG_LEVEL, 'TRACE')

logger = logging.getLogger(__name__)

# [logging]
# color = true
# console_format = %(levelname)-8s %(message)s
# debug_format = %(levelname)-8s %(asctime)s [%(process)d:%(threadName)s] %(name)s\n  %(message)s
# debug_file = mopidy.log
# config_file =


class DelayedHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)
        self._released = False
        self._buffer = []

    def handle(self, record):
        if not self._released:
            self._buffer.append(record)

    def release(self):
        self._released = True
        root = logging.getLogger('')
        while self._buffer:
            root.handle(self._buffer.pop(0))


_delayed_handler = DelayedHandler()


def bootstrap_delayed_logging():
    root = logging.getLogger('')
    root.setLevel(logging.NOTSET)
    root.addHandler(_delayed_handler)


def setup_logging(verbosity_level, save_debug_log):

    logging.captureWarnings(True)

    # if config['logging']['config_file']:
    #     # Logging config from file must be read before other handlers are
    #     # added. If not, the other handlers will have no effect.
    #     try:
    #         path = config['logging']['config_file']
    #         logging.config.fileConfig(path, disable_existing_loggers=False)
    #     except Exception as e:
    #         # Catch everything as logging does not specify what can go wrong.
    #         logger.error('Loading logging config %r failed. %s', path, e)

    setup_console_logging(verbosity_level)
    if save_debug_log:
        print('Here we would call setup_debug_logging_to_file(config)')
        # setup_debug_logging_to_file(config)

    _delayed_handler.release()


def setup_console_logging(verbosity_level):
    if verbosity_level < min(LOG_LEVELS.keys()):
        verbosity_level = min(LOG_LEVELS.keys())
    if verbosity_level > max(LOG_LEVELS.keys()):
        verbosity_level = max(LOG_LEVELS.keys())

    # loglevels = config.get('loglevels', {})
    loglevels = {}
    has_debug_loglevels = any([
        level < logging.INFO for level in loglevels.values()])

    verbosity_filter = VerbosityFilter(verbosity_level, loglevels)

    if verbosity_level < 1 and not has_debug_loglevels:
        log_format = "%(levelname)-8s %(message)s"
    else:
        # log_format = "(%(threadName)-9s) %(log_color)s%(levelname)-8s%(reset)s (%(funcName)-5s) %(message_log_color)s%(message)s"
        log_format = "%(levelname)-8s %(asctime)s [%(process)d:%(threadName)s] %(name)s\n  %(message)s"
        # source: Logging Cookbook — Python 3.6.0 documentation
        # log_format = "%(asctime)-15s %(name)-5s %(levelname)-8s IP: %(ip)-15s User: %(user)-8s %(message)s"
    formatter = logging.Formatter(log_format)

    # if config['logging']['color']:
    #     handler = ColorizingStreamHandler({})
    # else:
    #     handler = logging.StreamHandler()
    handler = ColorizingStreamHandler({})
    handler.addFilter(verbosity_filter)
    handler.setFormatter(formatter)

    logging.getLogger('').addHandler(handler)


# def setup_debug_logging_to_file(config):
#     formatter = logging.Formatter(config['logging']['debug_format'])
#     handler = logging.handlers.RotatingFileHandler(
#         config['logging']['debug_file'], maxBytes=10485760, backupCount=3)
#     handler.setFormatter(formatter)
#
#     logging.getLogger('').addHandler(handler)


class VerbosityFilter(logging.Filter):

    def __init__(self, verbosity_level, loglevels):
        self.verbosity_level = verbosity_level
        self.loglevels = loglevels

    def filter(self, record):
        for name, required_log_level in listitems(self.loglevels):
            if record.name == name or record.name.startswith(name + '.'):
                return record.levelno >= required_log_level

        if record.name.startswith('scarlett_os'):
            required_log_level = LOG_LEVELS[self.verbosity_level]['scarlett_os']
        else:
            required_log_level = LOG_LEVELS[self.verbosity_level]['root']
        return record.levelno >= required_log_level


#: Available log colors.
COLORS = [b'black', b'red', b'green', b'yellow', b'blue', b'magenta', b'cyan',
          b'white']


class ColorizingStreamHandler(logging.StreamHandler):  # noqa

    """
    Stream handler which colorizes the log using ANSI escape sequences.

    Does nothing on Windows, which doesn't support ANSI escape sequences.

    This implementation is based upon https://gist.github.com/vsajip/758430,
    which is:

        Copyright (C) 2010-2012 Vinay Sajip. All rights reserved.
        Licensed under the new BSD license.
    """

    # Map logging levels to (background, foreground, bold/intense)
    level_map = {
        TRACE_LOG_LEVEL: (None, 'blue', False),
        logging.DEBUG: (None, 'blue', False),
        logging.INFO: (None, 'white', False),
        logging.WARNING: (None, 'yellow', False),
        logging.ERROR: (None, 'red', False),
        logging.CRITICAL: ('red', 'white', True),
    }
    # Map logger name to foreground colors
    logger_map = {}

    csi = '\x1b['
    reset = '\x1b[0m'

    is_windows = platform.system() == 'Windows'

    def __init__(self, logger_colors):
        super(ColorizingStreamHandler, self).__init__()
        self.logger_map = logger_colors

    @property
    def is_tty(self):
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty()

    def emit(self, record):
        try:
            message = self.format(record)
            self.stream.write(message)
            self.stream.write(getattr(self, 'terminator', '\n'))
            self.flush()
        except Exception:
            self.handleError(record)

    def format(self, record):
        message = logging.StreamHandler.format(self, record)
        if not self.is_tty or self.is_windows:
            return message
        for name, color in iteritems(self.logger_map):
            if record.name.startswith(name):
                return self.colorize(message, fg=color)
        if record.levelno in self.level_map:
            bg, fg, bold = self.level_map[record.levelno]
            return self.colorize(message, bg=bg, fg=fg, bold=bold)
        return message

    def colorize(self, message, bg=None, fg=None, bold=False):
        params = []
        if bg in COLORS:
            params.append(str(COLORS.index(bg) + 40))
        if fg in COLORS:
            params.append(str(COLORS.index(fg) + 30))
        if bold:
            params.append('1')
        if params:
            message = ''.join((
                self.csi, ';'.join(params), 'm', message, self.reset))
        return message
