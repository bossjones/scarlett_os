#!/bin/bash

set -e

# if [ ! -f /virtualenv/bin/activate ]; then
#     virtualenv /virtualenv -p python${INSPIRE_PYTHON_VERSION}
#     source /virtualenv/bin/activate
#     pip install --upgrade pip setuptools wheel
#     cp -r /src-cache /virtualenv/src
# else
#     source /virtualenv/bin/activate
# fi

sudo find \( -name __pycache__ -o -name '*.pyc' \) | sudo xargs rm -rf
sudo chown pi:pi -R /home/pi/dev

exec "$@"
