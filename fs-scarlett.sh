#!/usr/bin/env bash

fswatch -o . -e .git | xargs -n1 -I{} rsync -avz -e \
   "ssh -i /Users/malcolm/dev/bossjones/scarlett_os/keys/vagrant_id_rsa \
   -p 2222 -o UserKnownHostsFile=/dev/null \
   -o StrictHostKeyChecking=no" \
   --port 2222 \
   --exclude *.pyc \
   --exclude *.git \
   --exclude *.vagrant \
   --exclude *.vendor \
   --exclude .Python --exclude env/ \
   --exclude build/ --exclude develop-eggs/ \
   --exclude dist/ --exclude downloads/ \
   --exclude eggs/ --exclude .eggs/ \
   --exclude lib/ --exclude lib64/ \
   --exclude parts/ --exclude sdist/ \
   --exclude var/ --exclude *.egg-info/ \
   --exclude *.__pycache__/ \
   --exclude *__pycache__/ \
   --exclude *.swp \
   --exclude *.tox \
   --exclude .installed.cfg --exclude *.egg \
   . pi@127.0.0.1:/home/pi/dev/bossjones-github/scarlett_os/
