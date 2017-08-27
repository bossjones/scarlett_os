# -*- coding: utf-8 -*-
import logging
import os
from os import environ
import select
import signal
import subprocess
from subprocess import Popen, call
import sys
import tempfile
import time
from time import sleep
import unittest
import unittest.mock as mock

import pydbus
from pydbus import SessionBus, connect
import pytest
from _pytest.monkeypatch import MonkeyPatch

from tests import PROJECT_ROOT

""" Component test fixtures.
    This module makes the following assumptions:
    * [IGNORE] py.test is invoked from the same directory as this module is located
    * [IGNORE] start_outside_service.py is located in the same directory
    * [IGNORE] dbus-proxy is found in a build/ directory one level above, i.e. "../build/dbus-proxy"
    * dbus has already been started up by Docker or is running on your OS
"""

OUTSIDE_SOCKET = "/tmp/dbus_proxy_outside_socket"
INSIDE_SOCKET = "/tmp/dbus_proxy_inside_socket"

# source: https://github.com/pytest-dev/pytest/issues/363
@pytest.fixture(scope="function")
def monkeysession(request):
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()

# source: https://github.com/YosaiProject/yosai/blob/master/test/isolated_tests/core/conf/conftest.py
@pytest.fixture(scope='function')
def mockersession(mocker):
    '''Stop previous mocks, yield mocker plugin obj, then stopall mocks again'''
    print('Called [setup]: mocker.stopall()')
    mocker.stopall()
    yield mocker
    print('Called [teardown]: mocker.stopall()')
    mocker.stopall()

# source: https://github.com/YosaiProject/yosai/blob/master/test/isolated_tests/core/conf/conftest.py
@pytest.fixture(scope='function')
def empty():
    return object()

# source: https://github.com/wmanley/pulsevideo/blob/d8259f2ce2f3951e380e319c80b9d124b47efdf2/tests/integration_test.py


def wait_until(f, timeout_secs=10):
    expiry_time = time.time() + timeout_secs
    while True:
        val = f()
        if val:
            return val  # truthy
        if time.time() > expiry_time:
            return val  # falsy

# source: https://stackoverflow.com/questions/25072126/why-does-python-lint-want-me-to-use-different-local-variable-name-than-a-global


def setup_environment():
    # source: http://stackoverflow.com/questions/17278650/python-3-script-using-libnotify-fails-as-cron-job  # noqa
    if 'TRAVIS_CI' in os.environ:
        if 'DISPLAY' not in os.environ:
            # TODO: Should this be on :99 ?
            os.environ['DISPLAY'] = ':0'

    if 'DBUS_SESSION_BUS_ADDRESS' not in os.environ:
        print('NOTE: DBUS_SESSION_BUS_ADDRESS environment var not found!')

    # Setup an environment for the fixtures to share so the bus address is the same for all  # noqa
    environment = environ.copy()

    # Setup an environment for the fixtures to share so the bus address is the same for all
    environment["DBUS_SESSION_BUS_ADDRESS"] = "unix:path=" + OUTSIDE_SOCKET

    print("[DBUS_SESSION_BUS_ADDRESS]: {}".format(environment["DBUS_SESSION_BUS_ADDRESS"]))
    return environment


@pytest.fixture(scope="session")
def get_environment():
    yield setup_environment()

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

########################################################################
# NOTE: pytest.fixture scopes:
# function - Run once per test
# class - Run once per class of tests
# module - Run once per module
# session -Run once per session
########################################################################

########################################################################
# from pydbus - BEGIN
########################################################################
# ADDRESS_FILE=$(mktemp /tmp/pydbustest.XXXXXXXXX)
# PID_FILE=$(mktemp /tmp/pydbustest.XXXXXXXXX)

# dbus-daemon --session --print-address=0 --print-pid=1 --fork 0>"$ADDRESS_FILE" 1>"$PID_FILE"  # noqa
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

