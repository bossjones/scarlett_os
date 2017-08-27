#!/usr/bin/env bash

# Use an optional pip cache to speed development
export HOST_IP=$(ip route| awk '/^default/ {print $3}') \
&& mkdir -p ~/.pip \
&& > ~/.pip/pip.conf \
&& echo [global] >> ~/.pip/pip.conf \
&& echo extra-index-url = http://$HOST_IP:3141/app/dev/+simple >> ~/.pip/pip.conf \
&& echo [install] >> ~/.pip/pip.conf \
&& echo trusted-host = $HOST_IP >> ~/.pip/pip.conf \
&& cat ~/.pip/pip.conf


echo "if it's working you will see out put including:"
echo "2 location(s) to search for versions of ignoredd:"
echo "* https://pypi.python.org/simple/ignoredd/"
echo "* http://172.17.0.1:3141/app/dev/+simple/ignoredd/"

pip install -v ignoredd
