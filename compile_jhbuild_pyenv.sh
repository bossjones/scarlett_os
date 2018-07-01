#!/usr/bin/env bash

mkdir -p /home/pi/gnome

# Install jhbuild if not done
if [[ ! -f "/usr/local/bin/jhbuild" ]] && [[ -f "/home/pi/jhbuild/autogen.sh" ]] || [[ "${FORCE_BUILD_JHBUILD}" = "" ]]; then
    echo "****************[JHBUILD]****************" && \
    cd /home/pi && \
    [ -d /home/pi/jhbuild ] || git clone https://github.com/GNOME/jhbuild.git && \
    cd jhbuild && \
    git checkout 86d958b6778da649b559815c0a0dbe6a5d1a8cd4 && \
    ./autogen.sh --prefix=/usr/local > /dev/null && \
    make > /dev/null && \
    sudo make install > /dev/null && \
    sudo chown pi:pi -R /usr/local/jhbuild && \
    chown pi:pi -R /home/pi/jhbuild && \

    echo "****************[GTK-DOC]****************" && \
    cd /home/pi/gnome && \
    git clone https://github.com/GNOME/gtk-doc.git && \
    jhbuild buildone -n gtk-doc && \

    echo "****************[GLIB]****************" && \
    cd /home/pi/gnome && \
    git clone https://github.com/GNOME/glib.git && \
    cd glib && \
    git checkout eaca4f4116801f99e30e42a857559e19a1e6f4ce && \
    jhbuild buildone -n glib && \

    echo "****************[GOBJECT-INTROSPECTION]****************" && \
    cd /home/pi/gnome && \
    git clone https://github.com/GNOME/gobject-introspection.git && \
    cd gobject-introspection && \
    git checkout cee2a4f215d5edf2e27b9964d3cfcb28a9d4941c && \
    jhbuild buildone -n gobject-introspection && \

    echo "****************[pixman]****************" && \
    cd /home/pi/gnome && \
    [ -d /home/pi/gnome/pixman ] || git clone git://anongit.freedesktop.org/git/pixman && \
    cd pixman && \
    git checkout pixman-0.33.6 && \
    chmod +x ./autogen.sh && \
    jhbuild run ./autogen.sh && \
    jhbuild run ./configure --prefix=/home/pi/jhbuild && \
    jhbuild run make -j4  && \
    jhbuild run make install && \

    echo "****************[cairo]****************" && \
    cd /home/pi/gnome && \
    [ -d /home/pi/gnome/cairo ] || git clone git://anongit.freedesktop.org/git/cairo && \
    cd cairo && \
    git checkout 1.14.6 && \
    chmod +x ./autogen.sh && \
    jhbuild run ./autogen.sh && \
    jhbuild run ./configure --prefix=/home/pi/jhbuild --enable-xlib --enable-ft --enable-svg --enable-ps --enable-pdf --enable-tee --enable-gobject && \
    jhbuild run make -j4  && \
    jhbuild run make install && \

    echo "****************[PYCAIRO]****************" && \
    cd /home/pi/gnome && \
    [ -d /home/pi/gnome/pycairo ] || git clone --depth=10 git://git.cairographics.org/git/pycairo && \
    cd pycairo && \
    jhbuild run python3 setup.py install && \
    echo "IF THIS DOESNT WORK, LOOK AT OTHER OPTION AT BOTTOM OF SCRIPT"

    echo "****************[PYGOBJECT]****************" && \
    cd /home/pi/gnome && \
    git clone https://github.com/GNOME/pygobject.git && \
    cd /home/pi/gnome && \
    cd pygobject && \
    git checkout fb1b8fa8a67f2c7ea7ad4b53076496a8f2b4afdb && \
    jhbuild run ./autogen.sh --prefix=/home/pi/jhbuild --with-python=$(which python3) > /dev/null && \
    jhbuild run make install > /dev/null && \

    echo "****************[meson]****************" && \
    jhbuild run python -m pip install meson && \


    echo "****************[fribidi]****************" && \
    cd /home/pi/gnome && \
    git clone https://github.com/fribidi/fribidi.git && \
    cd /home/pi/gnome && \
    cd fribidi && \
    jhbuild run meson mesonbuild/ --prefix=/home/pi/jhbuild -Ddocs=false --libdir=lib --includedir=include --bindir=bin --datadir=share --mandir=share/man && \
    jhbuild run ninja -C mesonbuild/ && \
    jhbuild run ninja -C mesonbuild/ install && \

    echo "****************[pango]****************" && \
    cd /home/pi/gnome && \
    git clone https://gitlab.gnome.org/GNOME/pango.git && \
    cd /home/pi/gnome && \
    cd pango && \
    git checkout 1.42.1 && \
    jhbuild run meson mesonbuild/ --prefix=/home/pi/jhbuild --libdir=lib --includedir=include --bindir=bin --datadir=share --mandir=share/man && \
    jhbuild run ninja -C mesonbuild/ dist && \


    echo "****************[gtk2]****************" && \
    cd $JHBUILD && \
    git clone https://gitlab.gnome.org/GNOME/gtk.git gtk2 && \
    cd gtk2 && \
    git checkout gtk-2-24 && \
    cd $JHBUILD/gtk2 && \
    jhbuild run ./autogen.sh --prefix=/home/pi/jhbuild > /dev/null && \
    jhbuild run ./configure --prefix=/home/pi/jhbuild --disable-man --with-xinput=xfree > /dev/null && \
    jhbuild run make clean all > /dev/null && \
    jhbuild run make install > /dev/null

    echo "****************[gtk3]****************" && \
    cd $JHBUILD && \
    git clone https://gitlab.gnome.org/GNOME/gtk.git && \
    cd gtk && \
    git checkout gtk-3-22 && \
    cd $JHBUILD/gtk && \
    jhbuild run ./autogen.sh --prefix=/home/pi/jhbuild > /dev/null && \
    jhbuild run ./configure --prefix=/home/pi/jhbuild --enable-xkb --enable-xinerama --enable-xrandr --enable-xfixes --enable-xcomposite --enable-xdamage
