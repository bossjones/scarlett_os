#!/usr/bin/env bash

if [ '$GSTREAMER' = '1.0'   ]; then sudo add-apt-repository -y ppa:ricotz/testing; fi
if [ '$GSTREAMER' = '1.0'   ]; then sudo add-apt-repository -y ppa:gnome3-team/gnome3; fi
if [ '$GSTREAMER' = '1.0'   ]; then sudo add-apt-repository -y ppa:gnome3-team/gnome3-staging; fi

sudo add-apt-repository -y ppa:pitti/systemd-semaphore
sudo apt-get update -qq

sudo apt-get update -qq
sudo apt-get install -y libz-dev libbz2-dev gstreamer$GSTREAMER-tools libgstreamer$GSTREAMER-dev libgstreamer-plugins-base$GSTREAMER-dev libgstreamer-plugins-bad$GSTREAMER-dev
if [ '$GSTREAMER' = '1.0'   ]; then sudo apt-get install -y libgstreamer-plugins-good$GSTREAMER-dev; fi
sudo apt-get update -qq

sudo apt-get install -y gir1.2-gst-plugins-base-1.0 \
    gir1.2-gstreamer-1.0 graphviz-dev \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad python-gst-1.0

sudo apt-get install -qq python3-gi

sudo apt-get install -qq python-gst-1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    libsndfile1-dev libasound2-dev \
    libgstreamer-plugins-base1.0-dev \
    python-numpy \
    python-scipy
sudo apt-get -y install automake \
    gir1.2-gst-plugins-base-1.0 \
    gir1.2-gstreamer-1.0 \
    gstreamer1.0-libav \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-tools \
    libasound2-dev \
    libgstreamer-plugins-base1.0-dev \
    libsndfile1-dev python \
    python-dev python-gi \
    python-gst-1.0 python-gst-1.0 \
    python-imaging python-lxml \
    python-numpy python-scipy \
    python-virtualenv \
    python3-gi

sudo apt-get -y install libsdl2-dev \
    libsdl2-ttf-dev libsdl2-image-dev \
    libsdl2-mixer-dev gnome-common

sudo apt-get -y install libgstreamer1.0-dev \
    gstreamer1.0-alsa \
    gstreamer1.0-plugins-base

sudo apt-get -y install python-dev \
    libsmpeg-dev libswscale-dev \
    libavformat-dev libavcodec-dev \
    libjpeg-dev libtiff4-dev \
    libX11-dev libmtdev-dev

sudo apt-get -y install python-setuptools \
    build-essential libgl1-mesa-dev \
    libgles2-mesa-dev xvfb pulseaudio

if [ "$TRAVIS_OS_NAME" = "linux" ]; then sudo add-apt-repository 'deb http://us.archive.ubuntu.com/ubuntu/ trusty main restricted universe multiverse'; fi
if [ "$TRAVIS_OS_NAME" = "linux" ]; then sudo add-apt-repository 'deb http://us.archive.ubuntu.com/ubuntu/ trusty-updates main restricted universe multiverse'; fi
if [ "$TRAVIS_OS_NAME" = "linux" ]; then sudo apt-get update -qq; sudo apt-get install -qq pkg-config; fi

sudo apt-get -y update

sudo apt-get -y install ubuntu-restricted-extras

sudo apt-get -y install libfftw3-dev

sudo apt-get install -qq python3-dev python3-cairo-dev \
    python3-gi gnome-common \
    gtk-doc-tools libgtk-3-dev \
    libgirepository1.0-dev libmount-dev \
    cvs

sudo apt-get update -q

sudo apt-get install --no-install-recommends -y xvfb \
    gir1.2-gtk-3.0 \
    $(echo $PACKAGES)

sudo apt-get install -qq \
    git gettext xsltproc \
    docbook-xml docbook-xsl \
    autopoint git-core \
    python-libxml2 byacc wget

