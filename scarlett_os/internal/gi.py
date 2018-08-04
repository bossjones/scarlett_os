# NOTE: from __future__ import absolute_import means that if you import
# string, Python will always look for a top - level string module, rather
# than current_package.string. However, it does not affect the logic
# Python uses to decide what file is the string module. When you do  #
# pylint: disable=C0301,W0511
from __future__ import absolute_import, print_function, unicode_literals

# NOTE: On Python 3 there is currently no support for bytes, see bug 746564 for more details.
# NOTE: On Python 3 there is currently no support for bytes, see bug 746564 for more details.
# NOTE: On Python 3 there is currently no support for bytes, see bug 746564 for more details.
# https://pygobject.readthedocs.io/en/latest/guide/api/basic_types.html

import sys
import textwrap


try:
    import gi

    gi.require_version("GLib", "2.0")
    gi.require_version("Gst", "1.0")
    from gi.repository import GLib
    from gi.repository import GObject
    from gi.repository import Gst
    from gi.repository import Gio

    # FIXME: enable this 3/6/2018 !!!
    # SOURCE: https://gitlab.gnome.org/GNOME/gnome-builder/blob/master/src/plugins/jedi/jedi_plugin.py#L100
    # gi.require_version('GIRepository', '2.0')
    # gi.require_version('Gtk', '3.0')
    # gi.require_version('GtkSource', '3.0')
    # gi.require_version('Ide', '1.0')

    # Initalize for threads
    # NOTE: We might not want to put this here

    # SOURCE: https://stackoverflow.com/questions/43777428/capture-gstreamer-network-video-with-python
    # Enable this so we can pass in commandline arguments
    # Gst.init(sys.argv)
    # NOTE: Set this env var below to catch errors
    # G_DEBUG=fatal_warnings
    # Gst.init(['--gst-disable-segtrap',
    #           '--gst-disable-registry-fork', '--gst-debug-level=5'])
    ##########################################################################
    # pi@scarlett-ansible-manual1604-2  ⓔ scarlett_os  ⎇  master S:2 U:23 ?:120  ~/dev/bossjones-github/scarlett_os  jhbuild run -- gst-inspect-1.0 --help-gst
    # Usage:
    # gst-inspect-1.0 [OPTION...] [ELEMENT-NAME | PLUGIN-NAME]
    # GStreamer Options
    # --gst-version                        Print the GStreamer version
    # --gst-fatal-warnings                 Make all warnings fatal
    # --gst-debug-help                     Print available debug categories and exit
    # --gst-debug-level=LEVEL              Default debug level from 1 (only error) to 9 (anything) or 0 for no output
    # --gst-debug=LIST                     Comma-separated list of category_name:level pairs to set specificlevels for the individual categories. Example: GST_AUTOPLUG:5,GST_ELEMENT_*:3
    # --gst-debug-no-color                 Disable colored debugging output
    # --gst-debug-color-mode               Changes coloring mode of the debug log. Possible modes: off, on, disable, auto, unix
    # --gst-debug-disable                  Disable debugging
    # --gst-plugin-spew                    Enable verbose plugin loading diagnostics
    # --gst-plugin-path=PATHS              Colon-separated paths containing plugins
    # --gst-plugin-load=PLUGINS            Comma-separated list of plugins to preload in addition to the list stored in environment variable GST_PLUGIN_PATH
    # --gst-disable-segtrap                Disable trapping of segmentation faults during plugin loading
    # --gst-disable-registry-update        Disable updating the registry
    # --gst-disable-registry-fork          Disable spawning a helper process while scanning the registry
    ##########################################################################
    Gst.init(None)
    Gst.debug_set_active(True)
    Gst.debug_set_default_threshold(1)
except ImportError:
    print(
        textwrap.dedent(
            """
        ERROR: A GObject Python package was not found.

        Mopidy requires GStreamer to work. GStreamer is a C library with a
        number of dependencies itself, and cannot be installed with the regular
        Python tools like pip.

        Please see http://docs.mopidy.com/en/latest/installation/ for
        instructions on how to install the required dependencies.
    """
        )
    )
    raise
else:
    Gst.init([])
    gi.require_version("GstPbutils", "1.0")
    from gi.repository import GstPbutils

# SOURCE: https://github.com/mopidy/mopidy/blob/6e9cb3b9cafd5909e8271a44b8dd04a8441e638d/mopidy/internal/gi.py
# GLib.set_prgname('mopidy')
# GLib.set_application_name('Mopidy')

REQUIRED_GST_VERSION = (1, 2, 3)

if Gst.version() < REQUIRED_GST_VERSION:
    sys.exit(
        "ERROR: ScarlettOS requires GStreamer >= %s, but found %s."
        % (".".join(map(str, REQUIRED_GST_VERSION)), Gst.version_string())
    )


def _gst_available():
    """Determine whether Gstreamer and the Python GObject bindings are
    installed.
    """
    try:
        import gi
    except ImportError:
        return False

    try:
        gi.require_version("Gst", "1.0")
    except (ValueError, AttributeError):
        return False

    try:
        # pylint: disable=W0612
        from gi.repository import Gst  # noqa
    except ImportError:
        return False

    return True


__all__ = ["GLib", "GObject", "Gst", "GstPbutils", "gi", "Gio"]
