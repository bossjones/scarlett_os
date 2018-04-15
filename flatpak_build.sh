#!/usr/bin/env bash

source /home/developer/.bashrc

pyenv version 3.5.2;
mkdir -p /app/lib/python3.5/site-packages;
CFLAGS='-L/usr/lib -Lbuild/temp.linux-x86_64-3.4 -I/usr/include -I/usr/include/python3.5m/' CXX=/usr/bin/g++ CC=/usr/bin/gcc PYTHONUSERBASE=/app/ pip3.5 install --target=/app --root=/ -r requirements.txt;
CFLAGS='-L/usr/lib -Lbuild/temp.linux-x86_64-3.4 -I/usr/include -I/usr/include/python3.5m/' CXX=/usr/bin/g++ CC=/usr/bin/gcc PYTHONUSERBASE=/app/ pip3.5 install --target=/app --root=/ -r requirements_dev.txt;
CFLAGS='-L/usr/lib -Lbuild/temp.linux-x86_64-3.4 -I/usr/include -I/usr/include/python3.5m/' CXX=/usr/bin/g++ CC=/usr/bin/gcc PYTHONUSERBASE=/app/ python3.5 setup.py install --prefix=/app --root=/;
CFLAGS='-L/usr/lib -Lbuild/temp.linux-x86_64-3.4 -I/usr/include -I/usr/include/python3.5m/' CXX=/usr/bin/g++ CC=/usr/bin/gcc PYTHONUSERBASE=/app/ pip3.5 install --target=/app --root=/ -e .[test];
