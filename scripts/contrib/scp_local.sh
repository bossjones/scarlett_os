#!/usr/bin/env bash

set -x

if [[ "${SCARLETT_SCP_RECURSIVE}" == "1" ]]; then
    _SCP_RECURSIVE="-r"
else
    _SCP_RECURSIVE=""
fi

# Scp from vagrant box to local machine

scp -i ~/dev/bossjones/scarlett_os/keys/vagrant_id_rsa -P 2222 \
-o UserKnownHostsFile=/dev/null \
-o StrictHostKeyChecking=no \
${_SCP_RECURSIVE} \
pi@127.0.0.1:/home/pi/dev/bossjones-github/scarlett_os/$1 .
