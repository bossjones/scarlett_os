from __future__ import absolute_import, print_function, unicode_literals

import sys
import textwrap


try:
    import gi
    gi.require_version('Gst', '1.0')
    from gi.repository import GLib, GObject, Gst, Gio
    # Initalize for threads
    # NOTE: We might not want to put this here
    Gst.init(None)
    Gst.debug_set_active(True)
    Gst.debug_set_default_threshold(1)
except ImportError:
    print(textwrap.dedent("""
        ERROR: A GObject Python package was not found.

        Mopidy requires GStreamer to work. GStreamer is a C library with a
        number of dependencies itself, and cannot be installed with the regular
        Python tools like pip.

        Please see http://docs.mopidy.com/en/latest/installation/ for
        instructions on how to install the required dependencies.
    """))
    raise
else:
    Gst.init([])
    gi.require_version('GstPbutils', '1.0')
    from gi.repository import GstPbutils


REQUIRED_GST_VERSION = (1, 2, 3)

if Gst.version() < REQUIRED_GST_VERSION:
    sys.exit(
        'ERROR: Mopidy requires GStreamer >= %s, but found %s.' % (
            '.'.join(map(str, REQUIRED_GST_VERSION)), Gst.version_string()))


def _gst_available():
    """Determine whether Gstreamer and the Python GObject bindings are
    installed.
    """
    try:
        import gi
    except ImportError:
        return False

    try:
        gi.require_version('Gst', '1.0')
    except (ValueError, AttributeError):
        return False

    try:
        from gi.repository import Gst  # noqa
    except ImportError:
        return False

    return True


__all__ = [
    'GLib',
    'GObject',
    'Gst',
    'GstPbutils',
    'gi',
    'Gio'
]