# source: https://github.com/Alberto-Beralix/Beralix/blob/dd890d68e71d84618648a2e5f33196c8d064e18b/i386-squashfs-root/usr/share/software-center/softwarecenter/testutils.py
@pytest.fixture(scope="module")
def create_dummy_session_dbus(request):
    # source: dbus-proxy
    """
    Create a dummy session bus.

    The dbus-deamon will be torn down at the end of the test.
    """
    # TODO: Parametrize the socket path.

    if 'TRAVIS_CI' in os.environ:
        if 'DISPLAY' not in os.environ:
            # TODO: Should this be on :99 ?
            os.environ['DISPLAY'] = ':0'

    m_dbus = None
    # The 'exec' part is a workaround to make the whole process group be killed
    # later when kill() is called and not just the shell. This is only needed when
    # 'shell' is set to True like in the later Popen() call below.
    start_dbus_daemon_command = [
        # "exec",
        "dbus-daemon",
        "--session",
        "--nofork",
        "--print-address"
    ]
    try:
        # For some reason shell needs to be set to True,
        # which is the reason the command is passed as
        # a string instead as an argument list,
        # as recommended in the docs.
        m_dbus = Popen(start_dbus_daemon_command, stdout=subprocess.PIPE)
        # import pdb;pdb.set_trace()
        # get and store address
        bus_address = m_dbus.stdout.readline().strip()
        print('[m_dbus.stdout.readline().strip()]')
        print(bus_address)
        print(bus_address.decode('utf-8'))
        print(type(bus_address))
        print(type(bus_address.decode('utf-8')))
        os.environ["SOFTWARE_CENTER_APTD_FAKE"] = bus_address.decode('utf-8')
        print('\n[setup] create_session_bus, dbus-daemon running ...')
        # Allow time for the bus daemon to start
        sleep(0.5)
    except OSError as e:
        print("Error starting dbus-daemon: {}".format(str(e)))
        sys.exit(1)

    def teardown():
        print('\n[teardown] create_session_bus, killing dbus-daemon ...')
        m_dbus.terminate()
        m_dbus.wait()
        m_dbus.kill()
        del os.environ["SOFTWARE_CENTER_APTD_FAKE"]
        # dbus_daemon.kill()
        # os.remove(OUTSIDE_SOCKET)

    # The finalizer is called after all of the tests that use the fixture.
    # If you’ve used parameterized fixtures,
    # the finalizer is called between instances of the parameterized fixture changes.
    request.addfinalizer(teardown)



