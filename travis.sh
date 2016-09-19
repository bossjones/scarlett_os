#!/usr/bin/env bash

# export MAIN_DIR=$(pwd)
# export VIRT_ROOT=/home/travis/virtualenv/python$TRAVIS_PYTHON_VERSION
# export PKG_CONFIG_PATH=$VIRT_ROOT/lib/pkgconfig
# export SCARLETT_CONFIG=$MAIN_DIR/tests/fixtures/.scarlett
# # - export SCARLETT_HMM=$MAIN_DIR/tests/fixtures/model/hmm/en_US/hub4wsj_sc_8k
# export SCARLETT_LM=$MAIN_DIR/tests/fixtures/lm/1602.lm
# export SCARLETT_DICT=$MAIN_DIR/tests/fixtures/dict/1602.dic
# export PYTHONIOENCODING=UTF8
# export GSTREAMER=1.0
# export PYTHON_VERSION=$(python -c "import sys; print('%s.%s' % sys.version_info[:2])")
# export PYTHON_INC_DIR=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())")
# export PYTHON_SITE_PACKAGES=$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
#

export CFLAGS="-fPIC -O0 -ggdb -fno-inline -fno-omit-frame-pointer"

# JHBuild detects too many cores
export MAKEFLAGS="-j4"

# JHBuild related variables
export PREFIX="${HOME}/jhbuild"
export JHBUILD="${HOME}/gnome"
export ENABLE_PYTHON3=yes

sudo add-apt-repository ppa:miurahr/openresty-devel -y
sudo apt-get update -qq

# Create a basic .jhbuildrc
echo "import os"                           > ~/.jhbuildrc
echo "prefix='${PREFIX}'"                 >> ~/.jhbuildrc
echo "checkoutroot='${JHBUILD}'"          >> ~/.jhbuildrc
echo "moduleset = 'gnome-world'"          >> ~/.jhbuildrc
echo "interact = False"                   >> ~/.jhbuildrc
echo "makeargs = '${MAKEFLAGS}'"          >> ~/.jhbuildrc
echo "os.environ['CFLAGS'] = '${CFLAGS}'" >> ~/.jhbuildrc

mkdir -p "${PREFIX}"
mkdir -p "${JHBUILD}"

sudo apt-get install -qq gnome-common
sudo apt-get install -qq gtk-doc-tools
sudo apt-get install -qq libgtk-3-dev
sudo apt-get install -qq libgirepository1.0-dev

if [ "x${ENABLE_DISTCHECK}" == "xyes" ]; then
  sudo apt-get install -qq yelp-tools;
  sudo apt-get install -qq libgladeui-dev;
fi

if [ "x${ENABLE_LUA51}" == "xyes" ]; then
  sudo apt-get install -qq lua5.1;
  sudo apt-get install -qq liblua5.1-0-dev;
fi

if [ "x${ENABLE_LUAJIT}" == "xyes" ]; then
  sudo apt-get install -qq luajit;
  sudo apt-get install -qq luajit-5.1-dev;
fi

# Must be done after Lua has been installed.
# Fix Lua's package.path and package.cpath and
# add the variables to the JHBuild enviroment
if [ "x${ENABLE_LUA51}" == "xyes" ]; then
  LUA_PATH="`lua5.1 -e 'print(package.path)'`";
  LUA_PATH="${PREFIX}/share/lua/5.1/?/init.lua;${LUA_PATH}";
  LUA_PATH="${PREFIX}/share/lua/5.1/?.lua;${LUA_PATH}";
  LUA_CPATH="`lua5.1 -e 'print(package.cpath)'`";
  LUA_CPATH="${PREFIX}/lib/lua/5.1/?.so;${LUA_CPATH}";

  echo "os.environ['LUA_PATH']  = '${LUA_PATH}'"  >> ~/.jhbuildrc;
  echo "os.environ['LUA_CPATH'] = '${LUA_CPATH}'" >> ~/.jhbuildrc;
fi

if [ "x${ENABLE_PYTHON2}" == "xyes" ]; then
  sudo apt-get install -qq python2-dev;
  sudo apt-get install -qq python-cairo-dev;
  sudo apt-get install -qq python-gi-dev;
fi

if [ "x${ENABLE_PYTHON3}" == "xyes" ]; then
  sudo apt-get install -qq python3-dev;
  sudo apt-get install -qq python3-cairo-dev;
  sudo apt-get install -qq python3-gi;
fi

# Get JHBuild
(cd "${JHBUILD}" &&
 git clone --depth 1 https://github.com/GNOME/jhbuild.git &&
 cd jhbuild && ./autogen.sh --prefix=/usr/local &&
 make && sudo make install)

# Need a gtk-doc that can handle virtual/rename-to function annotations
if [ "x${ENABLE_DISTCHECK}" == "xyes" ]; then
  (cd "${JHBUILD}" &&
   git clone --depth 1 https://github.com/GNOME/gtk-doc.git &&
   jhbuild buildone -n gtk-doc);
fi

# Need at least glib version 2.38
(cd "${JHBUILD}" &&
 git clone --depth 1 https://github.com/GNOME/glib.git &&
 jhbuild buildone -n glib)

# Need at least gobject-introspection version 1.39
(cd "${JHBUILD}" &&
 git clone https://github.com/GNOME/gobject-introspection.git &&
 cd gobject-introspection && git checkout 1.46.0 &&
 jhbuild buildone -n gobject-introspection)

# Need LGI from git master
if [ "x${ENABLE_LUA51}" == "xyes" ]; then
  (cd "${JHBUILD}" &&
   git clone --depth 1 https://github.com/pavouk/lgi.git && cd lgi &&
   jhbuild run make PREFIX="${PREFIX}"
                    CFLAGS="${CFLAGS} -I/usr/include/lua5.1" &&
   jhbuild run make install PREFIX="${PREFIX}");
fi

if [ "x${ENABLE_PYTHON2}" == "xyes" ] ||
   [ "x${ENABLE_PYTHON3}" == "xyes" ]; then
  (cd "${JHBUILD}" &&
   git clone --depth 1 https://github.com/GNOME/pygobject.git);
fi

# Need PyGObject built for Python 2
if [ "x${ENABLE_PYTHON2}" == "xyes" ]; then
  (cd "${JHBUILD}" && cd pygobject &&
   jhbuild run ./autogen.sh --prefix="${PREFIX}" --with-python=python2 &&
   jhbuild run make install && jhbuild run git clean -xdf);
fi

# Need PyGObject built for Python 3
if [ "x${ENABLE_PYTHON3}" == "xyes" ]; then
  (cd "${JHBUILD}" && cd pygobject &&
   jhbuild run ./autogen.sh --prefix="${PREFIX}" --with-python=python3 &&
   jhbuild run make install);
fi

jhbuild run ./autogen.sh --prefix="${PREFIX}"
  --enable-gtk-doc=${ENABLE_DISTCHECK:-no}
  --enable-gtk=${ENABLE_GTK:-no}
  --enable-lua5.1=${ENABLE_LUA51:-no}
  --enable-luajit=${ENABLE_LUAJIT:-no}
  --enable-python2=${ENABLE_PYTHON2:-no}
  --enable-python3=${ENABLE_PYTHON3:-no} || (cat config.log; exit 1)
jhbuild run make

# script:
#   # Can only run when all options are enabled
#   - if [ "x${ENABLE_DISTCHECK}" != "xyes" ]; then
#       jhbuild run make check;
#     else
#       jhbuild run make distcheck;
#     fi
