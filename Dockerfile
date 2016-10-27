FROM  bossjones/boss-docker-jhbuild-pygobject3:v1
MAINTAINER Malcolm Jones <bossjones@theblacktonystark.com>

COPY ./ /home/pi/dev/bossjones-github/scarlett_os

WORKDIR /home/pi/dev/bossjones-github/scarlett_os

RUN set -x cd /home/pi/dev/bossjones-github/scarlett_os \
    && pwd \
    && jhbuild run python3 setup.py install \
    && jhbuild run -- pip install -e .[test] \
    && jhbuild run -- coverage run -- setup.py test \
    && jhbuild run -- pip install coveralls \
    && sudo chmod 777 /home/pi/dev/bossjones-github/scarlett_os

COPY ./container/root /

# RUN sudo touch .coverage

ENTRYPOINT ["/docker_entrypoint.sh"]
CMD true
