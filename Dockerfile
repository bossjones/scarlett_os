FROM bossjones/boss-docker-jhbuild-pygobject3:2.0.0
MAINTAINER Malcolm Jones <bossjones@theblacktonystark.com>

COPY ./ /home/pi/dev/bossjones-github/scarlett_os

WORKDIR /home/pi/dev/bossjones-github/scarlett_os

RUN sudo apt-get update -yqq && \
    sudo apt-get install dbus dbus-x11 psmisc vim xvfb xclip htop -yqq && \
    sudo apt-get clean && \
    sudo apt-get autoclean -y && \
    sudo apt-get autoremove -y && \
    sudo rm -rf /var/lib/{cache,log}/ && \
    sudo rm -rf /var/lib/apt/lists/*.lz4 /tmp/* /var/tmp/*

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
    && pip install --upgrade setuptools==36.0.1 wheel==0.29.0 \
    && jhbuild run -- pip install -r requirements.txt \
    && jhbuild run -- pip freeze \
    && jhbuild run python3 setup.py install \
    && jhbuild run -- pip install -e .[test]

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
    # && \
    # echo "****************[SUBLIME-ANACONDA]****************" && \
    # sudo chown pi:pi -R /opt/ && \
    # cd /opt/ && \
    # git clone https://github.com/DamnWidget/anaconda.git && \
    # cd anaconda && \
    # git checkout 223cc612b0318262535ac488d1f4b4121c2e8f0d

ENTRYPOINT ["/docker_entrypoint.sh"]
CMD true
