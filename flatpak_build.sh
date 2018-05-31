#!/usr/bin/env bash

export NON_ROOT_USER=developer

curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash && \
    git clone https://github.com/pyenv/pyenv-virtualenvwrapper /home/${NON_ROOT_USER}/.pyenv/plugins/pyenv-virtualenvwrapper && \
    git clone https://github.com/pyenv/pyenv-pip-rehash /home/${NON_ROOT_USER}/.pyenv/plugins/pyenv-pip-rehash && \
    git clone https://github.com/pyenv/pyenv-pip-migrate /home/${NON_ROOT_USER}/.pyenv/plugins/pyenv-pip-migrate && \
    pyenv install 3.5.2

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
pyenv init - > ~/pyenv_temp
pyenv virtualenv-init - > ~/pyenv_venv_init
source ~/pyenv_temp
source ~/pyenv_venv_init
export PYENV_VIRTUALENVWRAPPER_PREFER_PYVENV="true"
export PATH="/app/bin:$PATH"

# source /home/developer/.bashrc

pyenv version 3.5.2;
mkdir -p /app/lib/python3.5/site-packages;
CFLAGS='-L/usr/lib -Lbuild/temp.linux-x86_64-3.4 -I/usr/include -I/usr/include/python3.5m/' CXX=/usr/bin/g++ CC=/usr/bin/gcc PYTHONUSERBASE=/app/ pip3.5 install --target=/app --root=/ -r requirements.txt;
CFLAGS='-L/usr/lib -Lbuild/temp.linux-x86_64-3.4 -I/usr/include -I/usr/include/python3.5m/' CXX=/usr/bin/g++ CC=/usr/bin/gcc PYTHONUSERBASE=/app/ pip3.5 install --target=/app --root=/ -r requirements_dev.txt;
CFLAGS='-L/usr/lib -Lbuild/temp.linux-x86_64-3.4 -I/usr/include -I/usr/include/python3.5m/' CXX=/usr/bin/g++ CC=/usr/bin/gcc PYTHONUSERBASE=/app/ python3.5 setup.py install --prefix=/app --root=/;
CFLAGS='-L/usr/lib -Lbuild/temp.linux-x86_64-3.4 -I/usr/include -I/usr/include/python3.5m/' CXX=/usr/bin/g++ CC=/usr/bin/gcc PYTHONUSERBASE=/app/ pip3.5 install --target=/app --root=/ -e .[test];
