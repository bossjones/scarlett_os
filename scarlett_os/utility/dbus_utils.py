# -*- coding: utf-8 -*-
from __future__ import print_function


def convert_complex_type(subsig):  # pragma: no cover
    result = None
    len_consumed = 0

    c = subsig[0]

    c_lookahead = ""
    try:
        c_lookahead = subsig[1]
    except:
        c_lookahead = ""

    if c == "a" and c_lookahead == "{":  # handle dicts as a special case array
        ss = subsig[2:]
        # account for the trailing '}'
        len_consumed = 3
        c = ss[0]
        key = convert_simple_type(c)

        ss = ss[1:]

        (r, lc) = convert_complex_type(ss)
        if r:
            subtypelist = [key]
            for item in r:
                subtypelist.append(item)

            len_consumed += lc + 1
        else:
            value = convert_simple_type(ss[0])
            subtypelist = [key, value]
            len_consumed += 1

        result = ["Dict of {", subtypelist, "}"]

    elif c == "a":  # handle an array
        ss = subsig[1:]
        (r, lc) = convert_complex_type(ss)
        if r:
            subtypelist = r
            len_consumed = lc + 1
        else:
            subtypelist = sig_to_type_list(ss[0])
            len_consumed = 1

        result = ["Array of [", subtypelist, "]"]
    elif c == "(":  # handle structs
        # iterate over sig until paren_count == 0
        paren_count = 1
        i = 0
        ss = subsig[1:]
        len_ss = len(ss)
        while i < len_ss and paren_count != 0:
            if ss[i] == "(":
                paren_count += 1
            elif ss[i] == ")":
                paren_count -= 1

            i += 1

        len_consumed = i
        ss = ss[0 : i - 1]
        result = ["Struct of (", sig_to_type_list(ss), ")"]

    return (result, len_consumed)


def convert_simple_type(c):  # pragma: no cover
    result = None

    if c == "n":
        result = "Int16"
    elif c == "q":
        result = "UInt16"
    elif c == "i":
        result = "Int32"
    elif c == "u":
        result = "UInt32"
    elif c == "x":
        result = "Int64"
    elif c == "t":
        result = "UInt64"
    elif c == "s":
        result = "String"
    elif c == "b":
        result = "Boolean"
    elif c == "y":
        result = "Byte"
    elif c == "o":
        result = "Object Path"
    elif c == "g":
        result = "Signature"
    elif c == "d":
        result = "Double"
    elif c == "v":
        result = "Variant"

    return result


def sig_to_type_list(sig):  # pragma: no cover
    i = 0
    result = []

    sig_len = len(sig)
    while i < sig_len:
        c = sig[i]
        type_ = convert_simple_type(c)
        if not type_:
            (type_, len_consumed) = convert_complex_type(sig[i:])
            if not type_:
                type_ = "Error(" + c + ")"

            i += len_consumed

        if isinstance(type_, list):
            for item in type_:
                result.append(item)
        else:
            result.append(type_)

        i += 1

    return result


def type_list_to_string(type_list):  # pragma: no cover
    result = ""
    add_cap = False

    for dbus_type in type_list:
        if isinstance(dbus_type, list):
            result += type_list_to_string(dbus_type)
            add_cap = True
        else:
            # we get rid of the leading comma later
            if not add_cap:
                result += ", "
            else:
                add_cap = False

            try:
                result += dbus_type
            except:
                print(type_list)

    return result[2:]


def sig_to_markup(sig, span_attr_str):  # pragma: no cover
    list_ = sig_to_type_list(sig)
    markedup_list = []
    m = "<span " + span_attr_str + ">"
    m += type_list_to_string(list_)
    m += "</span>"

    return m


def sig_to_string(sig):  # pragma: no cover
    return type_list_to_string(sig_to_type_list(sig))


class DbusSignalHandler(object):
    """Helper for tracking dbus signal registrations"""

    def __init__(self):
        self._ids = {}

    def connect(self, bus, dbus_signal, func, *args):
        """Connect a function + args to dbus_signal dbus_signal on an bus.

        Each dbus_signal may only be handled by one callback in this implementation.

        Args:
            `bus` (pydbus.bus.Bus): Pydbus DBus object to talk to Scarlett Mpris service.
            `dbus_signal` (ListenerReadySignal,
                           SttFailedSignal,
                           KeywordRecognizedSignal,
                           CommandRecognizedSignal,
                           ListenerCancelSignal,
                           ConnectedToListener): The type of dbus signal to subscribe to.
            `func` (callable): callback function
            `*args` (extra arguments): Extra arguments required for callback functions
        """

        assert (bus, dbus_signal) not in self._ids
        self._ids[(bus, dbus_signal)] = bus.subscribe(
            sender=None,
            iface="org.scarlett.Listener",
            signal=dbus_signal,
            object="/org/scarlett/Listener",
            arg0=None,
            flags=0,
            signal_fired=func,
        )

    def disconnect(self, bus, dbus_signal):
        """Disconnect whatever handler we have for an bus+dbus_signal pair.

        Does nothing it the handler has already been removed.
        """
        signal_id = self._ids.pop((bus, dbus_signal), None)
        if signal_id is not None:
            signal_id.disconnect()

    def clear(self):
        """Clear all registered signal handlers."""
        # NOTE: How to avoid “RuntimeError: dictionary changed size during iteration” error?
        # source: http://stackoverflow.com/questions/11941817/how-to-avoid-runtimeerror-dictionary-changed-size-during-iteration-error
        # HINT: use list()
        for bus, dbus_signal in list(self._ids):
            signal_id = self._ids.pop((bus, dbus_signal))
            signal_id.disconnect()
