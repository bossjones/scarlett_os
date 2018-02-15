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