sudo apt-get install -qq --no-install-recommends \
    docbook-xsl flex bison cvs gperf cmake valac g++ \
    lib{pam0g,iw,db,gdbm,png12,ffi,tiff,boost-signals,ldap2}-dev \
    lib{vorbis,gl1-mesa,unistring,quvi,icu,neon27,usb-1.0-0,sasl2}-dev \
    lib{asound2,ncurses5,nss3,udev,usb,acl1,polkit-gobject-1,cairo}-dev \
    lib{oauth,nl-route-3,nl-genl-3,cups2,rsvg2,systemd-login}-dev \
    lib{dvdread,soundtouch,wnck-3,avahi-gobject}-dev \
    libtasn1-3-bin \
    libx{cb-util0,composite,randr,damage,ft2,i,t}-dev \
    {uuid,ppp,python-cairo}-dev \
    icc-profiles-free libxml-simple-perl subversion ruby gnome-doc-utils \
    yelp-tools apt-file

# NOTE: jhbuild dependency for sysdeps
sudo apt-get install -qq apt-file
sudo apt-file update

curl -s -q -L 'https://bootstrap.pypa.io/ez_setup.py' > ${HOME}/ez_setup.py
curl -s -q -L 'https://bootstrap.pypa.io/get-pip.py' > ${HOME}/get-pip.py
sudo python3 ${HOME}/ez_setup.py
sudo python3 ${HOME}/get-pip.py
sudo pip3 install virtualenv virtualenvwrapper
sudo pip3 install -I path.py==7.7.1

# jhbuilder and gstreamer need this it seems
sudo pip3 install meson

# virtualenv
export WORKON_HOME=${HOME}/.virtualenvs
export PROJECT_HOME=${HOME}/dev
export VIRTUALENVWRAPPER_PYTHON=`which python3`
export VIRTUALENVWRAPPER_VIRTUALENV=`which virtualenv`
if [ "$TRAVIS_OS_NAME" = "linux" ]; then
    /home/travis/virtualenv/python3.5.2/bin/virtualenvwrapper.sh
else
    source /usr/local/bin/virtualenvwrapper.sh
fi
export PYTHONSTARTUP=$HOME/.pythonrc
export PIP_DOWNLOAD_CACHE=$HOME/.pip/cache

mkdir -p $WORKON_HOME

rmvirtualenv scarlett_os
mkvirtualenv scarlett_os

echo -e "\n[ Write to postactivate ]"
cat << EOF > $HOME/.virtualenvs/scarlett_os/bin/postactivate
# FOR VIRTUALENVS
export GSTREAMER=1.0
export PI_HOME=$HOME
export MAIN_DIR=$HOME/dev/bossjones-github/scarlett_os
export VIRT_ROOT=$HOME/.virtualenvs/scarlett_os
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/dev


# export PKG_CONFIG_PATH=$PI_HOME/.virtualenvs/scarlett_os/lib/pkgconfig
export SCARLETT_CONFIG=$HOME/dev/bossjones-github/scarlett_os/tests/fixtures/.scarlett
export SCARLETT_HMM=$HOME/.virtualenvs/scarlett_os/share/pocketsphinx/model/en-us/en-us
export SCARLETT_LM=$HOME/dev/bossjones-github/scarlett_os/tests/fixtures/lm/1473.lm
export SCARLETT_DICT=$HOME/dev/bossjones-github/scarlett_os/tests/fixtures/dict/1473.dic

# for GST PLUGINS
export LD_LIBRARY_PATH=$HOME/.virtualenvs/scarlett_os/lib
export GST_PLUGIN_PATH=${PREFIX}/lib/gstreamer-$GSTREAMER

export PYTHON=/usr/bin/python3
EOF

echo -e "\n[ Chmod +x postactivate ]"
chmod +x $HOME/.virtualenvs/scarlett_os/bin/postactivate

workon scarlett_os
