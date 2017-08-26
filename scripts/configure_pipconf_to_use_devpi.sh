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
