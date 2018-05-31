#!/usr/bin/env bash

# [[ "$TRACE" ]] && set -x
if test "$TRACE" = "1"; then set -x; fi

if test "z$1" = "z"; then echo "Please pass in a networking interface name, eg 'en0' " && exit 1; fi

_INTERFACE=$1

# FIXME: Make me into the end all starter script

# SOURCE: https://hub.docker.com/r/kayvan/scidvspc/

DIR=$(basename $PWD)

n_procs=()

export NON_ROOT_USER="developer"
export _UID=$(id -u)
export _GID=$(id -g)
export DOCKER_DEVELOPER_CHROOT=".docker-${NON_ROOT_USER}-chroot"
export DOCKER_DEVELOPER_CHROOT_FULL_PATH=${HOME}/${DOCKER_DEVELOPER_CHROOT}
export _HOST_IP=$(ifconfig ${_INTERFACE} | grep "inet "| awk '{print $2}')
export DISPLAY_MAC=$_HOST_IP:1
export USERNAME=scarlettos
export CONTAINER_NAME=docker-gnome-builder-meson
export NON_ROOT_USER_HOME_DIR=/home/${NON_ROOT_USER}

export LC_ALL="en_US.UTF-8"
export LANG="en_US.UTF-8"
export LANGUAGE="en_US.UTF-8"
export C_CTYPE="en_US.UTF-8"
export LC_NUMERIC=
export LC_TIME="en_US.UTF-8"

docker run \
  --privileged \
  --cap-add=ALL \
  -i \
  --tty \
  --net host \
  -e TRACE=1 \
  -e HOME=${NON_ROOT_USER_HOME_DIR} \
  -e UID \
  -e GID \
  -e LC_ALL \
  -e LANG \
  -e C_CTYPE \
  -e LC_NUMERIC \
  -e LC_TIME \
  -e DISPLAY=${DISPLAY_MAC} \
  -e XAUTHORITY=/tmp/xauth \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/.Xauthority:/tmp/xauth \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $DOCKER_DEVELOPER_CHROOT_FULL_PATH:$HOME:rw \
  -v /run/user/${UID}/pulse:/run/pulse \
  \
  -v $PWD:/home/$NON_ROOT_USER/Projects/$DIR \
  -v /usr/share/fonts:/usr/local/share/fonts:ro \
  -v /usr/share/themes:/usr/local/share/themes:ro \
  -v /usr/share/icons:/usr/local/share/icons:ro \
  -w /home/$NON_ROOT_USER/$DIR \
  --entrypoint "/app/bin/entrypoint-dbus-bash" \
  $USERNAME/$CONTAINER_NAME:latest /app/bin/docker-entrypoint.sh
