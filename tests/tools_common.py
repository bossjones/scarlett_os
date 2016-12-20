"""Generic testing utility tools."""

import tempfile
import contextlib

# source: Timeside
def tmp_file_sink(prefix=None, suffix=None):
    tmpfile = tempfile.NamedTemporaryFile(delete=True,
                                          prefix=prefix,
                                          suffix=suffix)
    tmpfile.close()
    return tmpfile.name


@contextlib.contextmanager
def monkeypatched(object, name, patch):
    """Temporarily monkeypatches an object."""
    # source: https://gist.github.com/rectangletangle/0a0d5a2e84dd3178d348
    # This is a convenient way to monkeypatch a method or attribute of a Python
    # object. This is great for situations where you want to modify a global
    # object within a limited scope, i.e., your typical class or module when
    # testing. This was tested and works with Python 2.7 and 3.4.

    pre_patched_value = getattr(object, name)
    setattr(object, name, patch)
    yield object
    setattr(object, name, pre_patched_value)
