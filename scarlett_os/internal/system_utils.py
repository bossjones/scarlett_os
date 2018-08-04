# -*- coding: utf-8 -*-

import logging
from subprocess import check_output
from scarlett_os.internal.encoding import bytesting_to_string


logger = logging.getLogger(__name__)


def get_pid(name):
    """Get pid of process by name if it exists."""
    try:
        pid = check_output(["pidof", name])
    except:
        logger.error("Process of that name does not exist.")
        return False

    return bytesting_to_string(pid).rstrip("\n")
