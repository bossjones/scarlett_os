#!/usr/bin/env python  # NOQA
# -*- coding: utf-8 -*-

# source: http://stackoverflow.com/questions/16981921/relative-imports-in-python-3

"""Scarlett User Module."""

import os
import getpass


def get_user_name(override=None):
    """Return name of current user, eg 'pi' or 'developer'.

    Keyword Arguments:
        override {[string]} -- [description] (default: {None})

    Returns:
        [string] -- [user name]
    """
    if override:
        return override
    else:
        return getpass.getuser()


def get_user_home(override=None):
    """Return user home directory, eg. '/home/pi'

    Keyword Arguments:
        override {[string]} -- [full path to user home] (default: {None})

    Returns:
        [string] -- [user home]
    """
    if override:
        return override
    else:
        return os.path.expanduser("~")


def get_user_project_root_path(override=None):
    """Return path to where all git packages go on your system, eg. /home/pi/dev

    Keyword Arguments:
        override {[string]} -- [full path to folder containing git projects] (default: {None})

    Returns:
        [string] -- [path to git projects]
    """
    if override:
        return override
    else:
        return os.path.join(get_user_home(), "dev")


def get_user_project_base_path(override=None):
    """Return path to where scarlet_os folder is located, eg /home/pi/dev/bossjones-github/scarlett_os

    Keyword Arguments:
        override {[string]} -- [full path to folder containing scarlett_os project] (default: {None})

    Returns:
        [string] -- [full path to folder containing scarlett_os project]
    """
    if override:
        return override
    else:
        return os.path.join(
            get_user_project_root_path() + "/bossjones-github", "scarlett_os"
        )
