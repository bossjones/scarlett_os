#!/usr/bin/env bash

export MAIN_DIR=$(pwd)
export VIRT_ROOT=/home/travis/virtualenv/python$TRAVIS_PYTHON_VERSION
export PKG_CONFIG_PATH=$VIRT_ROOT/lib/pkgconfig
export SCARLETT_CONFIG=$MAIN_DIR/tests/fixtures/.scarlett
# - export SCARLETT_HMM=$MAIN_DIR/tests/fixtures/model/hmm/en_US/hub4wsj_sc_8k
export SCARLETT_LM=$MAIN_DIR/tests/fixtures/lm/1602.lm
export SCARLETT_DICT=$MAIN_DIR/tests/fixtures/dict/1602.dic
export PYTHONIOENCODING=UTF8
export GSTREAMER=1.0
export PYTHON_VERSION=$(python -c "import sys; print('%s.%s' % sys.version_info[:2])")
export PYTHON_INC_DIR=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())")
export PYTHON_SITE_PACKAGES=$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