--enable-x11-backend > /dev/null && \
    jhbuild run make clean all > /dev/null && \
    jhbuild run make install > /dev/null

    echo "****************[GSTREAMER]****************" && \
    cd /home/pi/gnome && \
    curl -L "https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-1.8.2.tar.xz" > gstreamer-1.8.2.tar.xz && \
    tar -xJf gstreamer-1.8.2.tar.xz && \
    cd gstreamer-1.8.2 && \
    jhbuild run ./autogen.sh --prefix=/home/pi/jhbuild && \
    jhbuild run ./configure --enable-introspection=yes --enable-gtk-doc=no --prefix=/home/pi/jhbuild > /dev/null && \
    jhbuild run make -j4  > /dev/null && \
    jhbuild run make install > /dev/null && \

    echo "****************[ORC]****************" && \
    cd /home/pi/gnome && \
    curl -L "https://gstreamer.freedesktop.org/src/orc/orc-0.4.25.tar.xz" > orc-0.4.25.tar.xz && \
    tar -xJf orc-0.4.25.tar.xz && \
    cd orc-0.4.25 && \
    jhbuild run ./configure --prefix=/home/pi/jhbuild > /dev/null && \
    jhbuild run make -j4  > /dev/null && \
    jhbuild run make install > /dev/null && \

    echo "****************[GST-PLUGINS-BASE]****************" && \
    cd /home/pi/gnome && \
    curl -L "http://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-1.8.2.tar.xz" > gst-plugins-base-1.8.2.tar.xz && \
    tar -xJf gst-plugins-base-1.8.2.tar.xz && \
    cd gst-plugins-base-1.8.2 && \
    jhbuild run ./autogen.sh --prefix=/home/pi/jhbuild && \
    jhbuild run ./configure --prefix=/home/pi/jhbuild --enable-orc --enable-introspection=yes --enable-gtk-doc=no --disable-examples --enable-gtk-doc-html=no > /dev/null && \
    jhbuild run make -j4  > /dev/null && \
    jhbuild run make install > /dev/null && \

    echo "****************[GST-PLUGINS-GOOD]****************" && \
    cd /home/pi/gnome && \
    curl -L "http://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-1.8.2.tar.xz" > gst-plugins-good-1.8.2.tar.xz && \
    tar -xJf gst-plugins-good-1.8.2.tar.xz && \
    cd gst-plugins-good-1.8.2 && \
    jhbuild run ./autogen.sh --prefix=/home/pi/jhbuild && \
    jhbuild run ./configure --prefix=/home/pi/jhbuild --enable-orc --enable-gtk-doc=no --disable-examples --enable-gtk-doc-html=no > /dev/null && \
    jhbuild run make -j4  > /dev/null && \
    jhbuild run make install > /dev/null && \

    echo "****************[GST-PLUGINS-UGLY]****************" && \
    cd /home/pi/gnome && \
    curl -L "http://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-1.8.2.tar.xz" > gst-plugins-ugly-1.8.2.tar.xz && \
    tar -xJf gst-plugins-ugly-1.8.2.tar.xz && \
    cd gst-plugins-ugly-1.8.2 && \
    jhbuild run ./autogen.sh --prefix=/home/pi/jhbuild && \
    jhbuild run ./configure --prefix=/home/pi/jhbuild --enable-orc --enable-gtk-doc=no --disable-examples --enable-gtk-doc-html=no > /dev/null && \
    jhbuild run make -j4  > /dev/null && \
    jhbuild run make install > /dev/null && \

    echo "****************[GST-PLUGINS-BAD]****************" && \
    cat /home/pi/jhbuild/bin/gdbus-codegen && \
    export BOSSJONES_PATH_TO_PYTHON=$(which python3) && \
    sed -i 's,#!python3,#!/home/pi/.pyenv/versions/3.5.2/bin/python3,g' /home/pi/jhbuild/bin/gdbus-codegen && \
    sed -i 's,#!python,#!/home/pi/.pyenv/versions/3.5.2/bin/python3,g' /home/pi/jhbuild/bin/gdbus-codegen && \
    cat /home/pi/jhbuild/bin/gdbus-codegen && \
    cd /home/pi/gnome && \
    curl -L "http://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-1.8.2.tar.xz" > gst-plugins-bad-1.8.2.tar.xz && \
    tar -xJf gst-plugins-bad-1.8.2.tar.xz && \
    cd gst-plugins-bad-1.8.2 && \
    jhbuild run ./autogen.sh --prefix=/home/pi/jhbuild && \
    jhbuild run ./configure --prefix=/home/pi/jhbuild --enable-orc --enable-gtk-doc=no --disable-examples --enable-gtk-doc-html=no > /dev/null && \
    jhbuild run make -j4  > /dev/null && \
    jhbuild run make install > /dev/null && \

    echo "****************[GST-LIBAV]****************" && \
    cd /home/pi/gnome && \
    curl -L "http://gstreamer.freedesktop.org/src/gst-libav/gst-libav-1.8.2.tar.xz" > gst-libav-1.8.2.tar.xz && \
    tar -xJf gst-libav-1.8.2.tar.xz && \
    cd gst-libav-1.8.2 && \
    jhbuild run ./autogen.sh --prefix=/home/pi/jhbuild && \
    jhbuild run ./configure --prefix=/home/pi/jhbuild --enable-orc --enable-gtk-doc=no --enable-gtk-doc-html=no > /dev/null && \
    jhbuild run make -j4  > /dev/null && \
    jhbuild run make install > /dev/null && \


    echo "****************[GST-PYTHON]****************" && \
    cd /home/pi/gnome && \
    git clone https://github.com/GStreamer/gst-python && \
    cd gst-python && \
    git checkout 1.8.2 && \
    jhbuild run ./autogen.sh --prefix=/home/pi/jhbuild && \
    jhbuild run ./configure --prefix=/home/pi/jhbuild --enable-shared=no > /dev/null && \
    jhbuild run make -j4  > /dev/null && \
    jhbuild run make install > /dev/null && \

    echo "****************[GST-PLUGINS-ESPEAK]****************" && \
    cd $JHBUILD && \
    curl -L "https://github.com/bossjones/bossjones-gst-plugins-espeak-0-4-0/archive/v0.4.1.tar.gz" > gst-plugins-espeak-0.4.0.tar.gz && \
    tar xvf gst-plugins-espeak-0.4.0.tar.gz && \
    rm -rfv gst-plugins-espeak-0.4.0 && \
    mv -fv bossjones-gst-plugins-espeak-0-4-0-0.4.1 gst-plugins-espeak-0.4.0 && \
    cd gst-plugins-espeak-0.4.0 && \
    for i in `grep -irH "-lespeak-ng" * | cut -d ':' -f1`; do
        sed -i 's,-lespeak-ng,-lespeak,g' $i
    done
    jhbuild run ./configure --prefix=/home/pi/jhbuild > /dev/null && \
    jhbuild run make > /dev/null && \
    jhbuild run make install > /dev/null && \

    echo "****************[SPHINXBASE]****************" && \
    cd $JHBUILD && \
    git clone https://github.com/cmusphinx/sphinxbase.git && \
    cd sphinxbase && \
    git checkout 74370799d5b53afc5b5b94a22f5eff9cb9907b97 && \
    cd $JHBUILD/sphinxbase && \
    jhbuild run ./autogen.sh --prefix=/home/pi/jhbuild > /dev/null && \
    jhbuild run ./configure --prefix=/home/pi/jhbuild > /dev/null && \
    jhbuild run make clean all > /dev/null && \
    jhbuild run make install > /dev/null && \

    echo "****************[POCKETSPHINX]****************" && \
    cd $JHBUILD && \
    git clone https://github.com/cmusphinx/pocketsphinx.git && \
    cd pocketsphinx && \
    git checkout 68ef5dc6d48d791a747026cd43cc6940a9e19f69 && \
    jhbuild run ./autogen.sh --prefix=/home/pi/jhbuild > /dev/null && \
    jhbuild run ./configure --prefix=/home/pi/jhbuild --with-python > /dev/null && \
    jhbuild run make clean all > /dev/null && \
    jhbuild run make install > /dev/null && \

    echo "****************[GDBINIT]****************" && \
    sudo zcat /usr/share/doc/python3.5/gdbinit.gz | tee /home/pi/.gdbinit && \
    sudo chown pi:pi /home/pi/.gdbinit && \

    echo "****************[GSTREAMER-COMPLETION]****************" && \
    curl -L "https://raw.githubusercontent.com/drothlis/gstreamer/bash-completion-master/tools/gstreamer-completion" | sudo tee -a /etc/bash_completion.d/gstreamer-completion && \
    sudo chown root:root /etc/bash_completion.d/gstreamer-completion && \
    sudo ldconfig
