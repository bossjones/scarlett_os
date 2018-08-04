#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ScarlettOS unit tests
"""

# NOTE: A bunch of this was borrowed from Pitivi

import glob
import os
import sys
import unittest


def get_scarlett_os_dir():
    """
    Gets the scarlett_os root directory.

    Example:

    pi@5068ced95719:~/dev/bossjones-github/scarlett_os/tests$ python try.py
    /home/pi/dev/bossjones-github/scarlett_os
    pi@5068ced95719:~/dev/bossjones-github/scarlett_os/tests$

    """
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    scarlett_os_dir = os.path.join(tests_dir, os.path.pardir)
    return os.path.abspath(scarlett_os_dir)


PROJECT_ROOT = get_scarlett_os_dir()


def setup():
    """Sets paths and initializes modules, to be able to run the tests."""
    res = True

    # # Make available to configure.py the top level dir.
    # scarlett_os_dir = get_scarlett_os_dir()
    # sys.path.insert(0, scarlett_os_dir)
    #
    # NOTE: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # SUPER IMPORTANT
    # CONFIGURE RELATES TO A SCRIPT THAT GENERATES Pitivi MAKEFILES ( Since they compile stuff as well )
    # IT IS NOT THE BASIC CONFIGURATION FOR THE APPLICATION
    # IF YOU NEED THAT YOU SHOULD BE LOOKING AT settings.py
    # from scarlett_os import configure
    #
    # # Make available the compiled C code.
    # sys.path.append(configure.BUILDDIR)
    # subproject_paths = os.path.join(configure.BUILDDIR, "subprojects", "gst-transcoder")
    #
    # _prepend_env_paths(LD_LIBRARY_PATH=subproject_paths,
    #                    GST_PLUGIN_PATH=subproject_paths,
    #                    GI_TYPELIB_PATH=subproject_paths,
    #                    GST_PRESET_PATH=[os.path.join(scarlett_os_dir, "data", "videopresets"),
    #                                     os.path.join(scarlett_os_dir, "data", "audiopresets")],
    #                    GST_ENCODING_TARGET_PATH=[os.path.join(scarlett_os_dir, "data", "encoding-profiles")])
    # os.environ.setdefault('SCARLETT_OS_TOP_LEVEL_DIR', scarlett_os_dir)
    #
    # # Make sure the modules are initialized correctly.
    # from scarlett_os import check
    # check.initialize_modules()
    # res = check.check_requirements()
    #
    # from scarlett_os.utils import loggable as log
    # log.init('SCARLETT_OS_DEBUG')

    return res


# TODO: Comment this in after we figure out best way to get some of this working
# if not setup():
#     raise ImportError("Could not setup testsuite")
