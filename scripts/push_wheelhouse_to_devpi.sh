#!/usr/bin/env bash

# source: https://github.com/muccg/docker-devpi

pip wheel --download=packages --wheel-dir=wheelhouse -r requirements.txt
pip wheel --download=packages --wheel-dir=wheelhouse -r requirements_test_all.txt
pip install "devpi-client>=2.3.0" \
&& export HOST_IP=$(ip route| awk '/^default/ {print $3}') \
&& if devpi use http://$HOST_IP:3141>/dev/null; then \
       devpi use http://$HOST_IP:3141/root/public --set-cfg \
    && devpi login root --password=password  \
    && devpi upload --from-dir --formats=* ./wheelhouse; \
else \
    echo "No started devpi container found at http://$HOST_IP:3141"; \
fi