else
    # if we don't need to re-build
    echo "****************[HEY GUESS WHAT]****************"
    echo "****************[JHBUILD IS RDY]****************"
    [[ ! -f "/usr/local/bin/jhbuild" ]] && echo 'TRUE: ! -f "/usr/local/bin/jhbuild"' || echo 'FALSE: ! -f "/usr/local/bin/jhbuild"'
    [[ -f "/home/pi/jhbuild/autogen.sh" ]] && echo 'TRUE: -f "/home/pi/jhbuild/autogen.sh"' || echo 'FALSE: -f "/home/pi/jhbuild/autogen.sh"'
    [[ $FORCE_BUILD_JHBUILD = 1 ]] && echo 'TRUE: $FORCE_BUILD_JHBUILD = 1' || echo 'FALSE: $FORCE_BUILD_JHBUILD = 1'
fi

# Alternative to compiling pyenv pycairo
# SOURCE: https://github.com/pyenv/pyenv/issues/16
# set -e
_PYENV_ROOT="${_PYENV_ROOT:-${HOME}/.pyenv}"
_PREFIX="${_PYENV_ROOT}/versions/$(pyenv version-name | awk -F: '{print($1)}')"

# test -f py2cairo-1.10.0.tar.bz2 || wget http://cairographics.org/releases/py2cairo-1.10.0.tar.bz2
# rm -rf py2cairo-1.10.0
# tar xvf py2cairo-1.10.0.tar.bz2
# cd py2cairo-1.10.0
# python2 ./waf --version
# (
#   cd .waf-*
#   wget -O- "https://gist.github.com/yyuu/5566264/raw/612da9ff5b215cda42eb62fc3d332f3d2ae172db/python.py.patch" | patch -p0
# )
# python2 ./waf --prefix="${_PREFIX}" configure
# python2 ./waf build
# python2 ./waf install

