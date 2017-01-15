# -*- coding: utf-8 -*-
import pytest

import os
from os import environ

import sys
import tempfile

from time import sleep
from subprocess import Popen
from subprocess import call

import unittest
import unittest.mock as mock

import pydbus
from pydbus import SessionBus
from pydbus import connect

import time

# from scarlett_os import tests
from tests import PROJECT_ROOT
# import PROJECT_ROOT


""" Component test fixtures.
    This module makes the following assumptions:
    * [IGNORE] py.test is invoked from the same directory as this module is located
    * [IGNORE] start_outside_service.py is located in the same directory
    * [IGNORE] dbus-proxy is found in a build/ directory one level above, i.e. "../build/dbus-proxy"
    * dbus has already been started up by Docker or is running on your OS
"""

# source: https://github.com/wmanley/pulsevideo/blob/d8259f2ce2f3951e380e319c80b9d124b47efdf2/tests/integration_test.py
def wait_until(f, timeout_secs=10):
    expiry_time = time.time() + timeout_secs
    while True:
        val = f()
        if val:
            return val  # truthy
        if time.time() > expiry_time:
            return val  # falsy

########################################################################
#       code from pydbus
########################################################################
# DBUS_SESSION_BUS_ADDRESS = os.getenv("DBUS_SESSION_BUS_ADDRESS")

# with connect(DBUS_SESSION_BUS_ADDRESS) as bus:
#   bus.dbus

# del bus._dbus
# try:
#   bus.dbus
#   assert(False)
# except RuntimeError:
#   pass

# with SessionBus() as bus:
#   pass

# # SessionBus() and SystemBus() are not closed automatically, so this should work:
# bus.dbus
########################################################################

# OUTSIDE_SOCKET = "/tmp/dbus_proxy_outside_socket"
# INSIDE_SOCKET = "/tmp/dbus_proxy_inside_socket"

# source: http://stackoverflow.com/questions/17278650/python-3-script-using-libnotify-fails-as-cron-job
if not 'DISPLAY' in os.environ:
    os.environ['DISPLAY'] = ':0'

if not 'DBUS_SESSION_BUS_ADDRESS' in os.environ:
  print('NOTE: DBUS_SESSION_BUS_ADDRESS environment var not found!')

# Setup an environment for the fixtures to share so the bus address is the same for all
environment = environ.copy()

########################################################################
# NOTE: unix sockets, abstract ( eg 'unix:abstract=' )
########################################################################
# source: http://man7.org/linux/man-pages/man7/unix.7.html
# abstract: an abstract socket address is distinguished
# (from a pathname socket) by the fact that sun_path[0]
# is a null byte ('\0').
# The socket's address in this namespace is given by the additional
# bytes in sun_path that are covered by the specified length of the
# address structure. (Null bytes in the name have no
# special significance.)

# The name has no connection with filesystem pathnames.
# When the address of an abstract socket is returned,
# the returned addrlen is greater than
# sizeof(sa_family_t) (i.e., greater than 2),
# and the name of the socket is contained in the first
# (addrlen - sizeof(sa_family_t)) bytes of sun_path.
########################################################################
#
########################################################################
# DBUS_SESSION_BUS_ADDRESS=unix:abstract=/tmp/dbus-MAIDjJlN9C,guid=1f05155ec6139a513e017f81587a8693
# environment["DBUS_SESSION_BUS_ADDRESS"] = "unix:path=" + OUTSIDE_SOCKET

# TODO: own_name() is deprecated, use request_name() instead.
# bus.own_name(name='org.scarlett')

########################################################################
# NOTE: pytest.fixture scopes:
# function - Run once per test
# class - Run once per class of tests
# module - Run once per module
# session -Run once per session
########################################################################

# from pydbus import SessionBus

# done = 0


# def get_session_bus():
#     bus = SessionBus()
#     bus.own_name(name='org.scarlett')
#     return bus


# class TestScarlettSpeaker(unittest.TestCase):

#     def __load_dbus_service(self):

#       bus = get_session_bus()

#       sl = mpris.ScarlettListener(bus=bus.con, path='/org/scarlett/Listener')

#       pass
#
#
########################################################################
# from pydbus - BEGIN
########################################################################
# ADDRESS_FILE=$(mktemp /tmp/pydbustest.XXXXXXXXX)
# PID_FILE=$(mktemp /tmp/pydbustest.XXXXXXXXX)

