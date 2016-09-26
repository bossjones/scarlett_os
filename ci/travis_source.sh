# export MAIN_DIR=$(pwd)
export GSTREAMER=1.0
export ENABLE_PYTHON2=yes
export ENABLE_PYTHON3=yes
export ENABLE_GTK=yes
export PYTHON_VERSION=3.4

# from jhbuild
export CFLAGS="-fPIC -O0 -ggdb -fno-inline -fno-omit-frame-pointer"
# JHBuild detects too many cores
export MAKEFLAGS="-j4"

#export CFLAGS="-g -O0"
# export MAKEFLAGS="-j4"

# JHBuild related variables
export PREFIX="${HOME}/jhbuild"
export JHBUILD="${HOME}/gnome"

# NOTE: taken from: jhbuild-session
export PATH=${PREFIX}/bin:${PREFIX}/sbin:${PATH}
export LD_LIBRARY_PATH=${PREFIX}/lib:${LD_LIBRARY_PATH}
export PYTHONPATH=${PREFIX}/lib/python$PYTHON_VERSION/site-packages:/usr/lib/python$PYTHON_VERSION/site-packages
export PKG_CONFIG_PATH=${PREFIX}/lib/pkgconfig:${PREFIX}/share/pkgconfig:/usr/lib/pkgconfig
export XDG_DATA_DIRS=${PREFIX}/share:/usr/share
export XDG_CONFIG_DIRS=${PREFIX}/etc/xdg
export PYTHON="python3"
export PACKAGES="python3-gi python3-gi-cairo"
export CC=gcc
