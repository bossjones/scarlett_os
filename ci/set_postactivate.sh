echo -e "\n[ Write to postactivate ]"
cat << EOF > $HOME/.virtualenvs/scarlett_os/bin/postactivate
# FOR VIRTUALENVS
export GSTREAMER=1.0
export PI_HOME=$HOME
export MAIN_DIR=$HOME/dev/bossjones-github/scarlett_os
export VIRT_ROOT=$HOME/.virtualenvs/scarlett_os
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/dev


# export PKG_CONFIG_PATH=$PI_HOME/.virtualenvs/scarlett_os/lib/pkgconfig
export SCARLETT_CONFIG=$HOME/dev/bossjones-github/scarlett_os/tests/fixtures/.scarlett
export SCARLETT_HMM=$HOME/.virtualenvs/scarlett_os/share/pocketsphinx/model/en-us/en-us
export SCARLETT_LM=$HOME/dev/bossjones-github/scarlett_os/tests/fixtures/lm/1473.lm
export SCARLETT_DICT=$HOME/dev/bossjones-github/scarlett_os/tests/fixtures/dict/1473.dic

# for GST PLUGINS
export LD_LIBRARY_PATH=$HOME/.virtualenvs/scarlett_os/lib
export GST_PLUGIN_PATH=${PREFIX}/lib/gstreamer-1.0

export PYTHON=/usr/bin/python3
EOF

echo -e "\n[ Chmod +x postactivate ]"
chmod +x $HOME/.virtualenvs/scarlett_os/bin/postactivate

workon scarlett_os
