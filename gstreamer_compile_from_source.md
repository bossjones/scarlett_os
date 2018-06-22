source: https://gist.github.com/Brainiarc7/9f9b3de1246c0316f2a273c80841cadc

# Guide: How to build gstreamer from source on Ubuntu 16.04 for loading via the modules system

Build gstreamer from source (git checkouts):
--------------------------------------------

Install build dependencies:

    sudo apt-get install gtk-doc-tools liborc-0.4-0 liborc-0.4-dev libvorbis-dev libcdparanoia-dev libcdparanoia0 cdparanoia libvisual-0.4-0 libvisual-0.4-dev libvisual-0.4-plugins libvisual-projectm vorbis-tools vorbisgain libopus-dev libopus-doc libopus0 libopusfile-dev libopusfile0 libtheora-bin libtheora-dev libtheora-doc libvpx-dev libvpx-doc libvpx3 libqt5gstreamer-1.0-0 libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev libflac++-dev libavc1394-dev libraw1394-dev libraw1394-tools libraw1394-doc libraw1394-tools libtag1-dev libtagc0-dev libwavpack-dev wavpack

**Extras:**



    sudo apt-get install libfontconfig1-dev libfreetype6-dev libx11-dev libxext-dev libxfixes-dev libxi-dev libxrender-dev libxcb1-dev libx11-xcb-dev libxcb-glx0-dev

Additionally, if you do not configure with -qt-xcb (for QT only with gstreamer), you should also install these development packages:

    sudo apt-get install libxcb-keysyms1-dev libxcb-image0-dev libxcb-shm0-dev libxcb-icccm4-dev libxcb-sync0-dev libxcb-xfixes0-dev libxcb-shape0-dev libxcb-randr0-dev libxcb-render-util0-dev

Some of these packages depend on others in this list, so installing one may cause others to be automatically installed. Other distributions may provide system packages with similar names.

Basic Qt dependencies:

    sudo apt-get install libfontconfig1-dev libdbus-1-dev libfreetype6-dev libudev-dev


Dependencies for multimedia:

    sudo apt-get install libasound2-dev libavcodec-dev libavformat-dev libswscale-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev gstreamer-tools gstreamer0.10-plugins-good gstreamer0.10-plugins-bad

QtWebKit dependencies:

    sudo apt-get install libicu-dev libsqlite3-dev libxslt1-dev libssl-dev

Navigate to the source directory needed for the build:

Check out the sources, one by one:


    git clone git://anongit.freedesktop.org/git/gstreamer/gstreamer
    git clone git://anongit.freedesktop.org/git/gstreamer/gst-plugins-base
    git clone git://anongit.freedesktop.org/git/gstreamer/gst-plugins-good
    git clone git://anongit.freedesktop.org/git/gstreamer/gst-plugins-bad
    git clone git://anongit.freedesktop.org/git/gstreamer/gst-plugins-ugly
    git clone git://anongit.freedesktop.org/git/gstreamer/gst-libav
    git clone git://anongit.freedesktop.org/git/gstreamer/gst-python
    git clone https://cgit.freedesktop.org/gstreamer/gstreamer-vaapi

Prepare the target directories where the binaries will reside:

    sudo mkdir -p /apps/gstreamer/git
    sudo mkdir -p /apps/gst-plugins-base/git
    sudo mkdir -p /apps/gst-plugins-good/git
    sudo mkdir -p /apps/gst-plugins-bad/git
    sudo mkdir -p /apps/gst-plugins-ugly/git
    sudo mkdir -p /apps/gst-libav/git
    sudo mkdir -p /apps/gst-python/git
    sudo mkdir -p /apps/gstreamer-vaapi/git



Write an initial module file for gstreamer, to be expanded on completion when dependencies are built:

    #%Module1.0
    #####################################################################
    ##
    ## gstreamer Modulefile
    ## by Dennis Mungai on December 30 2016
    ##
    ## Locally built package
    ##
    ## Target: QT5
    ##
    set appname             gstreamer
    set version             git
    set prefix              /apps/${appname}/${version}/

    set url "https://gstreamer.freedesktop.org/"
    set msg "This module adds gstreamer v$version to various paths\n\nGstreamer Official Site: $url\n"

    proc ModulesHelp { } {
            puts stderr "$msg"
    }

    module-whatis   "$msg"

    conflict        gstreamer

    prepend-path    PATH                         ${prefix}/bin
    prepend-path    LD_LIBRARY_PATH              ${prefix}/lib
    prepend-path    PKG_CONFIG_PATH              ${prefix}lib/pkgconfig



Now, to build:

Check out all sources above and navigate to each build directory:



    cd gstreamer
    git pull
    ./autogen.sh
    ./configure --prefix=/apps/gstreamer/git --enable-gtk-doc
    time make -j$(nproc)
    sudo make install
    cd ..

    cd gst-plugins-base
    git pull
    module load gstreamer/git
    ./autogen.sh --prefix=/apps/gst-plugins-base/git --enable-gtk-doc --enable-iso-codes --enable-orc
    time make -j$(nproc)
    sudo make install
    cd ..

    cd gst-plugins-good
    git pull
    module load gstreamer/git
    ./autogen.sh --prefix=/apps/gst-plugins-good/git --enable-gtk-doc --enable-orc
    time make -j$(nproc)
    sudo make install
    cd ..

    cd gst-plugins-ugly
    git pull
    ./autogen.sh --prefix=/apps/gst-plugins-ugly/git --enable-gtk-doc --enable-orc
    time make -j$(nproc)
    sudo make install
    cd ..

    cd gst-libav
    git pull
    ./autogen.sh --prefix=/apps/gst-libav/git --enable-gtk-doc --enable-orc
    time make -j$(nproc)
    sudo make install
    cd ..

    cd gst-plugins-bad
    git pull
    ./autogen.sh --prefix=/apps/gst-plugins-bad/git --enable-gtk-doc --enable-orc --with-cuda-prefix=/usr/local/cuda
    time make -j$(nproc)
    sudo make install
    cd ..

To build python bindings:

    cd gst-python
    module load gstreamer/git
    git pull
    ./autogen.sh
    ./configure --prefix=/apps/gstreamer/git
    time make -j$(nproc)
    sudo make install
    cd ..


**Create all modules for the installed packages:**

For the main gstreamer modulefile:

    module show gstreamer/git
    -------------------------------------------------------------------
    /usr/share/modules/modulefiles/gstreamer/git:

    module-whatis	 This module adds gstreamer vgit to various paths

    Gstreamer Official Site: https://gstreamer.freedesktop.org/

    conflict	 gstreamer
    prepend-path	 PATH /apps/gstreamer/git//bin
    prepend-path	 LD_LIBRARY_PATH /apps/gstreamer/git//lib
    prepend-path	 PKG_CONFIG_PATH /apps/gstreamer/git/lib/pkgconfig
    -------------------------------------------------------------------

**Content:**


    #%Module1.0
    #####################################################################
    ##
    ## gstreamer Modulefile
    ## by Dennis Mungai on December 30 2016
    ##
    ##
    ##
    ##
    ##
    set appname             gstreamer
    set version             git
    set prefix              /apps/${appname}/${version}/

    set url "https://gstreamer.freedesktop.org/"
    set msg "This module adds gstreamer v$version to various paths\n\nGstreamer Official Site: $url\n"

    proc ModulesHelp { } {
            puts stderr "$msg"
    }

    module-whatis   "$msg"

    conflict        gstreamer

    prepend-path    PATH                         ${prefix}/bin
    prepend-path    LD_LIBRARY_PATH              ${prefix}/lib
    prepend-path    PKG_CONFIG_PATH              ${prefix}lib/pkgconfig

    #No conflict needed, omit it here.

    # Make sure gstreamer-plugins-base/git is loaded
    # This was compiled against gstreamer-plugins-base/git
    if { ![is-loaded gstreamer-plugins-base/git] } {
        module load gstreamer-plugins-base/git
    }

    # Make sure gstreamer-plugins-good/git is loaded
    # This was compiled against gstreamer-plugins-good/git
    if { ![is-loaded gstreamer-plugins-good/git] } {
        module load gstreamer-plugins-good/git
    }

    # Make sure gstreamer-plugins-ugly/git is loaded
    # This was compiled against gstreamer-plugins-ugly/git
    if { ![is-loaded gstreamer-plugins-ugly/git] } {
        module load gstreamer-plugins-ugly/git
    }

    # Make sure gstreamer-plugins-ugly/git is loaded
    # This requires gstreamer-plugins-ugly/git
    if { ![is-loaded gstreamer-plugins-ugly/git] } {
        module load gstreamer-plugins-ugly/git
    }

    #Make sure gstreamer-libav/git is loaded
    #Some plugins require gstreamer-libav/git
    if { ![is-loaded gstreamer-libav/git] } {
        module load gstreamer-libav/git
    }


**gstreamer-plugins-base/git modulefile:**

    module show gstreamer-plugins-base/git
    -------------------------------------------------------------------
    /usr/share/modules/modulefiles/gstreamer-plugins-base/git:

    module-whatis	 This module adds gstreamer-plugins-base vgit to various paths

    Gstreamer Official Site: https://gstreamer.freedesktop.org/

    prepend-path	 PATH /apps/gst-plugins-base/git//bin
    prepend-path	 LD_LIBRARY_PATH /apps/gst-plugins-base/git//lib
    prepend-path	 PKG_CONFIG_PATH /apps/gst-plugins-base/git/lib/pkgconfig
    -------------------------------------------------------------------

