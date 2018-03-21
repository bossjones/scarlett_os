#!/usr/bin/env bash

# shellcheck disable=2086
# shellcheck shell=bash

# NOTE: Only Run this if we aren't using jhbuild!!!!!!!!
# NOTE: Only Run this if we aren't using jhbuild!!!!!!!!
# NOTE: Only Run this if we aren't using jhbuild!!!!!!!!
# NOTE: Only Run this if we aren't using jhbuild!!!!!!!!
# NOTE: Only Run this if we aren't using jhbuild!!!!!!!!
# NOTE: Only Run this if we aren't using jhbuild!!!!!!!!


DEST_DIR=$(ls -d ${VIRTUAL_ENV}/lib/pyth*/site-packages)
DIST_PKGS=/usr/lib/python3/dist-packages

echo ${DEST_DIR}

for F in cairo dbus _dbus_bindings.cpython-33m-x86_64-linux-gnu.so _dbus_glib_bindings.cpython-33m-x86_64-linux-gnu.so gi
do
	if [ -h ${DEST_DIR}/${F} ]; then
		rm ${DEST_DIR}/${F}
	fi
	ln -s ${DIST_PKGS}/${F} ${DEST_DIR}/${F}
done
