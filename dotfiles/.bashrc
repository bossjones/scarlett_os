#!/usr/bin/env bash

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

source $HOME/.bashrc

# Set my editor and git editor
export EDITOR="/usr/bin/vim -w"
export GIT_EDITOR='/usr/bin/vim -w'

# virtualenv
export WORKON_HOME=/home/pi/.virtualenvs/scarlett_os
export PROJECT_HOME=$HOME/dev
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
export VIRTUALENVWRAPPER_SCRIPT=/usr/local/bin/virtualenvwrapper.sh
source /usr/local/bin/virtualenvwrapper.sh
export PYTHONSTARTUP=~/.pythonrc
export PIP_DOWNLOAD_CACHE=$HOME/.pip/cache

# Case-insensitive globbing (used in pathname expansion)
shopt -s nocaseglob

# load the last 5000 lines into memory
HISTSIZE=50000000
# save 10000 lines to disk
HISTFILESIZE=$HISTSIZE
# Append to the Bash history file, rather than overwriting it
shopt -s histappend
# have bash immediately add commands to our history instead of waiting for the end of each session
export PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND"

# Autocorrect typos in path names when using `cd`
shopt -s cdspell

# Enable some Bash 4 features when possible:
# * `autocd`, e.g. `**/qux` will enter `./foo/bar/baz/qux`
# * Recursive globbing, e.g. `echo **/*.txt`
for option in autocd globstar; do
  shopt -s "$option" 2> /dev/null
done
