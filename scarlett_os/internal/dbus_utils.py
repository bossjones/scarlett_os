# NOTE: Borrowed basically all of this from Gosa project.

# import os
# import sys

# try:
#     # import pydbus
#     from pydbus import SessionBus

# except ImportError:
#     print("Please install the python dbus module.")
#     sys.exit(1)

# import time
# import threading
# import logging
# from scarlett_os.internal.gi import GLib

# from scarlett_os.internal.system_utils import get_pid

# logger = logging.getLogger(__name__)


# def parse_session_bus_from_env(pname='dbus-daemon'):
#     """
#     Provide a new private session bus so we don't polute the regular one.

#     This is a straight copy of: https://github.com/martinpitt/python-dbusmock/blob/master/dbusmock/testcase.py#L92

#     Returns:
#         tuple: (pid, address) pair.
#     """
#     # source: https://github.com/projecthamster/hamster-dbus/blob/cfd4cabda55779d2f07649c6c364e2e781e3d7c5/tests/conftest.py

#     address = os.environ.get('DBUS_SESSION_BUS_ADDRESS')
#     pid = get_pid(pname)

#     return (pid, address)