# dbus-daemon --session --print-address=0 --print-pid=1 --fork 0>"$ADDRESS_FILE" 1>"$PID_FILE"
#   --print-address[=DESCRIPTOR]
#              Print the address of the message bus to standard output,
#              or to the given file descriptor. This is used by programs
#              that launch the message bus.
#   --session
#              Use the standard configuration file for the
#              per-login-session message bus.
#
#   --print-pid[=DESCRIPTOR]
#       Print the process ID of the message bus to standard output,
#       or to the given file descriptor. This is used by
#       programs that launch the message bus.
#
#   --fork
#       Force the message bus to fork and become a daemon,
#       even if the configuration file does not specify that it should.
#       In most contexts the configuration file already gets this right,
#       though. This option is not supported on Windows.
# export DBUS_SESSION_BUS_ADDRESS=$(cat "$ADDRESS_FILE")
########################################################################
# from pydbus - END
########################################################################

########################################################################
# file descriptor 0,1,2 meaning - BEGIN
########################################################################
# source: https://en.wikipedia.org/wiki/File_descriptor
#
#
# 0 Standard input  STDIN_FILENO  stdin
# 1 Standard output STDOUT_FILENO stdout
# 2 Standard error  STDERR_FILENO stderr
#
########################################################################
# file descriptor 0,1,2 meaning - END
########################################################################

OUTSIDE_SOCKET = "/tmp/dbus_proxy_outside_socket"
INSIDE_SOCKET = "/tmp/dbus_proxy_inside_socket"


# Setup an environment for the fixtures to share so the bus address is the same for all
environment["DBUS_SESSION_BUS_ADDRESS"] = "unix:path=" + OUTSIDE_SOCKET

# print(environment["DBUS_SESSION_BUS_ADDRESS"])


@pytest.fixture(scope="module", autouse=True)
def session_bus(request):
    """ Create a session bus.

        The dbus-deamon will be torn down at the end of the test.
    """
    # TODO: Parametrize the socket path.

    dbus_daemon = None
    # The 'exec' part is a workaround to make the whole process group be killed
    # later when kill() is caled and not just the shell. This is only needed when
    # 'shell' is set to True like in the later Popen() call below.
    start_dbus_daemon_command = [
        "exec",
        " dbus-daemon",
        " --session",
        " --nofork",
        " --address=" + "unix:path=" + OUTSIDE_SOCKET
    ]
    try:
        # For some reason shell needs to be set to True, which is the reason the command
        # is passed as a string instead as an argument list, as recommended in the docs.
        dbus_daemon = Popen(
            "".join(start_dbus_daemon_command),
            env=environment,
            shell=True,
            stdout=sys.stdout)
        # Allow time for the bus daemon to start
        sleep(0.3)
    except OSError as e:
        print("Error starting dbus-daemon: {}".format(str(e)))
        sys.exit(1)

    def teardown():
        dbus_daemon.kill()
        os.remove(OUTSIDE_SOCKET)

    request.addfinalizer(teardown)


@pytest.fixture(scope='module')
def get_session_bus(init_session_bus):
    """
    Provide the session bus instance.

    Adapted from: https://github.com/martinpitt/python-dbusmock/blob/master/dbusmock/testcase.py#L137
    """
    # Fixture finalization / executing teardown code pytest
    # supports execution of fixture specific finalization code
    # when the fixture goes out of scope.
    # By using a yield statement instead of return,
    # all the code after the yield
    # statement serves as the teardown code.:
    if os.environ.get('DBUS_SESSION_BUS_ADDRESS'):
        bus = connect(environment["DBUS_SESSION_BUS_ADDRESS"])
        # yield bus
        # print("teardown new session bus")
        # return dbus.bus.BusConnection(os.environ['DBUS_SESSION_BUS_ADDRESS'])
    else:
        bus = SessionBus()
        # yield bus
        # print("teardown existing session bus")
        # Out[4]: <DBUS.org.freedesktop.DBus at 0x7fb8f40389b0>

    try:
        yield bus
    finally:
        print("Tearing down session bus object")
        del bus._dbus
        print("ran: del bus._dbus")
        # os.remove(socket_path)
        # dbus_daemon.kill()
        # dbus_daemon.wait()
        # 1/14/2017 # NOTE: RE-ENABLE THIS # del os.environ['DBUS_SESSION_BUS_ADDRESS']

# @pytest.fixture
# def hamster_service(request, session_bus):
#     """
#     Provide a hamster service running as a seperate process.

