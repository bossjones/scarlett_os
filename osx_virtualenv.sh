#!/usr/bin/env bash

brew reinstall gtk+3
brew reinstall gst-plugins-base gst-plugins-bad gst-plugins-ugly gst-plugins-good
brew reinstall gsed

export PYTHON_VERSION=3.5
export GSTREAMER=1.0
export PI_HOME=~/
export MAIN_DIR="${PI_HOME}/dev/bossjones/scarlett_os"
export VIRT_ROOT="${PI_HOME}/.virtualenvs/scarlett-os-venv2"
export PKG_CONFIG_PATH="${PI_HOME}/.virtualenvs/scarlett-os-venv2/lib/pkgconfig"
export SCARLETT_CONFIG="${PI_HOME}/dev/bossjones/scarlett_os/tests/fixtures/.scarlett"

# NOTE: THIS NEEDS TO BE FIXED
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
gsed -i '154s/data={}/return/' .waf3-1.6.4-*/waflib/Build.py # Bufix: https://bugs.freedesktop.org/show_bug.cgi?id=76759
python waf configure --prefix=$VIRTUAL_ENV # Now it should configure.
python waf build
python waf install

unset ARCHFLAGS
cd -

###########################################
# pygobject3
###########################################

export PKG_CONFIG_PATH=$VIRTUAL_ENV/lib/pkgconfig:/usr/local/opt/libffi/lib/pkgconfig
cd $MAIN_DIR
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

#############################################
# espeak compile
#############################################

export PATH_ESPEAK_DATA=$VIRTUAL_ENV/share
mkdir -p $PATH_ESPEAK_DATA=$VIRTUAL_ENV/share

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

export PATH=$PATH:$MAIN_DIR/espeak-1.48.04-source/src

#############################################
# espeak gst plugin
#############################################

cd $MAIN_DIR && \
curl -L "https://github.com/bossjones/bossjones-gst-plugins-espeak-0-4-0/archive/v0.4.1.tar.gz" > gst-plugins-espeak-0.4.0.tar.gz && \
tar xvf gst-plugins-espeak-0.4.0.tar.gz && \
rm -rfv gst-plugins-espeak-0.4.0 && \
mv -fv bossjones-gst-plugins-espeak-0-4-0-0.4.1 gst-plugins-espeak-0.4.0 && \
cd gst-plugins-espeak-0.4.0 && \

# export PKG_CONFIG_PATH=$VIRTUAL_ENV/lib/pkgconfig:/usr/local/opt/libffi/lib/pkgconfig
export PKG_CONFIG_PATH=$VIRTUAL_ENV/lib/pkgconfig:/usr/local/Cellar/gtk+3/3.18.5/lib/pkgconfig

export ESPEAK_PREFIX="$MAIN_DIR/espeak-1.48.04-source/src" && \
gsed -i "s,espeak/speak_lib.h,$MAIN_DIR/espeak-1.48.04-source/src/speak_lib.h," $MAIN_DIR/gst-plugins-espeak-0.4.0/src/espeak.c && \
./configure --prefix=$VIRT_ROOT CFLAGS="-I$VIRTUAL_ENV/include -I/usr/local/Cellar/gtk+3/3.20.6/include" --prefix=$VIRTUAL_ENV && \
make && \
make install && \
cd $MAIN_DIR

if [ -z ${MAIN_DIR+x} ]; then echo "MAIN_DIR is unset" && exit 1; else echo "MAIN_DIR is set to '$MAIN_DIR'"; fi

#############################################
# sphinx base CLONING
#############################################
cd $MAIN_DIR

if [[ -d $MAIN_DIR/sphinxbase ]]; then
  cd $MAIN_DIR/sphinxbase
  git status && git add . && git reset --hard && git fetch --all
else
  cd $MAIN_DIR && git clone https://github.com/cmusphinx/sphinxbase.git sphinxbase && cd sphinxbase
fi

git checkout 74370799d5b53afc5b5b94a22f5eff9cb9907b97
git clean -ffdx
git submodule update --init --recursive

#############################################
# pocketsphinx CLONING
#############################################
cd $MAIN_DIR

if [[ -d $MAIN_DIR/pocketsphinx ]]; then
  cd $MAIN_DIR/pocketsphinx
  (git status && git add . && git reset --hard && git fetch --all)
else
    cd $MAIN_DIR && git clone https://github.com/cmusphinx/pocketsphinx.git pocketsphinx && cd pocketsphinx
fi

git checkout 68ef5dc6d48d791a747026cd43cc6940a9e19f69
git clean -ffdx
git submodule update --init --recursive