# python2 ./waf --prefix="${_PREFIX}" configure

# ./autogen.sh --prefix="${_PREFIX}"
# for i in `grep -irH "import sys; print sys.prefix" * | cut -d ':' -f1`; do
#     sed -i 's,print sys.prefix,print(sys.prefix),g' $i
# done
# ./configure --prefix="${_PREFIX}"

# FIXME: something to look at re: adding /home/pi/jhbuild/lib/python3.5/site-packages/gi to LD_LIBRARY_PATH
# ldconfig -n /home/pi/jhbuild/lib/python3.5/site-packages/gi
# ----------------------------------------------------------------------
# Libraries have been installed in:
#    /home/pi/jhbuild/lib/python3.5/site-packages/gi

# If you ever happen to want to link against installed libraries
# in a given directory, LIBDIR, you must either use libtool, and
# specify the full pathname of the library, or use the '-LLIBDIR'
# flag during linking and do at least one of the following:
#    - add LIBDIR to the 'LD_LIBRARY_PATH' environment variable
#      during execution
#    - add LIBDIR to the 'LD_RUN_PATH' environment variable
#      during linking
#    - use the '-Wl,-rpath -Wl,LIBDIR' linker flag
#    - have your system administrator add LIBDIR to '/etc/ld.so.conf'

