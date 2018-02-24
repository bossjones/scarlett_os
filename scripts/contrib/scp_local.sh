#!/usr/bin/env bash

# Scp from vagrant box to local machine

scp -i ~/dev/bossjones/scarlett_os/keys/vagrant_id_rsa -P 2222 \
-o UserKnownHostsFile=/dev/null \
-o StrictHostKeyChecking=no \
pi@127.0.0.1:/home/pi/dev/bossjones-github/scarlett_os/$1 .
