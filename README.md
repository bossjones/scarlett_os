ScarlettOS
==========

S.C.A.R.L.E.T.T is Tony Darks artificially programmed intelligent computer. She is programmed to speak with a female voice in a British accent.

[![Build Status](https://travis-ci.org/bossjones/scarlett_os.svg?branch=master)](https://travis-ci.org/bossjones/scarlett_os)
[![Coverage Status](https://coveralls.io/repos/github/bossjones/scarlett_os/badge.svg?branch=master)](https://coveralls.io/github/bossjones/scarlett_os?branch=master)
[![GitHub release](https://img.shields.io/github/release/bossjones/scarlett_os.svg)]()
[![Docker Stars](https://img.shields.io/docker/stars/bossjones/scarlett_os.svg)](https://hub.docker.com/r/bossjones/scarlett_os/)
[![Docker Pulls](https://img.shields.io/docker/pulls/bossjones/scarlett_os.svg)](https://hub.docker.com/r/bossjones/scarlett_os/)
[![Contribution Guidelines](http://img.shields.io/badge/CONTRIBUTING-Guidelines-blue.svg)](./CONTRIBUTING.md)
[![LICENSE](https://img.shields.io/badge/license-Apache-blue.svg?style=flat-square)](./LICENSE)

ScarlettOS Docker Image ([Dockerfile](https://github.com/bossjones/scarlett_os))
================================================================================

[![image6](https://images.microbadger.com/badges/image/bossjones/scarlett_os.svg)](https://microbadger.com/images/bossjones/scarlett_os)
[![image7](https://images.microbadger.com/badges/version/bossjones/scarlett_os.svg)](https://microbadger.com/images/bossjones/scarlett_os)
[![image8](https://images.microbadger.com/badges/commit/bossjones/scarlett_os.svg)](https://microbadger.com/images/bossjones/scarlett_os)
[![image9](https://images.microbadger.com/badges/license/bossjones/scarlett_os.svg)](https://microbadger.com/images/bossjones/scarlett_os)

1.  Free software: Apache 2.0
2.  Documentation: <https://scarlett-os.readthedocs.io>.

\# Features
-----------

1.  TODO

Credits
-------

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.

INSTALL
-------

-   Fill this out soon


Development
----------

Interactive bash: `docker exec -it scarlettos_master_1 bash -l`

```
|2.2.3|  using virtualenv: scarlett-os-venv2  Malcolms-MBP-3 in ~/dev/bossjones/scarlett_os
± |feature-dev-container {5} U:1 ✗| → docker exec -it scarlettos_master_1 bash -l
pi  ⎇  feature-dev-container {5} U:1  ~/dev/bossjones-github/scarlett_os
```


## Debugging in VSCode

**Source: https://github.com/mikemcgowan/django-cms-plus/blob/57e3fa8ec35d73cdd937baac25f5201ec78bbdb9/README.md**

VSCode debug launch configuration:

```json
{
    "name": "Attach (Remote Debug)",
    "type": "python",
    "request": "attach",
    "localRoot": "${workspaceRoot}",
    "remoteRoot": "",
    "port": 2222,
    "secret": "my_secret",
    "host": "localhost"
}
```

Ensure the following exists in `web/manage.py` immediately before `execute_from_command_line()`:

```python
# https://stackoverflow.com/questions/41201438/debug-python-application-running-in-docker
try:
    import ptvsd
    ptvsd.enable_attach(secret='my_secret', address=('0.0.0.0', 2222))
except (OSError, ImportError):
    pass
```

### Gstreamer Environment Variables

Official docs: https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gstreamer/html/gst-running.html

Variable | Example | Description
--- | --- | ---
`GST_PLUGIN_SYSTEM_PATH` | `GST_PLUGIN_SYSTEM_PATH=/usr/local/lib/gstreamer-1.0` | GStreamer will scan these paths for GStreamer plug-ins. These plug-ins will be loaded after the plug-ins in the GST_PLUGIN_PATH variable below.
`GST_DEBUG` | `GST_DEBUG=GST_AUTOPLUG:6,GST_ELEMENT_*:4` | This variable can be set to a list of debug options, which cause GStreamer to print out different types of debugging information to stderr. The variable takes a comma-separated list of "category_name:level" pairs to set specific levels for the individual categories. The level value ranges from 0 (nothing) to 9 .
`GST_DEBUG_DUMP_DOT_DIR` | `GST_DEBUG_DUMP_DOT_DIR=/tmp` | Set this environment variable to a path to turn on all #GST_DEBUG_BIN_TO_DOT_FILE or #GST_DEBUG_BIN_TO_DOT_FILE_WITH_TS calls and have the dot files in that location. This will only work if the application in question makes these calls in strategic places (like when the pipeline state changes or an error occurs)
`GST_REGISTRY_UPDATE` | `GST_REGISTRY_UPDATE=no` | Set this environment variable to "no" to prevent GStreamer from updating the plugin registry. This is useful for embedded device which is not updating the plugins frequently, it will save time when doing gst_init().
`G_DEBUG` | `G_DEBUG=fatal_warnings` | Useful GLib environment variable. Set G_DEBUG=fatal_warnings to make GStreamer programs abort when a critical warning such as an assertion failure occurs. This is useful if you want to find out which part of the code caused that warning to be triggered and under what circumstances. Simply set G_DEBUG as mentioned above and run the program in gdb (or let it core dump). Then get a stack trace in the usual way.
