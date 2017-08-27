#!/usr/bin/execlineb -S0

# s6-setuidgid executes a program as another user. ( s6-setuidgid account prog... )
# s6-envuidgid potentially sets the UID, GID and GIDLIST environment variables according to the options and arguments it is given; then it executes into another program.
# s6-applyuidgid executes a program with reduced privileges.
# s6-envdir changes its environment, then executes into another program.

# foreground { s6-envuidgid pi s6-env }
# foreground { s6-env }
# foreground { s6-envuidgid pi id }

s6-envuidgid pi
s6-setuidgid pi
# exec s6-envdir "$XDG_RUNTIME_DIR"/env exec -a "${SHELL##*/}" "$SHELL"
# s6-envdir "$XDG_RUNTIME_DIR"/env
# exec -a /bin/bash /bin/bash -l -c exec "$@"
# exec -a /bin/bash /bin/bash -l -c exec "sudo su - pi $@"

# ------------------------------------------------------------------------
# NOTE: THIS ONE WORKED
exec -a /bin/bash /bin/bash -l
# result: pi  ⎇  feature-dev-container {5} ?:2  ~/dev/bossjones-github/scarlett_os/container/root
# ------------------------------------------------------------------------




# --------------------------------------------------------------------------------
# multisubstitute {
#   importas HOME HOME
#   importas XDG_RUNTIME_DIR XDG_RUNTIME_DIR
#   importas UID UID
#   importas GID GID
#   importas PATH PATH
#   importas ENABLE_PYTHON3 ENABLE_PYTHON3
#   importas ENABLE_GTK ENABLE_GTK
#   importas PREFIX PREFIX
#   importas JHBUILD JHBUILD
#   importas LD_LIBRARY_PATH LD_LIBRARY_PATH
#   importas PYTHONPATH PYTHONPATH
# }
# --------------------------------------------------------------------------------

# foreground { s6-echo " [run] TEST_PATH is ${TEST_PATH}" }
# foreground { s6-echo " [run] HOME is ${HOME}" }
# foreground { s6-echo " [run] XDG_RUNTIME_DIR is ${XDG_RUNTIME_DIR}" }
# foreground { s6-echo " [run] PATH is ${PATH}" }

# --------------------------------------------------------------------------------
# foreground { s6-env }
# multisubstitute {
#     import -D "1000" UID
#     import -D "1000" GID
# }
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# s6-applyuidgid -u 1000 -g 1000 w
# s6-envuidgid pi s6-chown -U ${XDG_RUNTIME_DIR}
# s6-applyuidgid -u 1000 -g 1000
# s6-applyuidgid -u 1000 -g 1000 umask 022 ${HOME}/.local/bin/env-setup
# s6-applyuidgid -u 1000 -g 1000

# set -e

# sudo find \( -name __pycache__ -o -name '*.pyc' \) | sudo xargs rm -rf
# sudo chown pi:pi -R /home/pi/dev

# exec "$@"
# --------------------------------------------------------------------------------

# echo "[run] Starting Pi."
# home="$(echo ~pi)"

# find \( -name __pycache__ -o -name '*.pyc' \) | xargs rm -rf
# chown $NOT_ROOT_USER:$NOT_ROOT_USER -R /home/$NOT_ROOT_USER/dev

# exec s6-setuidgid $NOT_ROOT_USER "$@"
