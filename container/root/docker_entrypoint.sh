#!/bin/bash

set -e

sudo find \( -name __pycache__ -o -name '*.pyc' \) | sudo xargs rm -rf
sudo chown pi:pi -R /home/pi/dev

exec "$@"
