#!/usr/bin/env python  # NOQA
# -*- coding: utf-8 -*-

# source: http://code.activestate.com/recipes/327082-pseudo-threads-with-generators-and-pygtkgnome-pyth/

# vim:sw=4:et:
"""
Scarlett Observable module.

Attempt to implement the observable pattern to solve weird race conditions between
Listener, Tasker, Player, Speaker during keyword matches.

https://sourcemaking.com/files/v2/content/patterns/Observer_example1.png
"""

import threading
from scarlett_os.internal.gi import gi
from scarlett_os.internal.gi import GObject
from scarlett_os.internal.gi import GLib

# TODO, Get this working with a KeyWord Match object


# SOURCE: https://github.com/ReapOmen/open-media/blob/1ac6be3e50e66df65ef37fa91e090739db041fb1/openmedia/observable/observable.py

class Observable(object):
    """Aka Subject, eg Auctioneer."""

    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, info):
        for obs in self._observers:
            event = threading.Event()
            GLib.idle_add(obs.update, event, info)


class Observer(object):
    """Aka Bidder in a auction. This class watches the Auctioneer and reacts to events."""

    def __init__(self):
        pass

    def update(self, event, info):
        return False


# class Counter(object):
#     def __init__(self, start = 0):
#         self.lock = threading.Lock()
#         self.value = start
#     def increment(self):
#         logging.debug('Waiting for a lock')
#         self.lock.acquire()
#         try:
#             logging.debug('Acquired a lock')
#             self.value = self.value + 1
#         finally:
#             logging.debug('Released a lock')
#             self.lock.release()