# git clone https://github.com/cmusphinx/sphinxbase.git # 74370799d5b53afc5b5b94a22f5eff9cb9907b97
# git clone https://github.com/cmusphinx/pocketsphinx.git # 68ef5dc6d48d791a747026cd43cc6940a9e19f69

# "msg": "'/usr/bin/aptitude safe-upgrade' failed: No apport report written because the error message indicates its a followup error from a previous failure.\nNo apport report written because the error message indicates its a followup error from a previous failure.\nNo apport report written because MaxReports is reached already\nE: Sub-process /usr/bin/dpkg returned an error code (1)\nFailed to perform requested operation on package.  Trying to recover:\nRunning depmod.\nupdate-initramfs: deferring update (hook will be called later)\nThe link /initrd.img is a dangling linkto /boot/initrd.img-4.4.0-36-generic\nvmlinuz(/boot/vmlinuz-4.4.0-36-generic\n) points to /boot/vmlinuz-4.4.0-36-generic\n (/boot/vmlinuz-4.4.0-36-generic) -- doing nothing at /var/lib/dpkg/info/linux-image-4.4.0-36-generic.postinst line 491.\nExamining /etc/kernel/postinst.d.\nrun-parts: executing /etc/kernel/postinst.d/apt-auto-removal 4.4.0-36-generic /boot/vmlinuz-4.4.0-36-generic\nrun-parts: executing /etc/kernel/postinst.d/dkms 4.4.0-36-generic /boot/vmlinuz-4.4.0-36-generic\nrun-parts: executing /etc/kernel/postinst.d/initramfs-tools 4.4.0-36-generic /boot/vmlinuz-4.4.0-36-generic\nupdate-initramfs: Generating /boot/initrd.img-4.4.0-36-generic\n\ngzip: stdout: No space left on device\ncpio: write error: Broken pipe\nE: mkinitramfs failure cpio 1 gzip 1\nupdate-initramfs: failed for /boot/initrd.img-4.4.0-36-generic with 1.\nrun-parts: /etc/kernel/postinst.d/initramfs-tools exited with return code 1\nFailed to process /etc/kernel/postinst.d at /var/lib/dpkg/info/linux-image-4.4.0-36-generic.postinst line 1052.\ndpkg: error processing package linux-image-4.4.0-36-generic (--configure):\n subprocess installed post-installation script returned error exit status 2\ndpkg: dependency problems prevent configuration of linux-image-extra-4.4.0-36-generic:\n linux-image-extra-4.4.0-36-generic depends on linux-image-4.4.0-36-generic; however:\n  Package linux-image-4.4.0-36-generic is not configured yet.\n\ndpkg: error processing package linux-image-extra-4.4.0-36-generic (--configure):\n dependency problems - leaving unconfigured\ndpkg: dependency problems prevent configuration of linux-image-generic:\n linux-image-generic depends on linux-image-4.4.0-36-generic; however:\n  Package linux-image-4.4.0-36-generic is not configured yet.\n linux-image-generic depends on linux-image-extra-4.4.0-36-generic; however:\n  Package linux-image-extra-4.4.0-36-generic is not configured yet.\n\ndpkg: error processing package linux-image-generic (--configure):\n dependency problems - leaving unconfigured\ndpkg: dependency problems prevent configuration of linux-generic:\n linux-generic depends on linux-image-generic (= 4.4.0.36.38); however:\n  Package linux-image-generic is not configured yet.\n\ndpkg: error processing package linux-generic (--configure):\n dependency problems - leaving unconfigured\nErrors were encountered while processing:\n linux-image-4.4.0-36-generic\n linux-image-extra-4.4.0-36-generic\n linux-image-generic\n linux-generic\n",
#############################################
# sphinx base
#############################################

# PYTHON=/usr/local/bin/python3 PYTHON_VERSION='3.5' ./autogen.sh --prefix=$VIRT_ROOT --disable-debug --disable-dependency-tracking
#  |2.1.7|  using virtualenv: scarlett-os-venv2  Malcolms-MBP-3 in ~/dev/bossjones/scarlett_os/sphinxbase
# ± |detached:master~32 ?:56 ?| ? python -c "import sys; print(sys.path);"
# ['',
# '/Users/malcolm/.virtualenvs/scarlett-os-venv2/lib/python35.zip'
# '/Users/malcolm/.virtualenvs/scarlett-os-venv2/lib/python3.5'
# '/Users/malcolm/.virtualenvs/scarlett-os-venv2/lib/python3.5/plat-darwin'
# '/Users/malcolm/.virtualenvs/scarlett-os-venv2/lib/python3.5/lib-dynload'
# '/usr/local/Cellar/python3/3.5.2_1/Frameworks/Python.framework/Versions/3.5/lib/python3.5'
# '/usr/local/Cellar/python3/3.5.2_1/Frameworks/Python.framework/Versions/3.5/lib/python3.5/plat-darwin'
# '/Users/malcolm/.virtualenvs/scarlett-os-venv2/lib/python3.5/site-packages']


