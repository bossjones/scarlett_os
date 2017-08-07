FROM bossjones/boss-docker-jhbuild-pygobject3:2.1.0
MAINTAINER Malcolm Jones <bossjones@theblacktonystark.com>

# build-arg are acceptable
# eg. docker build --build-arg var=xxx
ARG SCARLETT_ENABLE_SSHD
ARG SCARLETT_ENABLE_DBUS
ARG SCARLETT_BUILD_GNOME
ARG TRAVIS_CI
ARG STOP_AFTER_GOSS_JHBUILD
ARG STOP_AFTER_GOSS_GTK_DEPS
ARG STOP_AFTER_TRAVIS_CI_PYTEST
ARG SKIP_GOSS_TESTS_JHBUILD
ARG SKIP_GOSS_TESTS_GTK_DEPS
ARG SKIP_TRAVIS_CI_PYTEST

# metadata
ARG CONTAINER_VERSION
ARG GIT_BRANCH
ARG GIT_SHA
ARG BUILD_DATE

ENV SCARLETT_ENABLE_SSHD ${SCARLETT_ENABLE_SSHD:-0}
ENV SCARLETT_ENABLE_DBUS ${SCARLETT_ENABLE_DBUS:-'true'}
ENV SCARLETT_BUILD_GNOME ${SCARLETT_BUILD_GNOME:-'false'}
ENV TRAVIS_CI ${TRAVIS_CI:-'true'}
ENV STOP_AFTER_GOSS_JHBUILD ${STOP_AFTER_GOSS_JHBUILD:-'false'}
ENV STOP_AFTER_GOSS_GTK_DEPS ${STOP_AFTER_GOSS_GTK_DEPS:-'false'}
ENV SKIP_GOSS_TESTS_JHBUILD ${SKIP_GOSS_TESTS_JHBUILD:-'false'}
ENV SKIP_GOSS_TESTS_GTK_DEPS ${SKIP_GOSS_TESTS_GTK_DEPS:-'false'}
ENV STOP_AFTER_TRAVIS_CI_PYTEST ${STOP_AFTER_TRAVIS_CI_PYTEST:-'false'}
ENV SKIP_TRAVIS_CI_PYTEST ${SKIP_TRAVIS_CI_PYTEST:-'false'}

ENV WHEELHOUSE=/wheelhouse
ENV PIP_WHEEL_DIR=/wheelhouse
ENV PIP_FIND_LINKS=/wheelhouse

# VOLUME /wheelhouse
# VOLUME /application

COPY ./ /home/pi/dev/bossjones-github/scarlett_os

WORKDIR /home/pi/dev/bossjones-github/scarlett_os

# NOTE: Temp run install as pi user
USER $UNAME

RUN set -x cd /home/pi/dev/bossjones-github/scarlett_os \
    && pwd \
    # FIXME: Shouldn't be necessary anymore after pip > 9.0.1!
    # https://github.com/pypa/setuptools/issues/885
    # https://github.com/pypa/pip/issues/4216
    # ORIG: https://github.com/pradyunsg/pip/archive/hotfix/9.0.2.zip#egg=pip
    # Locking to bossjones fork just in case this changes without use knowing, tested and it works
    && pip install --ignore-installed --pre "https://github.com/pradyunsg/pip/archive/hotfix/9.0.2.zip#egg=pip" \
    && pip install --upgrade setuptools==36.0.1 wheel==0.29.0 wheel \
    && jhbuild run -- pip wheel -r requirements.txt \
    && jhbuild run -- pip freeze \
    && jhbuild run python3 setup.py install \
    && jhbuild run -- pip wheel -e .[test]

# NOTE: Temp run install as pi user
USER root

COPY ./container/root /

# Install stuff required for Sublime3 remote dev
RUN sudo mv -f /dotfiles/.pythonrc /home/pi/.pythonrc && \
    sudo chown pi:pi /home/pi/.pythonrc && \
    sudo mv -f /dotfiles/.pdbrc /home/pi/.pdbrc && \
    sudo chown pi:pi /home/pi/.pdbrc && \
    sudo mv -f /dotfiles/.pdbrc.py /home/pi/.pdbrc.py && \
    sudo chown pi:pi /home/pi/.pdbrc.py && \
    echo "****************[PTPYTHON]****************" && \
    sudo mkdir -p /home/pi/.ptpython && \
    sudo mv -f /dotfiles/.ptpython_config.py /home/pi/.ptpython/config.py && \
    sudo chown pi:pi /home/pi/.ptpython

# ENTRYPOINT ["/docker_entrypoint.sh"]
# CMD true
# ENTRYPOINT ["/.pi_setuid_shm"]
# CMD ["/.pi_setuid_shm", "true"]
CMD ["/bin/bash", "/run.sh"]
