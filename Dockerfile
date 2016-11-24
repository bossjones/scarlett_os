FROM  bossjones/boss-docker-jhbuild-pygobject3:v1
MAINTAINER Malcolm Jones <bossjones@theblacktonystark.com>

COPY ./ /home/pi/dev/bossjones-github/scarlett_os

WORKDIR /home/pi/dev/bossjones-github/scarlett_os

RUN sudo apt-get update -yqq && \
    sudo apt-get install dbus psmisc -yqq && \
    sudo apt-get clean && \
    sudo apt-get autoclean -y && \
    sudo apt-get autoremove -y && \
    sudo rm -rf /var/lib/{cache,log}/ && \
    sudo rm -rf /var/lib/apt/lists/*.lz4 /tmp/* /var/tmp/*

RUN set -x cd /home/pi/dev/bossjones-github/scarlett_os \
    && pwd \
    && jhbuild run -- pip install -r requirements.txt \
    && jhbuild run python3 setup.py install \
    && jhbuild run -- pip install -e .[test]

COPY ./container/root /

ENTRYPOINT ["/docker_entrypoint.sh"]
CMD true