#     This is heavily inspired by the way ``dbusmock`` sets up its ``mock_server``
#     """
#     import subprocess
#     import sys
#     import time
#     import psutil
#     def fin():
#         # [FIXME]
#         # We propably could be a bit more gentle then this.
#         os.kill(deamon.pid, signal.SIGKILL)
#     env = os.environ.copy()
#     deamon = subprocess.Popen([sys.executable, '-m', 'hamster_dbus.hamster_dbus', 'server'], env=env)
#     # Wait for the service to become available
#     time.sleep(2)
#     request.addfinalizer(fin)
#     return deamon


@pytest.fixture(scope="module")
def service_on_outside(request):
    """ Start the service on the "outside" as seen from the proxy.

        The service is torn down at the end of the test.
    """
    # TODO: Make it more robust w.r.t. where to find the service file.

    outside_service = None
    scarlett_root = r"{}".format(PROJECT_ROOT)

    try:
        outside_service = Popen(
            [
                "python3",
                "-m",
                "scarlett_os.mpris"
            ],
            env=environment,
            stdout=sys.stdout,
            cwd=scarlett_root)
        # Allow time for the service to show up on the bus
        # before consuming tests can try to use it.
        sleep(0.3)
    except OSError as e:
        print("Error starting service on outside: {}".format(str(e)))
        sys.exit(1)

    def teardown():
        outside_service.kill()

    request.addfinalizer(teardown)



########################################################################
# NOTE: Taken from pydbus py.test PR
########################################################################
# source: https://github.com/xZise/pydbus/blob/addf3913368cdc7225039525f3e53ab62b2a0f70/pydbus/tests/publish_multiface.py
# from pydbus import SessionBus
# from gi.repository import GLib
# from threading import Thread, Lock
# import sys
# import time

# import pytest

# from pydbus.tests.util import ClientThread

# @pytest.fixture
# def defaults():
#   loop = GLib.MainLoop()
#   loop.cancelled = False
#   bus = SessionBus()

#   obj = DummyObject()
#   with bus.publish("net.lew21.pydbus.tests.expose_multiface", obj):
#     yield loop, obj, bus.get("net.lew21.pydbus.tests.expose_multiface")


# def run(loop, func):
#   thread = ClientThread(func, loop)
#   GLib.timeout_add_seconds(2, loop.quit)

#   thread.start()
#   loop.run()

#   try:
#     return thread.result
#   except ValueError:
#     pytest.fail('Unable to finish thread')
# def test_using_multiface(defaults):
#   def thread_func():
#     results = []
#     results += [remote.Method1()]
#     results += [remote.Method2()]
#     return results

#   loop, obj, remote = defaults

#   result = run(loop, thread_func)

#   assert result == ["Method1", "Method2"]
#   assert obj.done == ["Method1", "Method2"]
########################################################################
#

# @pytest.fixture
# def hamster_service3(request, session_bus):
#     """
#     This works as intended.

#     We delegate loop setup and service instanciation to a new subprocess.
#     Unline many examples we do not use ``process.join()`` as this would block our
#     process indefinitly.
#     Using pytest teardown mechanics will make sure we shut down the spawned process
#     afterwards. This is where ``multiprocessing`` surpasses our ``threading`` based
#     solution.
#     """
#     import multiprocessing
#     def run_service():
#         """Set up the mainloop and instanciate our dbus service class."""
#         DBusGMainLoop(set_as_default=True)
#         loop = GLib.MainLoop()
#         myservice = HamsterDBusService()
#         loop.run()
#     def fin():
#         """Shutdown the mainloop process."""
#         process.terminate()
#     process = multiprocessing.Process(target=run_service)
#     process.start()
#     # Make sure we give it time to launch. Otherwise clients may query to early.
#     time.sleep(2)
#     request.addfinalizer(fin)
#     return process


@pytest.fixture(scope="module")
def scarlett_os_interface(request, session_bus):
# ORIG # def scarlett_os_interface(request, session_bus, hamster_service3):
    """Provide a covinient interface hook to our hamster-dbus service."""
    time.sleep(2)
    # bus.request_name(name='org.scarlett')
    # sl = ScarlettListener(bus=bus.con, path='/org/scarlett/Listener')
    # ORIG # return session_bus.get_object('org.gnome.hamster_dbus', '/org/gnome/hamster_dbus')
    return session_bus.request_name(name='org.scarlett')

