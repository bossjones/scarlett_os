#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Scarlett Dbus Service. Implemented via MPRIS D-Bus Interface Specification."""

# __future__ is a real module, and serves three purposes:
#
# To avoid confusing existing tools that analyze import statements and expect to find the modules theyre importing.
#
# To ensure that future statements run under releases prior to 2.1 at least yield runtime exceptions (the import of __future__ will fail, because there was no module of that name prior to 2.1).
#
# To document when incompatible changes were introduced, and when they will be  or were  made mandatory. This is a form of executable documentation, and can be inspected programmatically via importing __future__ and examining its contents.

# with:
#    This PEP adds a new statement "with" to the Python language to make it possible to
#    factor out standard uses of try/finally statements.
#    In this PEP, context managers provide __enter__() and __exit__()
#    methods that are invoked on entry to and exit from the body of the
#    with statement.

# division: PEP 238 -- Changing the Division Operator
#   We propose to fix this by introducing different operators for
#   different operations: x/y to return a reasonable approximation of
#   the mathematical result of the division ("true division"), x//y to
#   return the floor ("floor division").  We call the current, mixed
#   meaning of x/y "classic division".


from __future__ import with_statement, division, absolute_import

# from scarlett_os.compat import configparser  # noqa

import sys
import os

from scarlett_os.internal.debugger import init_debugger

init_debugger()

# TODO: Move this to a debug function that allows you to enable it or disable it
os.environ[
    "GST_DEBUG_DUMP_DOT_DIR"] = "/home/pi/dev/bossjones-github/scarlett_os/_debug"
os.putenv('GST_DEBUG_DUMP_DIR_DIR',
          '/home/pi/dev/bossjones-github/scarlett_os/_debug')

from scarlett_os.internal.gi import gi, GObject, Gst, GLib, Gio
import threading

import pprint
pp = pprint.PrettyPrinter(indent=4)

import logging
logger = logging.getLogger(__name__)

# An in-memory stream for text. It inherits TextIOWrapper.
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import re

# NOTE: ConfigParser does not exist in python3, only python2
# import ConfigParser

try:
    import configparser
except:
    from six.moves import configparser

# The signal.signal() function allows defining custom handlers to be executed when a signal is received. A small number of default handlers are installed: SIGPIPE is ignored (so write errors on pipes and sockets can be reported as ordinary Python exceptions) and SIGINT is translated into a KeyboardInterrupt exception.
import signal

# The gettext module provides internationalization (I18N) and localization (L10N) services for your Python modules and applications.
from gettext import gettext as _
from scarlett_os.utility.gnome import abort_on_exception, _IdleObject


from scarlett_os.const import (SCARLETT_CANCEL, SCARLETT_LISTENING,
                               SCARLETT_RESPONSE, SCARLETT_FAILED)

gst = Gst
HERE = os.path.dirname(__file__)
loop = GObject.MainLoop()


class Server(object):  # noqa
    def __repr__(self):
        return '<Server>'

    def __init__(self, bus, path, dbus_xml=None):
        super(Server, self).__init__()
        method_outargs = {}
        method_inargs = {}

        if dbus_xml:
            __xml = dbus_xml
        else:
            __xml = self.__doc__

        for interface in Gio.DBusNodeInfo.new_for_xml(__xml).interfaces:

            for method in interface.methods:
                method_outargs[method.name] = '(' + ''.join([arg.signature for arg in method.out_args]) + ')'
                method_inargs[method.name] = tuple(arg.signature for arg in method.in_args)

            bus.register_object(object_path=path,
                                interface_info=interface,
                                method_call_closure=self.on_method_call)

        self.method_inargs = method_inargs
        self.method_outargs = method_outargs

    def on_method_call(self,
                       connection,
                       sender,
                       object_path,
                       interface_name,
                       method_name,
                       parameters,
                       invocation):

        args = list(parameters.unpack())
        for i, sig in enumerate(self.method_inargs[method_name]):
            if sig is 'h':
                msg = invocation.get_message()
                fd_list = msg.get_unix_fd_list()
                args[i] = fd_list.get(args[i])

        result = getattr(self, method_name)(*args)

        # out_args is atleast (signature1). We therefore always wrap the result
        # as a tuple. Refer to https://bugzilla.gnome.org/show_bug.cgi?id=765603
        result = (result,)

        out_args = self.method_outargs[method_name]
        if out_args != '()':
            variant = GLib.Variant(out_args, result)
            invocation.return_value(variant)
        else:
            invocation.return_value(None)