**Content:**

    #%Module1.0
    #####################################################################
    ##
    ## gstreamer-plugins-base Modulefile
    ## by Dennis Mungai on December 30 2016
    ##
    set appname             gst-plugins-base
    set version             git
    set prefix              /apps/${appname}/${version}/

    set url "https://gstreamer.freedesktop.org/"
    set msg "This module adds gstreamer-plugins-base v$version to various paths\n\nGstreamer Official Site: $url\n"

    proc ModulesHelp { } {
            puts stderr "$msg"
    }

    module-whatis   "$msg"

    #Omit plugins

    prepend-path    PATH                         ${prefix}/bin
    prepend-path    LD_LIBRARY_PATH              ${prefix}/lib
    prepend-path    PKG_CONFIG_PATH              ${prefix}lib/pkgconfig

**gstreamer-plugins-good/git modulefile:**


    module show gstreamer-plugins-good/git
    -------------------------------------------------------------------
    /usr/share/modules/modulefiles/gstreamer-plugins-good/git:

    module-whatis	 This module adds gstreamer-plugins-good vgit to various paths

    Gstreamer Official Site: https://gstreamer.freedesktop.org/

    prepend-path	 PATH /apps/gst-plugins-good/git//bin
    prepend-path	 LD_LIBRARY_PATH /apps/gst-plugins-good/git//lib
    prepend-path	 PKG_CONFIG_PATH /apps/gst-plugins-good/git/lib/pkgconfig
    -------------------------------------------------------------------

**Module content:**

    #%Module1.0
    #####################################################################
    ##
    ## gstreamer-plugins-good Modulefile
    ## by Dennis Mungai on December 30 2016
    ##
    set appname             gst-plugins-good
    set version             git
    set prefix              /apps/${appname}/${version}/

    set url "https://gstreamer.freedesktop.org/"
    set msg "This module adds gstreamer-plugins-good v$version to various paths\n\nGstreamer Official Site: $url\n"

    proc ModulesHelp { } {
            puts stderr "$msg"
    }

    module-whatis   "$msg"

    #No conflict needed

    prepend-path    PATH                         ${prefix}/bin
    prepend-path    LD_LIBRARY_PATH              ${prefix}/lib
    prepend-path    PKG_CONFIG_PATH              ${prefix}lib/pkgconfig

**gstreamer-plugins-ugly/git module:**


    module show gstreamer-plugins-ugly/git
    -------------------------------------------------------------------
    /usr/share/modules/modulefiles/gstreamer-plugins-ugly/git:

    module-whatis	 This module adds gstreamer-plugins-ugly vgit to various paths

    Gstreamer Official Site: https://gstreamer.freedesktop.org/

    prepend-path	 PATH /apps/gst-plugins-ugly/git//bin
    prepend-path	 LD_LIBRARY_PATH /apps/gst-plugins-ugly/git//lib
    prepend-path	 PKG_CONFIG_PATH /apps/gst-plugins-ugly/git/lib/pkgconfig
    -------------------------------------------------------------------

**Content:**

    #%Module1.0
    #####################################################################
    ##
    ## gstreamer-plugins-ugly Modulefile
    ## by Dennis Mungai on December 30 2016
    ##
    set appname             gst-plugins-ugly
    set version             git
    set prefix              /apps/${appname}/${version}/

    set url "https://gstreamer.freedesktop.org/"
    set msg "This module adds gstreamer-plugins-ugly v$version to various paths\n\nGstreamer Official Site: $url\n"

    proc ModulesHelp { } {
            puts stderr "$msg"
    }

    module-whatis   "$msg"

    #No conflict needed

    prepend-path    PATH                         ${prefix}/bin
    prepend-path    LD_LIBRARY_PATH              ${prefix}/lib
    prepend-path    PKG_CONFIG_PATH              ${prefix}lib/pkgconfig


**gstreamer-libav module:**

    module show gstreamer-libav/git
    -------------------------------------------------------------------
    /usr/share/modules/modulefiles/gstreamer-libav/git:

    module-whatis	 This module adds gstreamer-plugins-base vgit to various paths

    Gstreamer Official Site: https://gstreamer.freedesktop.org/

    prepend-path	 PATH /apps/gstreamer-libav/git//bin
    prepend-path	 LD_LIBRARY_PATH /apps/gstreamer-libav/git//lib
    prepend-path	 PKG_CONFIG_PATH /apps/gstreamer-libav/git/lib/pkgconfig
    -------------------------------------------------------------------



**Module content:**

    #%Module1.0
    #####################################################################
    ##
    ## gstreamer-libav Modulefile
    ## by Dennis Mungai on December 30 2016
    ##
    set appname             gstreamer-libav
    set version             git
    set prefix              /apps/${appname}/${version}/

    set url "https://gstreamer.freedesktop.org/"
    set msg "This module adds gstreamer-plugins-base v$version to various paths\n\nGstreamer Official Site: $url\n"

    proc ModulesHelp { } {
            puts stderr "$msg"
    }

    module-whatis   "$msg"

    #No conflict

    prepend-path    PATH                         ${prefix}/bin
    prepend-path    LD_LIBRARY_PATH              ${prefix}/lib
    prepend-path    PKG_CONFIG_PATH              ${prefix}lib/pkgconfig

Now, you've successfully deployed gstreamer in a custom location for use.

Next gist: Building QT5 with this version of gstreamer baked in.



