@pytest.fixture(scope="module")
def create_session_bus(request, get_environment):
    # source: dbus-proxy
    """
    Create a session bus.

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
        # For some reason shell needs to be set to True,
        # which is the reason the command is passed as
        # a string instead as an argument list,
        # as recommended in the docs.
        dbus_daemon = Popen(
            "".join(start_dbus_daemon_command),
            env=get_environment,
            shell=True,
            stdout=sys.stdout)
        print('\n[setup] create_session_bus, dbus-daemon running ...')
        # Allow time for the bus daemon to start
        sleep(0.3)
    except OSError as e:
        print("Error starting dbus-daemon: {}".format(str(e)))
        sys.exit(1)

    def teardown():
        print('\n[teardown] create_session_bus, killing dbus-daemon ...')
        dbus_daemon.kill()
        os.remove(OUTSIDE_SOCKET)

    # The finalizer is called after all of the tests that use the fixture.
    # If you’ve used parameterized fixtures,
    # the finalizer is called between instances of the parameterized fixture changes.
    request.addfinalizer(teardown)


@pytest.fixture(scope="module")
# @pytest.fixture
def service_on_outside(request, get_environment, create_session_bus):
    # FROM: dbus-proxy
    """
    Start the service on the "outside" as seen from the proxy.

    The service is torn down at the end of the test.
    """
    # TODO: Make it more robust w.r.t. where to find the service file.

    outside_service = None
    scarlett_root = r"{}".format(PROJECT_ROOT)
    print("[service_on_outside]: {}".format(scarlett_root))

    try:
        outside_service = Popen(
            [
                "python3",
                "-m",
                "scarlett_os.mpris"
            ],
            env=get_environment,
            stdout=sys.stdout,
            cwd=scarlett_root)
        # Allow time for the service to show up on the bus
        # before consuming tests can try to use it.
        print('\n[setup] service_on_outside, mpris running')
        sleep(0.3)
    except OSError as e:
        print("Error starting service on outside: {}".format(str(e)))
        sys.exit(1)

    def teardown():
        print('\n[teardown] service_on_outside finalizer, disconnect from dbus mpris')
        outside_service.kill()

    # The finalizer is called after all of the tests that use the fixture.
    # If you’ve used parameterized fixtures,
    # the finalizer is called between instances of the parameterized fixture changes.
    request.addfinalizer(teardown)


@pytest.fixture
def service_tasker(request, get_environment):
    """
    Start the Scarlett Tasker Service after the mpris is already running

    The service is torn down at the end of the test.
    """

    tasker_service = None
    scarlett_root = r"{}".format(PROJECT_ROOT)
    print("[service_tasker]: {}".format(scarlett_root))

    try:
        tasker_service = Popen(
            [
                "python3",
                "-m",
                "scarlett_os.tasker"
            ],
            env=get_environment,
            stdout=sys.stdout,
            cwd=scarlett_root)
        # Allow time for the service to show up on the bus
        # before consuming tests can try to use it.
        sleep(0.3)
    except OSError as e:
        print("Error starting service on outside: {}".format(str(e)))
        sys.exit(1)

    def teardown():
        tasker_service.kill()

    # The finalizer is called after all of the tests that use the fixture.
    # If you’ve used parameterized fixtures,
    # the finalizer is called between instances of the parameterized fixture changes.
    request.addfinalizer(teardown)


@pytest.fixture(scope='module')
def get_bus(request, get_environment, create_session_bus):
    """
    Provide the session bus instance.

    Adapted from: https://github.com/martinpitt/python-dbusmock/blob/master/dbusmock/testcase.py#L137  # noqa
    """
    # Fixture finalization / executing teardown code pytest
    # supports execution of fixture specific finalization code
    # when the fixture goes out of scope.
    # By using a yield statement instead of return,
    # all the code after the yield
    # statement serves as the teardown code.:
    # if os.environ.get('DBUS_SESSION_BUS_ADDRESS'):
    if get_environment['DBUS_SESSION_BUS_ADDRESS']:
        print("[get_bus] inside if environment['DBUS_SESSION_BUS_ADDRESS']")
        bus = connect(get_environment["DBUS_SESSION_BUS_ADDRESS"])
        # yield bus
        # print("teardown new session bus")
        # return dbus.bus.BusConnection(os.environ['DBUS_SESSION_BUS_ADDRESS'])
    else:
        print('\n[get_bus] default SessionBus')
        bus = SessionBus()

    def teardown():
        """
        As historical note, another way to write teardown code is by
        accepting a request object into your fixture function and can
        call its request.addfinalizer one or multiple times:
        """
        # NOTE: # SessionBus() and SystemBus() are not closed automatically, so this should work
        # source: https://github.com/xZise/pydbus/blob/addf3913368cdc7225039525f3e53ab62b2a0f70/pydbus/bus.py#L31
        # NOTE: bus.dbus = @property from pydbus bus object.
        # NOTE: When you try to grab the property and it doesn't exist,
        # NOTE: it assigns a dbus connection again via: self._dbus = self.get(".DBus")[""]
        # NOTE: That's why we delete it each time
        # print("running: bus.con.close()")
        # bus.con.close()

        print("running: del bus._dbus")
        del bus._dbus

    # The finalizer is called after all of the tests that use the fixture.
    # If you’ve used parameterized fixtures,
    # the finalizer is called between instances of the parameterized fixture changes.
    request.addfinalizer(teardown)

    bus.dbus

    return bus


# @pytest.fixture
# def hamster_service(request, session_bus):
#     """
#     Provide a hamster service running as a seperate process.
#
#     This is heavily inspired by the way
#     ``dbusmock`` sets up its ``mock_server``
#     """
#     import subprocess
#     import sys
#     import time
#     import psutil
#     def fin():
#         # We propably could be a bit more gentle then this.
#         os.kill(deamon.pid, signal.SIGKILL)
#     env = os.environ.copy()
#     deamon = subprocess.Popen([sys.executable,
#                               '-m',
#                               'hamster_dbus.hamster_dbus',
#                               'server'], env=env)
#     # Wait for the service to become available
#     time.sleep(2)
#     request.addfinalizer(fin)
#     return deamon


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
#
# def test_using_multiface(defaults):
#     def thread_func():
#         results = []
#         results += [remote.Method1()]
#         results += [remote.Method2()]
#         return results

#     loop, obj, remote = defaults

#     result = run(loop, thread_func)

#     assert result == ["Method1", "Method2"]
#     assert obj.done == ["Method1", "Method2"]
########################################################################
#

