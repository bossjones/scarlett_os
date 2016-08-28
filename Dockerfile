FROM behance/docker-base:latest
MAINTAINER Malcolm Jones <bossjones@theblacktonystark.com>

# Prepare packaging environment
ENV DEBIAN_FRONTEND noninteractive

# Workaround for bug: https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=807948
RUN chmod 0777 /tmp

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
		tcl \
		tk \
	&& rm -rf /var/lib/apt/lists/*

ENV GPG_KEY 97FC712E4C024BBEA48A61ED3A5CA953F73C700D
ENV PYTHON_VERSION 3.5.2

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 8.1.2

RUN set -ex \
	&& buildDeps=' \
		tcl-dev \
		tk-dev \
	' \
	&& apt-get update && apt-get install -y $buildDeps --no-install-recommends && rm -rf /var/lib/apt/lists/* \
	\
	&& wget -O python.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" \
	&& wget -O python.tar.xz.asc "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc" \
	&& export GNUPGHOME="$(mktemp -d)" \
	&& gpg --keyserver ha.pool.sks-keyservers.net --recv-keys "$GPG_KEY" \
	&& gpg --batch --verify python.tar.xz.asc python.tar.xz \
	&& rm -r "$GNUPGHOME" python.tar.xz.asc \
	&& mkdir -p /usr/src/python \
	&& tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
	&& rm python.tar.xz \
	\
	&& cd /usr/src/python \
	&& ./configure \
		--enable-loadable-sqlite-extensions \
		--enable-shared \
	&& make -j$(nproc) \
	&& make install \
	&& ldconfig \
	\
# explicit path to "pip3" to ensure distribution-provided "pip3" cannot interfere
	&& if [ ! -e /usr/local/bin/pip3 ]; then : \
		&& wget -O /tmp/get-pip.py 'https://bootstrap.pypa.io/get-pip.py' \
		&& python3 /tmp/get-pip.py "pip==$PYTHON_PIP_VERSION" \
		&& rm /tmp/get-pip.py \
	; fi \
# we use "--force-reinstall" for the case where the version of pip we're trying to install is the same as the version bundled with Python
# ("Requirement already up-to-date: pip==8.1.2 in /usr/local/lib/python3.6/site-packages")
# https://github.com/docker-library/python/pull/143#issuecomment-241032683
	&& pip3 install --no-cache-dir --upgrade --force-reinstall "pip==$PYTHON_PIP_VERSION" \
# then we use "pip list" to ensure we don't have more than one pip version installed
# https://github.com/docker-library/python/pull/100
	&& [ "$(pip list |tac|tac| awk -F '[ ()]+' '$1 == "pip" { print $2; exit }')" = "$PYTHON_PIP_VERSION" ] \
	\
	&& find /usr/local -depth \
		\( \
			\( -type d -a -name test -o -name tests \) \
			-o \
			\( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
		\) -exec rm -rf '{}' + \
	&& apt-get purge -y --auto-remove $buildDeps \
	&& rm -rf /usr/src/python ~/.cache

# make some useful symlinks that are expected to exist
RUN cd /usr/local/bin \
	&& { [ -e easy_install ] || ln -s easy_install-* easy_install; } \
	&& ln -s idle3 idle \
	&& ln -s pydoc3 pydoc \
	&& ln -s python3 python \
	&& ln -s python3-config python-config

RUN pip3 install virtualenv virtualenvwrapper ipython numpy

# base_vars:
#   PYTHON_VERSION_MAJOR: '3'
#   PYTHON_VERSION: '3.5'
#   GSTREAMER: '1.0'
#   USER: 'pi'
#   USER_HOME: '/home/pi'
#   LANGUAGE_ID: 1473
#   GITHUB_BRANCH: "master"
#   GITHUB_REPO_NAME: "scarlett_os"
#   GITHUB_REPO_ORG: "bossjones"
#
# virtualenv_vars:
#   MAIN_DIR: "{{ base_vars.USER_HOME }}/dev/bossjones-github/{{ base_vars.GITHUB_REPO_NAME }}"
#   VIRT_ROOT: "{{ base_vars.USER_HOME }}/.virtualenvs/{{ base_vars.GITHUB_REPO_NAME }}"
#
# build_vars:
#   PKG_CONFIG_PATH: "{{ virtualenv_vars.VIRT_ROOT }}/lib/pkgconfig"
#   LD_LIBRARY_PATH: "{{ virtualenv_vars.VIRT_ROOT }}/lib"
#   GST_PLUGIN_PATH: "{{ virtualenv_vars.VIRT_ROOT }}/lib/gstreamer-{{ base_vars.GSTREAMER }}"
#
# scarlett_vars:
#   SCARLETT_CONFIG: "{{ virtualenv_vars.MAIN_DIR }}/tests/fixtures/.scarlett"
#   SCARLETT_HMM: "{{ virtualenv_vars.MAIN_DIR }}/.virtualenvs/{{ base_vars.GITHUB_REPO_NAME }}/share/pocketsphinx/model/en-us/en-us"
#   SCARLETT_LM: "{{ virtualenv_vars.MAIN_DIR }}/tests/fixtures/lm/{{ base_vars.LANGUAGE_ID }}.lm"
#   SCARLETT_DICT: "{{ virtualenv_vars.MAIN_DIR }}/tests/fixtures/dict/{{ base_vars.LANGUAGE_ID }}.dic"


# RUN
#
# export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
# export WORKON_HOME={{ virtualenv_vars.VIRT_ROOT }}
# source /usr/local/bin/virtualenvwrapper.sh
# mkvirtualenv --system-site-packages scarlett_os

ENV PYTHON_VERSION_MAJOR '3'
ENV GSTREAMER '1.0'
ENV USER 'pi'
ENV USER_HOME "/home/${USER}"
ENV LANGUAGE_ID 1473
ENV GITHUB_BRANCH "master"
ENV GITHUB_REPO_NAME 'scarlett_os'
ENV GITHUB_REPO_ORG 'bossjones'
ENV PI_HOME '/home/pi'
ENV MAIN_DIR '${PI_HOME}/dev/${GITHUB_REPO_ORG}-github/${GITHUB_REPO_NAME}'
ENV VIRT_ROOT '${PI_HOME}/.virtualenvs/${GITHUB_REPO_NAME}'
ENV PKG_CONFIG_PATH '${PI_HOME}/.virtualenvs/${GITHUB_REPO_NAME}/lib/pkgconfig'
ENV SCARLETT_CONFIG '${PI_HOME}/dev/${GITHUB_REPO_ORG}-github/${GITHUB_REPO_NAME}/tests/fixtures/.scarlett'
ENV SCARLETT_HMM '${PI_HOME}/dev/${GITHUB_REPO_ORG}-github/${GITHUB_REPO_NAME}/.virtualenvs/${GITHUB_REPO_NAME}/share/pocketsphinx/model/en-us/en-us'
ENV SCARLETT_LM '${PI_HOME}/dev/${GITHUB_REPO_ORG}-github/${GITHUB_REPO_NAME}/tests/fixtures/lm/${LANGUAGE_ID}.lm'
ENV SCARLETT_DICT '${PI_HOME}/dev/${GITHUB_REPO_ORG}-github/${GITHUB_REPO_NAME}/tests/fixtures/dict/${LANGUAGE_ID}.dic'
ENV LD_LIBRARY_PATH '${PI_HOME}/.virtualenvs/${GITHUB_REPO_NAME}/lib'
ENV GST_PLUGIN_PATH '${PI_HOME}/.virtualenvs/${GITHUB_REPO_NAME}/lib/gstreamer-${GSTREAMER}'
ENV PYTHON '/usr/local/bin/python3'
ENV PYTHON_VERSION '3.5'
ENV VIRTUALENVWRAPPER_PYTHON '/usr/local/bin/python3'
ENV VIRTUALENVWRAPPER_VIRTUALENV '/usr/local/bin/virtualenv'
ENV VIRTUALENVWRAPPER_SCRIPT '/usr/local/bin/virtualenvwrapper.sh'
ENV PYTHONSTARTUP '${USER_HOME}/.pythonrc'
ENV PIP_DOWNLOAD_CACHE '${USER_HOME}/.pip/cache'
ENV WORKON_HOME '${VIRT_ROOT}'

RUN set -xe \
    && useradd -d ${PI_HOME} -m -r -g ${USER} ${USER} \
    && groupadd -r ${USER} \
    && usermod -a -G ${USER} ${USER} \
    && mkdir -p ${PI_HOME}/dev/${GITHUB_REPO_ORG}-github \
    && chown -hR ${USER}:${USER} ${PI_HOME}/dev/${GITHUB_REPO_ORG}-github \
    && echo '${USER}     ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers \
    && echo '%${USER}     ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

USER ${USER}

RUN /bin/bash -c "source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv --system-site-packages ${GITHUB_REPO_NAME}"

# RUN python3 -m venv /.venv && \
#     /bin/bash -c "source /.venv/bin/activate"

# Clean up
RUN apt-get autoclean -y && \
    apt-get autoremove -y && \
    rm -rf /tmp/* /var/tmp/* && \
    rm -rf /var/lib/apt/lists/*

# Layer customizations over existing structure
COPY ./container/root /

# Ensure application code makes it into the /app directory
COPY ./ /app/

RUN /bin/bash -c "source /usr/local/bin/virtualenvwrapper.sh && workon ${GITHUB_REPO_NAME} && pip install -r /app/requirements.txt"

RUN /bin/bash -c "source /usr/local/bin/virtualenvwrapper.sh && workon ${GITHUB_REPO_NAME} && pip install -r /app/requirements_dev.txt"

CMD ["/bin/bash", "/run.sh"]
