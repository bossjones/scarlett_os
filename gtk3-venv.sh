#!/usr/bin/env bash
# script for pyenv installation of pygtk3 in ubuntu 12.04
# Adapted from https://gist.github.com/mehcode/6172694

system_package_installed() {
	if ! dpkg -l | grep -q $1; then
		sudo apt-get install $1
	fi
}

python_module_installed() {
	local mod=$1
	if ! python <<- EOF
	try:
	    import $mod
	    raise SystemExit(0)
	except ImportError:
	    raise SystemExit(-1)
	EOF
	then
		return 1
	fi
}

set -e
PYGTK_PREFIX="${VIRT_ROOT}"
# NOTE: "pyenv prefix" can return multiple.
PYGTK_PREFIX=${PYGTK_PREFIX%%:*}
echo -e "\E[1m * Using prefix: $PYGTK_PREFIX\E[0m"
export PATH="$PYGTK_PREFIX/bin:$PATH"
export PKG_CONFIG_PATH="$PYGTK_PREFIX/lib/pkgconfig:$PKG_CONFIG_PATH"

system_package_installed libcairo2-dev
system_package_installed libglib2.0-dev
system_package_installed libgirepository1.0-dev

# Setup variables.
CACHE="${MAIN_DIR}/install-pygtk-$$"
echo -e "\E[1m * Building in $CACHE\E[0m"

PYTHON_VERSION="$(python -c 'import sys; print(sys.version_info[0])')"
if [[ "$PYTHON_VERSION" == 2 ]]; then
    echo "[USING: python2]"
    PYCAIRO_BASENAME=py2cairo
else
    echo "[USING: python3]"
    PYCAIRO_BASENAME=pycairo
fi

# Make temp directory.
mkdir -p $CACHE

# Test for pycairo/py2cairo.
echo -e "\E[1m * Checking for cairo...\E[0m"
if ! python_module_installed cairo; then
    echo -e "\E[1m * Installing ${PYCAIRO_BASENAME}...\E[0m"
    # Fetch, build, and install pycairo/py2cairo.
    (   cd $CACHE
        if [[ $PYCAIRO_BASENAME == py2cairo ]]; then
            curl 'http://cairographics.org/releases/py2cairo-1.10.0.tar.bz2' > "py2cairo.tar.bz2"
            tar -xvf py2cairo.tar.bz2
            (   cd py2cairo*
                touch ChangeLog
                autoreconf -ivf
                ./configure --prefix=$PYGTK_PREFIX
                make
                make install
            )
        else
            git clone --depth=10 git://git.cairographics.org/git/${PYCAIRO_BASENAME}
            (   cd ${PYCAIRO_BASENAME}*
                python3 setup.py install
            )
        fi
    )
fi

# # Test for gobject-introspection
# echo -e "\E[1m * Checking for cairo...\E[0m"
# if ! python_module_installed cairo; then
#     echo -e "\E[1m * Installing ${PYCAIRO_BASENAME}...\E[0m"
#     # Fetch, build, and install pycairo/py2cairo.
#     (   cd $CACHE
#         if [[ $PYCAIRO_BASENAME == py2cairo ]]; then
#             curl 'http://cairographics.org/releases/py2cairo-1.10.0.tar.bz2' > "py2cairo.tar.bz2"
#             tar -xvf py2cairo.tar.bz2
#             (   cd py2cairo*
#                 touch ChangeLog
#                 autoreconf -ivf
#                 ./configure --prefix=$PYGTK_PREFIX
#                 make
#                 make install
#             )
#         else
#             git clone --depth=10 git://git.cairographics.org/git/${PYCAIRO_BASENAME}
#             (   cd ${PYCAIRO_BASENAME}*
#                 python3 setup.py install
#             )
#         fi
#     )
# fi

# (cd "${JHBUILD}" &&
#    git clone https://github.com/GNOME/gobject-introspection.git &&
#    cd gobject-introspection && git checkout 1.46.0 &&
#    jhbuild buildone -n gobject-introspection)

#
# - (cd "${JHBUILD}" &&
#    git clone --depth 1 https://github.com/GNOME/glib.git &&
#    jhbuild buildone -n glib)


# - curl -L "http://ftp.acc.umu.se/pub/gnome/sources/glib/2.32/glib-2.32.4.tar.xz" > glib-2.32.4.tar.xz
# - tar xf glib-2.32.4.tar.xz
# - cd glib-2.32.4
# - ./configure --prefix=$VIRT_ROOT > /dev/null
# - make > /dev/null
# - make install > /dev/null
# - cd $MAIN_DIR
# - sudo apt-get install -qq libtheora-dev libogg-dev libvorbis-dev libasound2-dev libjack-dev

# source: https://github.com/apache/celix/blob/master/Dockerfile.Android
# source: http://www.linuxfromscratch.org/blfs/view/svn/general/libffi.html

echo -e "\E[1m * Installing libffi...\E[0m"
curl -L -O ftp://sourceware.org/pub/libffi/libffi-3.2.1.tar.gz && \
tar -xvzf libffi-3.2.1.tar.gz  && \
cd libffi-3.2.1 && \
sed -e '/^includesdir/ s/$(libdir).*$/$(includedir)/' \
    -i include/Makefile.in &&
sed -e '/^includedir/ s/=.*$/=@includedir@/' \
    -e 's/^Cflags: -I${includedir}/Cflags:/' \
    -i libffi.pc.in        &&
./configure --prefix=/usr --disable-static &&
make && \
sudo make install && \
ldconfig

echo -e "\E[1m * Installing pcre...\E[0m"
(   cd $CACHE
	curl --remote-name ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.39.tar.gz
	tar -xvzf pcre-8.39.tar.gz
	cd pcre-8.39
	./configure --prefix=/usr --enable-utf
	make && sudo make install
	ldconfig
)


echo -e "\E[1m * Installing glib...\E[0m"
# Fetch, build, and install glib. v3.18.2
(   cd $CACHE
	git clone --depth=10 git://git.gnome.org/glib
	(   cd glib*
		# git reset --hard 7dc01c05fc07433161be74509b985647f6bedd19
		./autogen.sh --prefix=$PYGTK_PREFIX
		make
		make install
	)
)

# Test for gobject.
echo -e "\E[1m * Checking for gobject...\E[0m"
if ! python_module_installed gi; then
    echo -e "\E[1m * Installing gobject...\E[0m"
    # Fetch, build, and install gobject. v3.18.2
    (   cd $CACHE
        git clone --depth=10 git://git.gnome.org/pygobject
        (   cd pygobject*
		    git reset --hard 7dc01c05fc07433161be74509b985647f6bedd19
            # Fix include (reported at https://bugzilla.gnome.org/show_bug.cgi?id=746742).
            sed -i 's~^#include <pycairo/py3cairo.h>~#include <py3cairo.h>~' gi/pygi-foreign-cairo.c
            ./autogen.sh --prefix=$PYGTK_PREFIX
            make
            make install
        )
    )
fi