# TODO: See if this is something we want to do or not
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
def scarlett_os_interface(request, get_environment, get_bus):
    # ORIG # def scarlett_os_interface(request, session_bus, hamster_service3):  # noqa
    """Provide a covinient interface hook to our hamster-dbus service."""
    time.sleep(2)
    # bus.request_name(name='org.scarlett')
    # sl = ScarlettListener(bus=bus.con, path='/org/scarlett/Listener')
    # ORIG # return session_bus.get_object('org.gnome.hamster_dbus', '/org/gnome/hamster_dbus')  # noqa
    print("[get_bus] in [scarlett_os_interface]: {}".format(get_bus))
    get_bus.request_name(name='org.scarlett')
    return get_bus


# @pytest.fixture
@pytest.fixture(scope="module")
def get_dbus_proxy_obj_helper(request, get_environment, get_bus):
    """
    Returns dbus proxy object connected to org.scarlett @ /org/scarlett/Listener  # noqa

    ProxyObject implementing all the Interfaces exposed by the remote object.
    """
    time.sleep(2)
    print("[get_dbus_proxy_obj_helper] ('org.scarlett','/org/scarlett/Listener')")  # noqa
    return get_bus.get("org.scarlett", object_path='/org/scarlett/Listener')


# TODO: Think about implementing this, it allows you to create one DBusRunner per test session
# source: https://github.com/peuter/gosa/blob/master/client/conftest.py
# @pytest.fixture(scope="session", autouse=True)
# def use_test_config(request):
#     Environment.reset()
#     Environment.config = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "test_conf")
#     Environment.noargs = True
#     env = Environment.getInstance()

#     # Enable DBus runner
#     dr = DBusRunner()
#     dr.start()

#     PluginRegistry(component='gosa.client.module')  # @UnusedVariable
#     env.active = True

#     def shutdown():
#         env.active = False

#         # Wait for threads to shut down
#         for t in env.threads:
#             if hasattr(t, 'stop'):
#                 t.stop()
#             if hasattr(t, 'cancel'):
#                 t.cancel()
#             t.join(2)

#         PluginRegistry.shutdown()
#         dr.stop()

#     request.addfinalizer(shutdown)

@pytest.fixture
def service_receiver(request, get_environment):
    """
    Start the Scarlett Tasker Service after the mpris is already running

    The service is torn down at the end of the test.
    """

    receiver_service = None

    receiver_cmd = [
        "python3",
        "-m",
        "scarlett_os.receiver"
    ]

    try:
        receiver_service = ProcessMonitor(receiver_cmd, environment=get_environment)
        # Allow time for the service to show up on the bus
        # before consuming tests can try to use it.
        sleep(0.3)
    except OSError as e:
        print("Error starting service on outside: {}".format(str(e)))
        sys.exit(1)

    def teardown():
        receiver_service.terminate()
        print("ran: receiver_service.terminate()")
    request.addfinalizer(teardown)

    return receiver_service


# NOTE: Borrowed this straight from gst-switch. Using it for integration testing
class BaseError(Exception):

    """docstring for BaseError"""
    pass


class PathError(BaseError):

    """docstring for PathError"""
    pass


class ServerProcessError(BaseError):

    """docstring for ServerProcessError"""
    pass


class MatchTimeoutError(BaseError):

    """Timeout during ProcessMonitor.wait_for_output"""
    pass


class MatchEofError(BaseError):

    """Process died during ProcessMonitor.wait_for_output"""
    pass


class SelectError(BaseError):

    """select.select returned with an unknown Error
       during ProcessMonitor.wait_for_output"""
    pass


