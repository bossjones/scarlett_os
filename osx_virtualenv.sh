#!/usr/bin/env bash

brew reinstall gtk+3
brew reinstall gst-plugins-base gst-plugins-bad gst-plugins-ugly gst-plugins-good
brew reinstall gsed

export PYTHON_VERSION=3.5
export GSTREAMER=1.0
export PI_HOME=~/
export MAIN_DIR="${PI_HOME}/dev/bossjones/scarlett_os"
export VIRT_ROOT="${PI_HOME}/.virtualenvs/scarlett_os"
export PKG_CONFIG_PATH="${PI_HOME}/.virtualenvs/scarlett_os/lib/pkgconfig"
export SCARLETT_CONFIG="${PI_HOME}/dev/bossjones/scarlett_os/tests/fixtures/.scarlett"
export SCARLETT_HMM="${PI_HOME}/dev/bossjones/scarlett_os/.virtualenvs/scarlett_os/share/pocketsphinx/model/en-us/en-us"
export SCARLETT_LM="${PI_HOME}/dev/bossjones/scarlett_os/tests/fixtures/lm/1473.lm"
export SCARLETT_DICT="${PI_HOME}/dev/bossjones/scarlett_os/tests/fixtures/dict/1473.dic"

# for GST PLUGINS
export LD_LIBRARY_PATH="${PI_HOME}/.virtualenvs/scarlett_os/lib"
export GST_PLUGIN_PATH="${PI_HOME}/.virtualenvs/scarlett_os/lib/gstreamer-${GSTREAMER}"

export PYTHON=/usr/local/bin/python3
export PYTHON_VERSION='3.5'

mkvirtualenv --python=/usr/local/bin/python3 scarlett-os-venv2

###########################################
# pycairo
###########################################

cd $MAIN_DIR
curl -L https://cairographics.org/releases/pycairo-1.10.0.tar.bz2 | tar xj
cd pycairo-1.10.0
export ARCHFLAGS='-arch x86_64'

python waf configure --prefix=$VIRTUAL_ENV # It's ok, this will fail.
gsed -i '' '154s/data={}/return/' .waf3-1.6.4-*/waflib/Build.py # Bufix: https://bugs.freedesktop.org/show_bug.cgi?id=76759
python waf configure --prefix=$VIRTUAL_ENV # Now it should configure.
python waf build
python waf install

unset ARCHFLAGS
cd -

###########################################
# pygobject3
###########################################

export PKG_CONFIG_PATH=$VIRTUAL_ENV/lib/pkgconfig:/usr/local/opt/libffi/lib/pkgconfig

curl -L http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.20/pygobject-3.20.1.tar.xz | tar xJ
cd pygobject-3.20.1

./configure CFLAGS="-I$VIRTUAL_ENV/include" --prefix=$VIRTUAL_ENV
make
make install

cd -

###########################################
# pygobject3
###########################################

# source: http://pujansrt.blogspot.com/2010/03/gstreamer-install-on-mac-osx.html
# LDFLAGS="-L/usr/local/lib -L/opt/local/lib" CFLAGS="-I/usr/local/include -I/opt/local/include"  \
# PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:/opt/local/lib/pkgconfig" \
# ./configure --prefix=/usr/local && make DEPRECATED_CFLAGS="" && sudo make install
#
# LDFLAGS="-L/usr/local/lib -L/opt/local/lib" CFLAGS="-I/usr/local/include -I/opt/local/include"  \
# PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:/opt/local/lib/pkgconfig"  \
# ./configure --prefix=/usr/local --disable-mmx && make DEPRECATED_CFLAGS="" && sudo make install

# compile pulseaudio
# compile espeak

#############################################
# portaudio compile
#############################################

git clone https://github.com/bossjones/espeakosx ~/dev/bossjones/espeakosx
cd $MAIN_DIR
curl -L "http://www.portaudio.com/archives/pa_stable_v19_20140130.tgz" > pa.tgz
tar xzf pa.tgz
cd portaudio
patch -i ~/dev/bossjones/espeakosx/portaudio_configure_sdk.patch
./configure  --prefix=$VIRT_ROOT
make


cd $MAIN_DIR
curl -L "http://sourceforge.net/projects/espeak/files/espeak/espeak-1.48/espeak-1.48.04-source.zip" > ess.zip
unzip ess.zip
cd espeak-1.48.04-source/src
patch Makefile ~/dev/bossjones/espeakosx/Makefile.patch
patch event.cpp ~/dev/bossjones/espeakosx/event.cpp.patch
patch fifo.cpp ~/dev/bossjones/espeakosx/fifo.cpp.patch
cp $MAIN_DIR/portaudio/lib/.libs/libportaudio.a .
cp $MAIN_DIR/portaudio/include/portaudio.h .
make

# CURRENT_DIR=`pwd`
# DIR="/tmp/espeakosx"
# INNER_SRC_DIR="espeak-1.48.04-source/src"


cd $MAIN_DIR && \
curl -L "https://github.com/bossjones/bossjones-gst-plugins-espeak-0-4-0/archive/v0.4.1.tar.gz" > gst-plugins-espeak-0.4.0.tar.gz && \
tar xvf gst-plugins-espeak-0.4.0.tar.gz && \
rm -rfv gst-plugins-espeak-0.4.0 && \
mv -fv bossjones-gst-plugins-espeak-0-4-0-0.4.1 gst-plugins-espeak-0.4.0 && \
cd gst-plugins-espeak-0.4.0 && \
./configure --prefix=$VIRT_ROOT && \
make && \
make install && \
cd $MAIN_DIR