# See any operating system documentation about shared libraries for
# more information, such as the ld(1) and ld.so(8) manual pages.

# https://gist.github.com/sphaero/02717b0b35501ad94863
# # get repos if they are not there yet
# [ ! -d gstreamer ] && git clone git://anongit.freedesktop.org/git/gstreamer/gstreamer
# [ ! -d gst-plugins-base ] && git clone git://anongit.freedesktop.org/git/gstreamer/gst-plugins-base
# [ ! -d gst-plugins-good ] && git clone git://anongit.freedesktop.org/git/gstreamer/gst-plugins-good
# [ ! -d gst-plugins-bad ] && git clone git://anongit.freedesktop.org/git/gstreamer/gst-plugins-bad
# [ ! -d gst-plugins-ugly ] && git clone git://anongit.freedesktop.org/git/gstreamer/gst-plugins-ugly
# [ ! -d gst-libav ] && git clone git://anongit.freedesktop.org/git/gstreamer/gst-libav
# [ ! -d gst-omx ] && git clone git://anongit.freedesktop.org/git/gstreamer/gst-omx
# [ ! -d gst-python ] && git clone git://anongit.freedesktop.org/git/gstreamer/gst-python
# [ ! $RPI ] && [ ! -d gstreamer-vaapi ] && git clone git://gitorious.org/vaapi/gstreamer-vaapi.git


#  {
#             "name": "gtk3",
#             "config-opts": [ "--enable-xkb",
#                              "--enable-xinerama",
#                              "--enable-xrandr",
#                              "--enable-xfixes",
#                              "--enable-xcomposite",
#                              "--enable-xdamage",
#                              "--enable-x11-backend",
#                              "--enable-wayland-backend" ],
#             "cleanup-platform": [
#                 "/bin/gtk3-*",
#                 "/bin/gtk-builder-tool",
#                 "/bin/gtk-encode-symbolic-svg"
#             ],
#             "ensure-writable": ["/lib/*/gtk-3.0/*/immodules.cache"],
#             "sources": [
#                 {
#                     "type": "git",
#                     "url": "https://gitlab.gnome.org/GNOME/gtk.git",
#                     "branch": "gtk-3-22"
#                 }
#             ]

# # NOTE: originally from gstreamer
# jhbuild run ./configure --enable-doc-installation=no --prefix=/home/pi/jhbuild --disable-gtk-doc --disable-examples --disable-x11 --disable-glx --disable-opengl && \


# left off on gst plugins again

# Install order
# gnome-common
# yelp-xsl
# yelp-tools
# cantarell-fonts
# glib
# gobject-introspection
# gsettings-desktop-schemas
# glib-networking
# vala-bootstrap
# vala
# dconf
# libpsl
# libsoup
# dbus-glib
# json-glib
# libdatrie
# libthai
# wayland-updated
# wayland-protocols-updated
# fribidi
# pango
# atk
# at-spi2-core
# at-spi2-atk
# gdk-pixbuf
# libcroco
# librsvg
# gtk2
# gtk3
# adwaita-icon-theme
# gstreamer
# opus
# gstreamer-plugins-base
# cogl
# clutter
# clutter-gst
# clutter-gtk
# gstreamer-plugins-good
# gstreamer-plugins-bad
# gstreamer-libav
# libcanberra
# libsecret
# libnotify
# gvfs
# enchant
# gcab
# gnome-themes-extra
# mozjs52
# gjs
# pcre2
# vte
# brotli
# woff2
# WebKitGTK+
# yelp
# pycairo
# pygobject
# python-gstreamer
# gcr
# ibus
