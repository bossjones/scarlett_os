#!/usr/bin/env bash

export MAIN_DIR=$(pwd)
export GSTREAMER=1.0
export ENABLE_PYTHON3=yes
# from jhbuild
export CFLAGS="-fPIC -O0 -ggdb -fno-inline -fno-omit-frame-pointer"
# JHBuild detects too many cores
export MAKEFLAGS="-j4"
# JHBuild related variables
export PREFIX="${HOME}/jhbuild"
export JHBUILD="${HOME}/gnome"

# NOTE: taken from: jhbuild-session
export PATH=${PREFIX}/bin:${PREFIX}/sbin:${PATH}
export LD_LIBRARY_PATH=${PREFIX}/lib:${LD_LIBRARY_PATH}
export PYTHONPATH=${PREFIX}/lib/python3.5/site-packages:/usr/lib/python3.5/site-packages
export PKG_CONFIG_PATH=${PREFIX}/lib/pkgconfig:${PREFIX}/share/pkgconfig:/usr/lib/pkgconfig
export XDG_DATA_DIRS=${PREFIX}/share:/usr/share
export XDG_CONFIG_DIRS=${PREFIX}/etc/xdg

if [ '$GSTREAMER' = '1.0'   ]; then sudo add-apt-repository -y ppa:ricotz/testing; fi
if [ '$GSTREAMER' = '1.0'   ]; then sudo add-apt-repository -y ppa:gnome3-team/gnome3; fi
if [ '$GSTREAMER' = '1.0'   ]; then sudo add-apt-repository -y ppa:gnome3-team/gnome3-staging; fi

sudo add-apt-repository -y ppa:pitti/systemd-semaphore
sudo apt-get update -qq

sudo apt-get update -qq
sudo apt-get install -y libz-dev libbz2-dev gstreamer$GSTREAMER-tools libgstreamer$GSTREAMER-dev libgstreamer-plugins-base$GSTREAMER-dev libgstreamer-plugins-bad$GSTREAMER-dev
if [ '$GSTREAMER' = '1.0'   ]; then sudo apt-get install -y libgstreamer-plugins-good$GSTREAMER-dev; fi
sudo apt-get update -qq
sudo apt-get install -y gir1.2-gst-plugins-base-1.0 gir1.2-gstreamer-1.0 graphviz-dev gstreamer1.0-plugins-good gstreamer1.0-plugins-bad python-gst-1.0
sudo apt-get install -qq python3-gi
sudo apt-get install -qq python-gst-1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-bad gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-libav libsndfile1-dev libasound2-dev libgstreamer-plugins-base1.0-dev python-numpy python-scipy
sudo apt-get -y install automake gir1.2-gst-plugins-base-1.0 gir1.2-gstreamer-1.0 gstreamer1.0-libav gstreamer1.0-plugins-bad gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-tools libasound2-dev libgstreamer-plugins-base1.0-dev libsndfile1-dev python python-dev python-gi python-gst-1.0 python-gst-1.0 python-imaging python-lxml python-numpy python-scipy python-virtualenv python3-gi
sudo apt-get -y install libsdl2-dev libsdl2-ttf-dev libsdl2-image-dev libsdl2-mixer-dev gnome-common;
sudo apt-get -y install libgstreamer1.0-dev gstreamer1.0-alsa gstreamer1.0-plugins-base;
sudo apt-get -y install python-dev libsmpeg-dev libswscale-dev libavformat-dev libavcodec-dev libjpeg-dev libtiff4-dev libX11-dev libmtdev-dev;
sudo apt-get -y install python-setuptools build-essential libgl1-mesa-dev libgles2-mesa-dev;
sudo apt-get -y install xvfb pulseaudio;
if [ "$TRAVIS_OS_NAME" = "linux" ]; then sudo add-apt-repository 'deb http://us.archive.ubuntu.com/ubuntu/ trusty main restricted universe multiverse'; fi
if [ "$TRAVIS_OS_NAME" = "linux" ]; then sudo add-apt-repository 'deb http://us.archive.ubuntu.com/ubuntu/ trusty-updates main restricted universe multiverse'; fi
if [ "$TRAVIS_OS_NAME" = "linux" ]; then sudo apt-get update -qq; sudo apt-get install -qq pkg-config; fi
sudo apt-get -y update
sudo apt-get -y install ubuntu-restricted-extras
sudo apt-get -y install libfftw3-dev
sudo apt-get install -qq python3-dev;
sudo apt-get install -qq python3-cairo-dev;
sudo apt-get install -qq python3-gi;
sudo apt-get install -qq gnome-common
sudo apt-get install -qq gtk-doc-tools
sudo apt-get install -qq libgtk-3-dev
sudo apt-get install -qq libgirepository1.0-dev
sudo apt-get install -qq libmount-dev
sudo apt-get install -qq cvs
sudo apt-get update -q
sudo apt-get install --no-install-recommends -y xvfb gir1.2-gtk-3.0 $(echo $PACKAGES)
sudo apt-get install -qq build-essential
sudo apt-get install -qq git flex
sudo apt-get install -qq gettext xsltproc docbook-xml docbook-xsl
sudo apt-get install -qq apt-file autopoint
# install yacc / lex
sudo apt-get install -qq byacc flex
sudo apt-get install -qq bison
sudo apt-get install -qq docbook-xsl build-essential git-core python-libxml2
sudo apt-get install -qq --no-install-recommends \
    build-essential docbook-xsl flex bison cvs gperf cmake valac g++ \
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
sudo apt-get install -qq apt-file
sudo apt-file update
