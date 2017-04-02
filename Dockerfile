FROM  bossjones/boss-docker-jhbuild-pygobject3:v1.1
MAINTAINER Malcolm Jones <bossjones@theblacktonystark.com>

COPY ./ /home/pi/dev/bossjones-github/scarlett_os

WORKDIR /home/pi/dev/bossjones-github/scarlett_os

RUN sudo apt-get update -yqq && \
    sudo apt-get install dbus dbus-x11 psmisc vim xvfb xclip -yqq && \
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

# Install stuff required for Sublime3 remote dev
RUN sudo mv -f /dotfiles/.pythonrc /home/pi/.pythonrc && \
    sudo chown pi:pi /home/pi/.pythonrc && \
    sudo mv -f /dotfiles/.pdbrc /home/pi/.pdbrc && \
    sudo chown pi:pi /home/pi/.pdbrc && \
    sudo mv -f /dotfiles/.pdbrc.py /home/pi/.pdbrc.py && \
    sudo chown pi:pi /home/pi/.pdbrc.py && \
    echo "****************[SUBLIME-ANACONDA]****************" && \
    sudo chown pi:pi -R /opt/ && \
    cd /opt/ && \
    git clone https://github.com/DamnWidget/anaconda.git && \
    cd anaconda && \
    git checkout 223cc612b0318262535ac488d1f4b4121c2e8f0d

# RUN sudo
# 223cc612b0318262535ac488d1f4b4121c2e8f0d

ENTRYPOINT ["/docker_entrypoint.sh"]
CMD true