# NOTE: potential solution
# source: http://stackoverflow.com/questions/6490513/vim-failing-to-compile-with-python-on-os-x
# ./configure PYTHON_EXTRA_LDFLAGS="-u _PyMac_Error /Library/Frameworks/Python.framework/Versions/2.7/Python"
# checking python extra linking flags... PYTHON_EXTRA_LDFLAGS="-u _PyMac_Error /usr/local/opt/python3/Frameworks/Python.framework/Versions/3.5/Python"

./autogen.sh --prefix=$VIRT_ROOT PYTHON_EXTRA_LDFLAGS="-u _PyMac_Error /usr/local/opt/python3/Frameworks/Python.framework/Versions/3.5/Python" --disable-dependency-tracking PYTHON=python3
# "./configure", "--disable-dependency-tracking", "--prefix=#{prefix}", "PYTHON=#{python}"

# source: https://docs.python.org/3/extending/embedding.html#compiling-and-linking-

#  |2.1.7|  using virtualenv: scarlett-os-venv2  Malcolms-MBP-3 in ~/dev/bossjones/scarlett_os/sphinxbase
# ± |detached:master~32 ?:56 ?| ? /usr/local/bin/python3.5-config --cflags
# -I/usr/local/Cellar/python3/3.5.2_1/Frameworks/Python.framework/Versions/3.5/include/python3.5m -I/usr/local/Cellar/python3/3.5.2_1/Frameworks/Python.framework/Versions/3.5/include/python3.5m -Wno-unused-result -Wsign-compare -Wunreachable-code -fno-common -dynamic -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes
#
#  |2.1.7|  using virtualenv: scarlett-os-venv2  Malcolms-MBP-3 in ~/dev/bossjones/scarlett_os/sphinxbase
# ± |detached:master~32 ?:56 ?| ? /usr/local/bin/python3.5-config --ldflags
# -L/usr/local/Cellar/python3/3.5.2_1/Frameworks/Python.framework/Versions/3.5/lib/python3.5/config-3.5m -lpython3.5m -ldl -framework CoreFoundation
#
#  |2.1.7|  using virtualenv: scarlett-os-venv2  Malcolms-MBP-3 in ~/dev/bossjones/scarlett_os/sphinxbase
# ± |detached:master~32 ?:56 ?| ?


# ± |detached:master~32 ?:56 ?| ? ipython
# WARNING: Attempting to work in a virtualenv. If you encounter problems, please install IPython inside the virtualenv.
# Python 2.7.11 (default, Jan 22 2016, 08:28:37)
# Type "copyright", "credits" or "license" for more information.
#
# IPython 4.0.0 -- An enhanced Interactive Python.
# ?         -> Introduction and overview of IPython's features.
# %quickref -> Quick reference.
# help      -> Python's own help system.
# object?   -> Details about 'object', use 'object??' for extra details.
#
# In [1]: import sysconfig
#
# In [2]: sysconfig.get_config_var('LIBS')
# Out[2]: '-ldl  -framework CoreFoundation'
#
# In [3]: sysconfig.get_config_var('LINKFORSHARED')
# Out[3]: '-u _PyMac_Error Python.framework/Versions/2.7/Python'
#
# In [4]:

cd $MAIN_DIR/sphinxbase && \
PYTHON=/usr/local/bin/python3 ./autogen.sh --prefix=$VIRT_ROOT LDFLAGS="-L$VIRT_ROOT/lib -L/usr/local/opt/python3/lib" --disable-debug --disable-dependency-tracking && \
PYTHON=/usr/local/bin/python3 PYTHON_VERSION='3.5' ./configure --prefix=$VIRT_ROOT LDFLAGS="-L/usr/local/opt/python3/lib" --disable-debug --disable-dependency-tracking && \
make clean all && \
# make check && \
make install && \
cd $MAIN_DIR

#############################################
# pocketsphinx
#############################################

cd $MAIN_DIR/pocketsphinx && \
./autogen.sh --prefix=$VIRT_ROOT && \
./configure --prefix=$VIRT_ROOT && \
make clean all && \
# make check && \
make install && \
cd $MAIN_DIR