class ProcessMonitor(subprocess.Popen):
    """Runs a command in a background-thread and monitors its output

    Can block until the command prints a certain string and log the full
    output into a file
    """

    def __init__(self, cmd, cmd_output_target=sys.stderr, environment=None):
        self.log = logging.getLogger('server-output-monitor')

        # Logfile to write to
        self._cmd_output_target = cmd_output_target

        # Internal Buffer to search for matched when wait_for_output is called
        self._buffer = ""

        self.log.debug("starting subprocess")

        scarlett_root = r"{}".format(PROJECT_ROOT)

        try:
            super(ProcessMonitor, self).__init__(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=4096,
                env=environment,
                cwd=scarlett_root)
        except Exception as err:
            raise ServerProcessError(err)

        self.log.debug("subprocess successfully started")

    def terminate(self):
        """Kills the process and waits for the thread to exit"""

        self.log.debug("terminating the subprocess")
        super(ProcessMonitor, self).terminate()

        self.log.info("reading remaining data from subprocess")
        while True:
            # select takes three lists of file-descriptors to be monitored:
            #   readable, writeable and exceptional
            # The last argument is the timeout after which select should give
            # up. 0 means, that select should return immediately without
            # blocking (called a "poll")
            (read, _, _) = select.select([self.stdout], [], [], 0)

            # if the processes' stdout is not readable (ie there is nothing
            # to read), we're done and can exit the loop
            if self.stdout not in read:
                break

            # otherwise read as many bytes as possible, up to 2000,
            # from the process. os.read does not wait until exactly 2000
            # bytes have been read but returns as many bytes as possible
            # the only time os.read block is, when there's nothing to read,
            # which we ruled out by the poll-call to select before
            #
            # os.read -in contrast to self.stdout.read- is non-blocking,
            # if at least 1 character is readable.
            self.log.debug("reading data from subprocess")
            chunk = os.read(self.stdout.fileno(), 2000).decode('utf-8')

            if len(chunk) == 0:
                break

            self.log.debug(
                "read %d bytes, appending to cmd_output_target",
                len(chunk))
            self._cmd_output_target.write(chunk)

        # TODO: In python3 I'd add a timeout here but because of the forced
        # python2 compatibility it's not that simple. Using subprocess32
        # requires different patching in the unit-tests.
        self.log.debug("waiting for the subprocess to die")
        super(ProcessMonitor, self).communicate()

    def wait_for_output(self, match, timeout=5, count=1):
        """Searches the output already captured from the running process for
        match and returns immediatly if match has already been captured.

        Sets up a match-request for the stdout/stderr-reader and blocks until
        match emerges in the processes stdout/stderr but not longer then
        timeout. If no match is found until timeout is passed, a RuntimeError
        is raised.
        """
        if self._buffer.count(match) >= count:
            self.log.debug("match found, returning without reading more data")
            return

        endtime = time.time() + timeout
        while True:
            timeout = endtime - time.time()
            self.log.debug("waiting for data output by subprocess"
                           "(remaining time to timeout = %fs)", timeout)

            # select takes three lists of file-descriptors to be monitored:
            #   readable, writeable and exceptional
            # The last argument is the timeout after which select should give
            # up. If one of the supplied descriptors gets readable within the
            # supplied timeout, the function returns.
            (read, _, _) = select.select([self.stdout], [], [], timeout)

            # if the processed' stdout is not readable (ie there's
            # to read) and select did return nevertheless, so there must have
            # been an exception or a timeout.
            if self.stdout not in read:
                remaining = endtime - time.time()
                if remaining < 0:
                    raise MatchTimeoutError(
                        "Timeout while waiting for match "
                        "'%s' %dx in the subprocess output.\n"
                        "re-run tests with -x and look at "
                        "server.log to investigate further"
                        % (match, count,))

                raise SelectError("select returned without stdout being"
                                  " readable, assuming an exception")

            # read as many bytes as possible, up to 2000,
            # from the process. os.read does not wait until exactly 2000
            # bytes have been read but returns as many bytes as possible
            # the only time os.read block is, when there's nothing to read,
            # which we ruled out by the call to select before
            #
            # os.read -in contrast to self.stdout.read- is non-blocking,
            # if at least 1 character is readable.
            self.log.debug("reading data from subprocess")
            chunk = os.read(self.stdout.fileno(), 2000).decode('utf-8')

            if len(chunk) == 0:
                raise MatchEofError("Subprocess died while waiting for match "
                                    "'%s' %dx in the subprocess output."
                                    % (match, count,))

            self.log.debug("read %d bytes, appending to buffer", len(chunk))
            self._buffer += chunk
            self._cmd_output_target.write(chunk)

            self.log.debug("testing again for %dx '%s' in buffer",
                           count, match)
            if self._buffer.count(match) >= count:
                self.log.debug("match found, returning")
                return


if __name__ == "__main__":
    print('testing_create_session_bus')
    print('testing_create_session_bus_end')
