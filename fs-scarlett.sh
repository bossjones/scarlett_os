#!/usr/bin/env bash

fswatch -o . -e .git | xargs -n1 -I{} rsync -avz -e \
   "ssh -i /Users/malcolm/dev/bossjones/scarlett_os/keys/vagrant_id_rsa \
   -p 2222 -o UserKnownHostsFile=/dev/null \
   -o StrictHostKeyChecking=no" \
   --port 2222 \
   --exclude *.__pycache__/ \
   --exclude *.cache \
   --exclude *.egg \
   --exclude *.egg-info/ \
   --exclude *.git \
   --exclude *.pyc \
   --exclude *.swp \
   --exclude *.tox \
   --exclude *.vagrant \
   --exclude *.vendor \
   --exclude *__pycache__/ \
   --exclude .Python \
   --exclude .coverage \
   --exclude *.coverage \
   --exclude .eggs/ \
   --exclude .installed.cfg \
   --exclude .vscode/ \
   --exclude _debug/ \
   --exclude build/ \
   --exclude cov.xml \
   --exclude cov_annotate/ \
   --exclude develop-eggs/ \
   --exclude dist/ \
   --exclude downloads/ \
   --exclude gir-1.0/ \
   --exclude *.gir-1.0/ \
   --exclude eggs/ \
   --exclude env/ \
   --exclude espeak_tmp.wav/ \
   --exclude *espeak_tmp.wav/ \
   --exclude htmlcov/ \
   --exclude lib/ \
   --exclude lib64/ \
   --exclude parts/ \
   --exclude sdist/ \
   --exclude var/ \
   --exclude fakegir/ \
   --exclude *.py*.py \
   --exclude .pytest_cache/ \
   . pi@127.0.0.1:/home/pi/dev/bossjones-github/scarlett_os/