class ScarlettListener(_IdleObject, Server):  # noqa
    '''
    <!DOCTYPE node PUBLIC '-//freedesktop//DTD D-BUS Object Introspection 1.0//EN'
    'http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd'>
    <node>
      <interface name='org.freedesktop.DBus.Introspectable'>
          <method name='Introspect'>
              <arg name='data' direction='out' type='s'/>
          </method>
      </interface>
      <interface name='org.freedesktop.DBus.Properties'>
          <method name='Get'>
              <arg name='interface' direction='in' type='s'/>
              <arg name='property' direction='in' type='s'/>
              <arg name='value' direction='out' type='v'/>
          </method>
          <method name="Set">
              <arg name="interface_name" direction="in" type="s"/>
              <arg name="property_name" direction="in" type="s"/>
              <arg name="value" direction="in" type="v"/>
          </method>
          <method name='GetAll'>
              <arg name='interface' direction='in' type='s'/>
              <arg name='properties' direction='out' type='a{sv}'/>
          </method>
      </interface>
      <interface name='org.scarlett.Listener1'>
        <method name='emitKeywordRecognizedSignal'>
          <arg type='s' name='s_cmd' direction='out'/>
        </method>
        <method name='emitCommandRecognizedSignal'>
          <arg type='s' name='command' direction='in'/>
          <arg type='s' name='s_cmd' direction='out'/>
        </method>
        <method name='emitSttFailedSignal'>
          <arg type='s' name='s_cmd' direction='out'/>
        </method>
        <method name='emitListenerCancelSignal'>
          <arg type='s' name='s_cmd' direction='out'/>
        </method>
        <method name='emitListenerReadySignal'>
          <arg type='s' name='s_cmd' direction='out'/>
        </method>
        <method name='emitConnectedToListener'>
          <arg type='s' name='scarlett_plugin' direction='in'/>
          <arg type='s' name='s_cmd' direction='out'/>
        </method>
        <method name='emitListenerMessage'>
          <arg type='s' name='s_cmd' direction='out'/>
        </method>
        <method name='Quit'/>
        <property name='CanQuit' type='b' access='read' />
        <property name='Fullscreen' type='b' access='readwrite' />
        <property name='CanRaise' type='b' access='read' />
        <property name='HasTrackList' type='b' access='read'/>
        <property name='Identity' type='s' access='read'/>
        <property name='DesktopEntry' type='s' access='read'/>
        <signal name='KeywordRecognizedSignal'>
          <arg type='(ss)' name='kw_rec_status' direction='out'/>
        </signal>
        <signal name='CommandRecognizedSignal'>
          <arg type='(sss)' name='cmd_rec_status' direction='out'/>
        </signal>
        <signal name='SttFailedSignal'>
          <arg type='(ss)' name='stt_failed_status' direction='out'/>
        </signal>
        <signal name='ListenerCancelSignal'>
          <arg type='(ss)' name='listener_cancel_status' direction='out'/>
        </signal>
        <signal name='ListenerReadySignal'>
          <arg type='(ss)' name='listener_rdy_status' direction='out'/>
        </signal>
        <signal name='ConnectedToListener'>
          <arg type='s' name='conn_to_lis_status' direction='out'/>
        </signal>
      </interface>
    </node>
    '''

    LISTENER_IFACE = 'org.scarlett.Listener'
    LISTENER_PLAYER_IFACE = 'org.scarlett.Listener.Player'
    LISTENER_TRACKLIST_IFACE = 'org.scarlett.Listener.TrackList'
    LISTENER_PLAYLISTS_IFACE = 'org.scarlett.Listener.Playlists'
    LISTENER_EVENTS_IFACE = 'org.scarlett.Listener.event'

    def __repr__(self):  # noqa
        return "<ScarlettListener({}, {})>".format(str(self.address), str(self.path))

    @abort_on_exception
    def __init__(self, bus, path):
        _IdleObject.__init__(self)

        # Synchronously connects to the message bus specified by bus_type
        self.con = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        self.bus_conn = bus
        self.path = path
        self.address = 'org.scarlett'

        # Starts acquiring name on the bus specified by bus_type and calls name_acquired_handler and name_lost_handler when the name is acquired respectively lost.
        # Callbacks will be invoked in the thread-default main loop of the thread you are calling this function from.
        Gio.bus_own_name_on_connection(self.con,
                                       'org.scarlett',
                                       Gio.BusNameOwnerFlags.NONE,
                                       None,
                                       None)

        Server.__init__(self, bus, path)

        super(ScarlettListener, self).__init__()

        self.dbus_stack = []
        self._message = 'This is the DBusServer'
        self._status_ready = "  ScarlettListener is ready"
        self._status_kw_match = "  ScarlettListener caught a keyword match"
        self._status_cmd_match = "  ScarlettListener caught a command match"
        self._status_stt_failed = "  ScarlettListener hit Max STT failures"
        self._status_cmd_start = "  ScarlettListener emitting start command"
        self._status_cmd_fin = "  ScarlettListener Emitting Command run finish"
        self._status_cmd_cancel = "  ScarlettListener cancel speech Recognition"

        self.dbus_stack.append(bus)
        self.dbus_stack.append(path)
        logger.debug("Inside self.dbus_stack")
        pp.pprint(self.dbus_stack)

    #########################################################
    # Scarlett dbus signals ( out = func args )
    #########################################################

    def KeywordRecognizedSignal(self, message, scarlett_sound):
        logger.debug(" sending message: {}".format(message))
        bus = self.dbus_stack[0]
        logger.debug("Inside KeywordRecognizedSignal. Dump bus object")
        pp.pprint(bus)
        kw_rec_status = GLib.Variant("(ss)", (message, scarlett_sound))
        bus.emit_signal(None,
                        '/org/scarlett/Listener',
                        'org.scarlett.Listener',
                        'KeywordRecognizedSignal',
                        kw_rec_status)

    def CommandRecognizedSignal(self, message, scarlett_sound, scarlett_cmd):
        logger.debug(" sending message: {}".format(message))
        bus = self.dbus_stack[0]
        cmd_rec_status = GLib.Variant(
            "(sss)", (message, scarlett_sound, scarlett_cmd))
        bus.emit_signal(None,
                        '/org/scarlett/Listener',
                        'org.scarlett.Listener',
                        'CommandRecognizedSignal',
                        cmd_rec_status)

    def SttFailedSignal(self, message, scarlett_sound):
        logger.debug(" sending message: {}".format(message))
        bus = self.dbus_stack[0]
        stt_failed_status = GLib.Variant("(ss)", (message, scarlett_sound))
        bus.emit_signal(None,
                        '/org/scarlett/Listener',
                        'org.scarlett.Listener',
                        'SttFailedSignal',
                        stt_failed_status)

    def ListenerCancelSignal(self, message, scarlett_sound):
        logger.debug(" sending message: {}".format(message))
        bus = self.dbus_stack[0]
        listener_cancel_status = GLib.Variant(
            "(ss)", (message, scarlett_sound))
        bus.emit_signal(None,
                        '/org/scarlett/Listener',
                        'org.scarlett.Listener',
                        'ListenerCancelSignal',
                        listener_cancel_status)

    def ListenerReadySignal(self, message, scarlett_sound):
        logger.debug(" sending message: {}".format(message))
        bus = self.dbus_stack[0]
        listener_rdy_status = GLib.Variant("(ss)", (message, scarlett_sound))
        bus.emit_signal(None,
                        '/org/scarlett/Listener',
                        'org.scarlett.Listener',
                        'ListenerReadySignal',
                        listener_rdy_status)

    def ConnectedToListener(self, scarlett_plugin):
        logger.debug(" Client Connected: {}".format(scarlett_plugin))
        bus = self.dbus_stack[0]
        conn_to_lis_status = GLib.Variant("s", scarlett_plugin)
        bus.emit_signal(None,
                        '/org/scarlett/Listener',
                        'org.scarlett.Listener',
                        'ConnectedToListener',
                        conn_to_lis_status)

    #########################################################
    # Scarlett dbus methods in = func args, out = return values
    #########################################################

    def emitKeywordRecognizedSignal(self):
        global SCARLETT_LISTENING
        # you emit signals by calling the signal's skeleton method
        self.KeywordRecognizedSignal(self._status_kw_match, SCARLETT_LISTENING)
        return SCARLETT_LISTENING

    def emitCommandRecognizedSignal(self, command):
        global SCARLETT_RESPONSE
        self.CommandRecognizedSignal(self._status_cmd_match,
                                     SCARLETT_RESPONSE,
                                     command)
        return SCARLETT_RESPONSE

    def emitSttFailedSignal(self):
        global SCARLETT_FAILED
        self.SttFailedSignal(self._status_stt_failed, SCARLETT_FAILED)
        return SCARLETT_FAILED

    def emitListenerCancelSignal(self):
        global SCARLETT_CANCEL
        self.ListenerCancelSignal(self._status_cmd_cancel, SCARLETT_CANCEL)
        return SCARLETT_CANCEL

    def emitListenerReadySignal(self):
        global SCARLETT_LISTENING
        self.ListenerReadySignal(self._status_ready, SCARLETT_LISTENING)
        return SCARLETT_LISTENING

    def emitConnectedToListener(self, scarlett_plugin):
        logger.debug("emitConnectedToListener")
        self.ConnectedToListener(scarlett_plugin)
        return " {} is connected to ScarlettListener".format(scarlett_plugin)

    def emitListenerMessage(self):
        logger.debug("  sending message")
        return self._message

    #########################################################
    # END Scarlett dbus methods
    #########################################################

    #########################################################
    # START Dbus Introspection method calls required
    #########################################################

    def Get(self, interface_name, property_name):
        return self.GetAll(interface_name)[property_name]

    def GetAll(self, interface_name):
        if interface_name == ScarlettListener.LISTENER_IFACE:
            return {
                'CanQuit': GLib.Variant('b', True),
                'Fullscreen': GLib.Variant('b', False),
                'HasTrackList': GLib.Variant('b', True),
                'Identity': GLib.Variant('s', 'Scarlett'),
                'DesktopEntry': GLib.Variant('s', 'scarlett-listener')
            }
        elif interface_name == 'org.freedesktop.DBus.Properties':
            return {}
        elif interface_name == 'org.freedesktop.DBus.Introspectable':
            return {}
        else:
            raise Exception(
                'org.scarlett.ScarlettListener1',
                'This object does not implement the %s interface'
                % interface_name)

    def Set(self, interface_name, property_name, new_value):
        if interface_name == ScarlettListener.LISTENER_IFACE:
            if property_name == 'Fullscreen':
                pass
        else:
            raise Exception(
                'org.scarlett.ScarlettListener1',
                'This object does not implement the %s interface'
                % interface_name)

    def PropertiesChanged(self, interface_name, changed_properties,
                          invalidated_properties):
        self.con.emit_signal(None,
                             '/org/scarlett/Listener',
                             'org.freedesktop.DBus.Properties',
                             'PropertiesChanged',
                             GLib.Variant.new_tuple(GLib.Variant('s', interface_name),
                                                    GLib.Variant('a{sv}', changed_properties),
                                                    GLib.Variant('as', invalidated_properties)))

    def Introspect(self):
        return self.__doc__

    def Quit(self):
        """Removes this object from the DBUS connection and exits."""
        loop.quit()

if __name__ == '__main__':
    # Example of how to use it
    from pydbus import SessionBus
    bus = SessionBus()
    bus.own_name(name='org.scarlett')
    sl = ScarlettListener(bus=bus.con, path='/org/scarlett/Listener')
    loop.run()

    def sigint_handler(*args):
        """Exit on Ctrl+C"""

        # Unregister handler, next Ctrl-C will kill app
        # TODO: figure out if this is really needed or not
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        sl.Quit()

    signal.signal(signal.SIGINT, sigint_handler)
