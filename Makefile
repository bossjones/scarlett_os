# Copyright 2015-2016 Tony Dark Industries LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Edit this release and run "make release"
RELEASE=0.1.0

SHELL=/bin/bash

project := scarlett_os
projects := scarlett_os
username := bossjones
container_name := scarlett_os

gnome_username := scarlettos
gnome_container_name := docker-gnome-builder-meson

# label-schema spec: http://label-schema.org/rc1/

#CONTAINER_VERSION  = $(shell \cat ./VERSION | awk '{print $1}')
GIT_BRANCH              := $(shell git rev-parse --abbrev-ref HEAD)
GIT_SHA                 := $(shell git rev-parse HEAD)
BUILD_DATE              := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
FIXUID                  := $(shell id -u)
FIXGID                  := $(shell id -g)
DOCKER_IP               := $(shell echo $${DOCKER_HOST:-tcp://127.0.0.1:2376} | cut -d/ -f3 | cut -d: -f1)
CURRENT_DIR             := $(shell pwd)
MKDIR                   := mkdir
APP_WORK_DIR            := /app
ORG_NAME                := bossjones
PROJECT_NAME            := scarlett_os
REPO_NAME               := $(ORG_NAME)/$(PROJECT_NAME)
IMAGE_TAG               := $(REPO_NAME):$(GIT_SHA)
CONTAINER_NAME          := $(shell echo -n $(IMAGE_TAG) | openssl dgst -sha1 | sed 's/^.* //'  )


#################################################################################
# DOCKER_RUN_ARGS   = \
# 	-e FLIGHT_DIRECTOR_URL \
# 	-e FD_BEHAVE_DEFAULT_IMAGE \
# 	-e PYTHONUNBUFFERED=1 \
# 	-e DCOS_USER \
# 	-e DCOS_PASSWORD \
# 	-v ~/.dcos:/root/.dcos \
# 	-v ~/.docker:/root/.docker \
# 	-v $$PWD/junit-results:/junit-results \
# 	-v $$PWD:/usr/src/app \
# 	-i
# # if this session isn't interactive, then we don't want to allocate a
# # TTY, which would fail, but if it is interactive, we do want to attach
# # so that the user can send e.g. ^C through.
# INTERACTIVE := $(shell [ -t 0 ] && echo 1 || echo 0)
# ifeq ($(INTERACTIVE), 1)
# 	DOCKER_RUN_ARGS += -t
# endif
# ifneq ($(JENKINS_URL), )
# 	DOCKER_RUN_ARGS += -e BEHAVE_FORMATTER=plain.color
# endif

# MKDIR = mkdir
# PARALLEL = parallel
# PARALLEL_ARGS = -j 3 -v --results=outdir
#################################################################################

# NOTE: DEFAULT_GOAL
# source: (GNU Make - Other Special Variables) https://www.gnu.org/software/make/manual/html_node/Special-Variables.html
# Sets the default goal to be used if no
# targets were specified on the command
# line (see Arguments to Specify the Goals).
# The .DEFAULT_GOAL variable allows you to
# discover the current default goal,
# restart the default goal selection
# algorithm by clearing its value,
# or to explicitly set the default goal.
# The following example illustrates these cases:
.DEFAULT_GOAL       := help

flake8              := flake8
COV_DIRS            := $(projects:%=--cov %)
# [-s] per-test capturing method: one of fd|sys|no. shortcut for --capture=no.
# [--tb short] traceback print mode (auto/long/short/line/native/no).
# [--cov-config=path]     config file for coverage, default: .coveragerc
# [--cov=[path]] coverage reporting with distributed testing support. measure coverage for filesystem path (multi-allowed)
pytest_args         := -s --tb short --cov-config .coveragerc $(COV_DIRS) tests
pytest              := py.test $(pytest_args)
sources             := $(shell find $(projects) tests -name '*.py' | grep -v version.py | grep -v thrift_gen)

# coverage flags, these all come from here
# SOURCE: https://media.readthedocs.org/pdf/pytest-cov/latest/pytest-cov.pdf
test_args_no_xml    := --cov-report=
test_args_with_xml  := --cov-report term-missing --cov-report xml:cov.xml --cov-report html:htmlcov --cov-report annotate:cov_annotate --benchmark-skip
test_args           := --cov-report term-missing --cov-report xml --junitxml junit.xml
cover_args          := --cov-report html

.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"


define ASCILOGO
  ██████  ▄████▄   ▄▄▄       ██▀███   ██▓    ▓█████▄▄▄█████▓▄▄▄█████▓    ███▄ ▄███▓ ▄▄▄       ██ ▄█▀▓█████
▒██    ▒ ▒██▀ ▀█  ▒████▄    ▓██ ▒ ██▒▓██▒    ▓█   ▀▓  ██▒ ▓▒▓  ██▒ ▓▒   ▓██▒▀█▀ ██▒▒████▄     ██▄█▒ ▓█   ▀
░ ▓██▄   ▒▓█    ▄ ▒██  ▀█▄  ▓██ ░▄█ ▒▒██░    ▒███  ▒ ▓██░ ▒░▒ ▓██░ ▒░   ▓██    ▓██░▒██  ▀█▄  ▓███▄░ ▒███
  ▒   ██▒▒▓▓▄ ▄██▒░██▄▄▄▄██ ▒██▀▀█▄  ▒██░    ▒▓█  ▄░ ▓██▓ ░ ░ ▓██▓ ░    ▒██    ▒██ ░██▄▄▄▄██ ▓██ █▄ ▒▓█  ▄
▒██████▒▒▒ ▓███▀ ░ ▓█   ▓██▒░██▓ ▒██▒░██████▒░▒████▒ ▒██▒ ░   ▒██▒ ░    ▒██▒   ░██▒ ▓█   ▓██▒▒██▒ █▄░▒████▒
▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░░ ▒░▓  ░░░ ▒░ ░ ▒ ░░     ▒ ░░      ░ ▒░   ░  ░ ▒▒   ▓▒█░▒ ▒▒ ▓▒░░ ▒░ ░
░ ░▒  ░ ░  ░  ▒     ▒   ▒▒ ░  ░▒ ░ ▒░░ ░ ▒  ░ ░ ░  ░   ░        ░       ░  ░      ░  ▒   ▒▒ ░░ ░▒ ▒░ ░ ░  ░
░  ░  ░  ░          ░   ▒     ░░   ░   ░ ░      ░    ░        ░         ░      ░     ░   ▒   ░ ░░ ░    ░
      ░  ░ ░            ░  ░   ░         ░  ░   ░  ░                           ░         ░  ░░  ░      ░  ░
         ░
=======================================
endef

export ASCILOGO

# http://misc.flogisoft.com/bash/tip_colors_and_formatting

RED=\033[0;31m
GREEN=\033[0;32m
ORNG=\033[38;5;214m
BLUE=\033[38;5;81m
NC=\033[0m

export RED
export GREEN
export NC
export ORNG
export BLUE

# verify that certain variables have been defined off the bat
check_defined = \
    $(foreach 1,$1,$(__check_defined))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $(value 2), ($(strip $2)))))

list_allowed_args := name interface

help:
	@printf "\033[1m$$ASCILOGO $$NC\n"
	@printf "\033[21m\n\n"
	@printf "=======================================\n"
	@printf "\n"
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

list:
	@$(MAKE) -qp | awk -F':' '/^[a-zA-Z0-9][^$#\/\t=]*:([^=]|$$)/ {split($$1,A,/ /);for(i in A)print A[i]}' | sort

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

.PHONY: bootstrap
bootstrap:
	# [ "$$VIRTUAL_ENV" != "" ]
	rm -rf *.egg-info || true
	pip install -r requirements.txt
	pip install -r requirements_dev.txt
	python setup.py install
	pip install -e .[test]

.PHONY: bootstrap-experimental
bootstrap-experimental:
	pip install -r requirements_test_experimental.txt

clean-coverge-files:
	rm -rf htmlcov/
	rm -rf cov_annotate/
	rm -rf cov.xml

# NUKE THE WORLD
clean-build-test-artifacts:
	rm -rf build/
	rm -rf dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -frv {} +
	find . -name '*.egg' -exec rm -fv {} +
	$(MAKE) clean-coverge-files
	find . -name '*.pyc' -exec rm -fv {} +
	find . -name '*.pyo' -exec rm -fv {} +
	find . -name '*~' -print -exec rm -fv {} +
	find . -name '__pycache__' -exec rm -frv {} +

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

docker-build:
	docker-compose -f docker-compose.yml -f ci/build.yml build

docker-build-run: docker-build
	docker run -i -t --rm scarlettos_scarlett_master bash

lint: ## check style with flake8
	flake8 scarlett_os tests

pytest-install-test-deps: clean
	pip install -e .[test]
	python setup.py install

pytest-run:
	py.test
	# py.test -v --timeout=30 --duration=10 --cov --cov-report=

# NOTE: Run this test suite on vagrant boxes
jhbuild-run-test:
	jhbuild run python setup.py install
	jhbuild run -- pip install -e .[test]
	jhbuild run -- coverage run -- setup.py test
	jhbuild run -- coverage report --show-missing
	jhbuild run -- coverage xml -o cov.xml


# jhbuild run -- py.test -s --tb short --cov-config .coveragerc --cov scarlett_os tests --cov-report term-missing --cov-report xml:cov.xml --cov-report html:htmlcov --cov-report annotate:cov_annotate --benchmark-skip
# NOTE: Run this test suite on vagrant boxes
.PHONY: jhbuild-run-clean-test-all
jhbuild-run-clean-test-all: export TRAVIS_CI=1
jhbuild-run-clean-test-all:
	$(MAKE) clean-build-test-artifacts
	jhbuild run python setup.py install
	jhbuild run -- pip install -e .[test]
	jhbuild run -- coverage run -- setup.py test
	jhbuild run -- $(pytest) $(test_args_with_xml)
	# jhbuild run -- coverage report --show-missing

# NOTE: Nuke all artifacts before even testing
.PHONY: test-travis-clean-ruamelconfigonly
test-travis-clean-ruamelconfigonly: export TRAVIS_CI=1
test-travis-clean-ruamelconfigonly:
	$(MAKE) clean-build-test-artifacts
	jhbuild run python setup.py install
	jhbuild run -- pip install -e .[test]
	jhbuild run -- coverage run -- setup.py test
	jhbuild run -- $(pytest) $(test_args_with_xml) -m ruamelconfigonly
	jhbuild run -- coverage report --show-missing
	jhbuild run -- coverage xml -o cov.xml

# NOTE: Run this test suite on vagrant boxes
vagrant-travis-test: jhbuild-run-test

test: ## run tests quickly with the default Python
	python setup.py test

test-clean-all: ## run tests on every Python version with tox
	pip install -e .[test]
	python setup.py install
	coverage run setup.py test

test-with-pdb:
	# pytest -p no:timeout -k test_mpris_player_and_tasker
	pytest -p no:timeout -k test_mpris_player_and_tasker

test-docker:
	sudo chown -R vagrant:vagrant *
	grep -q -F 'privileged: true' docker-compose.yml || sed -i "/build: ./a \ \ privileged: true" docker-compose.yml
	docker-compose -f docker-compose.yml -f ci/build.yml build
	docker run --cap-add=ALL --privileged -v `pwd`:/home/pi/dev/bossjones-github/scarlett_os -i -t --rm scarlettos_scarlett_master make test-travis
	sudo chown -R vagrant:vagrant *

.PHONY: test-perf
test-perf:
	$(pytest) $(test_args) --benchmark-only

.PHONY: jenkins
jenkins: bootstrap
	$(pytest) $(test_args) --benchmark-skip

.PHONY: test-travis
test-travis: export TRAVIS_CI=1
test-travis:
	$(pytest) $(test_args_no_xml) --benchmark-skip
	coverage report --show-missing

.PHONY: test-travis-scarlettonly
test-travis-scarlettonly: export TRAVIS_CI=1
test-travis-scarlettonly:
	$(pytest) $(test_args_no_xml) --benchmark-skip -m scarlettonly
	coverage report --show-missing

.PHONY: test-travis-scarlettonlyintgr
test-travis-scarlettonlyintgr: export TRAVIS_CI=1
test-travis-scarlettonlyintgr:
	$(pytest) $(test_args_no_xml) --benchmark-skip -m scarlettonlyintgr
	coverage report --show-missing

.PHONY: test-travis-scarlettonlyintgr-no-timeout
test-travis-scarlettonlyintgr-no-timeout: export TRAVIS_CI=1
test-travis-scarlettonlyintgr-no-timeout:
	$(pytest) $(test_args_no_xml) --benchmark-skip -m scarlettonlyintgr -p no:timeout
	coverage report --show-missing

.PHONY: test-travis-scarlettonlyunittest
test-travis-scarlettonlyunittest: export TRAVIS_CI=1
test-travis-scarlettonlyunittest:
	$(pytest) $(test_args_no_xml) --benchmark-skip -m scarlettonlyunittest
	coverage report --show-missing

.PHONY: test-travis-unittest
test-travis-unittest: export TRAVIS_CI=1
test-travis-unittest:
	$(pytest) $(test_args_no_xml) --benchmark-skip -m unittest
	coverage report --show-missing

.PHONY: test-travis-debug
test-travis-debug:
	$(pytest) $(test_args_no_xml) --benchmark-skip --pdb --showlocals
	coverage report --show-missing

.PHONY: test-travis-leaks
test-travis-leaks: export TRAVIS_CI=1
test-travis-leaks:
	$(pytest) $(test_args_no_xml) --benchmark-skip -R :
	coverage report --show-missing

.PHONY: cover
cover:
	$(pytest) $(cover_args) --benchmark-skip
	coverage report --show-missing
	coverage html
	$(BROWSER) htmlcov/index.html

.PHONY: cover-travisci
cover-travisci: export TRAVIS_CI=1
cover-travisci: display-env
	# $(pytest) $(cover_args) --benchmark-skip -p no:ipdb
	pytest -p no:ipdb -p no:pytestipdb -s --tb short --cov-config .coveragerc --cov scarlett_os tests --cov-report html --benchmark-skip --showlocals --trace-config
	coverage report --show-missing
	coverage html
	$(BROWSER) htmlcov/index.html

.PHONY: cover-debug
cover-debug:
	# --showlocals # show local variables in tracebacks
	$(pytest) $(cover_args) --benchmark-skip --pdb --showlocals
	coverage report --show-missing
	coverage html
	$(BROWSER) htmlcov/index.html

.PHONY: cover-debug-no-timeout
cover-debug-no-timeout:
	pytest -p no:timeout -s --tb short --cov-config .coveragerc --cov scarlett_os tests --cov-report html --benchmark-skip --pdb --showlocals
	coverage report --show-missing
	coverage html
	$(BROWSER) htmlcov/index.html

.PHONY: display-env
display-env:
	@printf "=======================================\n"
	@printf "$$GREEN TRAVIS_CI:$$NC             $(TRAVIS_CI) \n"
	@printf "=======================================\n"

# This task simulates a travis environment
.PHONY: cover-debug-no-timeout-travisci
cover-debug-no-timeout-travisci: export TRAVIS_CI=1
cover-debug-no-timeout-travisci: display-env
	pytest -p no:timeout -s --tb short --cov-config .coveragerc --cov scarlett_os tests --cov-report html --benchmark-skip --pdb --showlocals
	coverage report --show-missing
	coverage html
	$(BROWSER) htmlcov/index.html

.PHONY: shell
shell:
	ipython

coverage: ## check code coverage quickly with the default Python
		# coverage run --source scarlett_os setup.py test
		coverage run --source=scarlett_os/ setup.py test
		# defined inside of setup.cfg:
		# --cov=scarlett_os --cov-report term-missing tests/
		# coverage run --source=scarlett_os/ --include=scarlett_os setup.py test
		coverage report --show-missing
		coverage html
		$(BROWSER) htmlcov/index.html

coverage-no-html: ## check code coverage quickly with the default Python

	coverage run --source scarlett_os setup.py test

	coverage report --show-missing

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/scarlett_os.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ scarlett_os
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: clean ## package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

dc-ci-build:
	docker-compose -f docker-compose.yml -f ci/build.yml build

docker-run-bash:
	docker run -i -t --rm scarlettos_scarlett_master bash

.PHONY: scp-local-coverage
scp-local-coverage:
	rm .coverage; \
	rm -rfv .coverage.*; \
	./scripts/contrib/scp_local.sh .coverage; \

.PHONY: scp-local-cov-xml
scp-local-cov-xml:
	rm cov.xml; \
	./scripts/contrib/scp_local.sh cov.xml; \

.PHONY: scp-local-cov_annotate
scp-local-cov_annotate: export SCARLETT_SCP_RECURSIVE=1
scp-local-cov_annotate:
	rm -rfv cov_annotate; \
	./scripts/contrib/scp_local.sh cov_annotate; \

.PHONY: scp-local-htmlcov
scp-local-htmlcov: export SCARLETT_SCP_RECURSIVE=1
scp-local-htmlcov:
	rm -rfv scp-local-htmlcov; \
	./scripts/contrib/scp_local.sh htmlcov; \

.PHONY: scp-local-gir
scp-local-gir: export SCARLETT_SCP_RECURSIVE=1
scp-local-gir:
	rm -rfv gir-1.0; \
	./scripts/contrib/scp_local.sh gir-1.0; \

# fakegir: Bring autocompletion to your PyGObject code
fakegir:
	git clone git@github.com:bossjones/fakegir.git

.PHONY: fakegir-bootstrap
fakegir-bootstrap:
	pip install -r requirements_autocomplete.txt

# Use this one on OSX followed by "make open-coverage-report-html"
.PHONY: scp-local-coverage-reports
scp-local-coverage-reports:
	$(MAKE) clean-coverge-files
	$(MAKE) scp-local-coverage
	$(MAKE) scp-local-cov-xml
	$(MAKE) scp-local-cov_annotate
	$(MAKE) scp-local-htmlcov

.PHONY: open-coverage-report-html
open-coverage-report-html:
	$(BROWSER) htmlcov/index.html

.PHONY: open-coverage-cov_annotate
open-coverage-cov_annotate:
	vim cov_annotate

# rm -f .coverage .coverage.* coverage.xml .metacov*
# --cov-append
coverage-erase:
	coverage erase
# run – Run a Python program and collect execution data.
# report – Report coverage results.
# html – Produce annotated HTML listings with coverage results.
# xml – Produce an XML report with coverage results.
# annotate – Annotate source files with coverage results.
# erase – Erase previously collected coverage data.
# combine – Combine together a number of data files.
# debug – Get diagnostic information.

# Coverage annotated source written to dir cov_annotate
# Coverage HTML written to dir htmlcov
# Coverage XML written to file cov.xml

# docker-exec-bash:
# 	container_id := $(shell docker ps |grep scarlettos_scarlett_master| awk '{print $1}')
# 	docker exec -i it $(container_id) bash

install: clean ## install the package to the active Python's site-packages
	python setup.py install

install-all:
	pip install -r requirements.txt
	python setup.py install
	pip install -e .[test]

setup-venv:
	mkvirtualenv --python=/usr/local/bin/python3 scarlett-os-venv

install-travis-lint:
	bundle install --path .vendor

run-travis-lint:
	bundle exec travis lint

install-gi-osx:
	brew reinstall pygobject3 --with-python3

isort:
	python setup.py isort

dbus-monitor-signal:
	dbus-monitor "type='signal'"

dbus-monitor-all:
	dbus-monitor

run-mpris:
	python -m scarlett_os.mpris

run-tasker:
	python -m scarlett_os.tasker

run-listener:
	python -m scarlett_os.listener

run-ruamel-config:
	python -m scarlett_os.common.configure.ruamel_config

# source: https://github.com/docker/machine/blob/master/docs/drivers/generic.md#interaction-with-ssh-agents
# source: http://blog.scottlowe.org/2015/08/04/using-vagrant-docker-machine-together/
create-docker-machine:
	docker-machine create -d generic \
						  --generic-ssh-user pi \
						  --generic-ssh-key /Users/malcolm/dev/bossjones/scarlett_os/keys/vagrant_id_rsa \
						  --generic-ssh-port 2222 \
						  --generic-ip-address 127.0.0.1 \
						  --engine-install-url "https://test.docker.com" \
						  scarlett-1604-packer
	eval $(docker-machine env scarlett-1604-packer)

docker-compose-build:
	@docker-compose -f docker-compose-devtools.yml build

docker-compose-build-master:
	@docker-compose -f docker-compose-devtools.yml build master

docker-compose-run-master:
	@docker-compose -f docker-compose-devtools.yml run --name scarlett_master --rm master bash

docker-compose-run-test:
	@docker-compose -f docker-compose-devtools.yml run --name scarlett_test --rm test bash python3 --version

docker-compose-up:
	@docker-compose -f docker-compose-devtools.yml up -d

docker-compose-up-build:
	@docker-compose -f docker-compose-devtools.yml up --build

docker-compose-up-build-d:
	@docker-compose -f docker-compose-devtools.yml up -d --build

docker-compose-down:
	@docker-compose -f docker-compose-devtools.yml down

docker-version:
	@docker --version
	@docker-compose --version

docker-exec:
	@scripts/docker/exec-master

docker-exec-master:
	@scripts/docker/exec-master

format:
	$(call check_defined, name, Please set name)
	yapf -i $(product).py || (exit 1)

convert-markdown-to-rst:
	pandoc --from=markdown_github --to=rst --output=README.rst README.md

install-pandoc-stuff:
	ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip3 install sphinx sphinx-autobuild restructuredtext-lint

.PHONY: docker-clean
docker-clean:
	docker rm $(docker ps -a -q); docker rmi $(docker images | grep "^<none>" | awk '{print $3}');

# NOTE: Use this to ssh to running docker container
.PHONY: ssh
ssh:
	@ssh \
	-o Compression=yes \
	-o DSAAuthentication=yes \
	-o LogLevel=FATAL \
	-o IdentitiesOnly=yes \
	-o StrictHostKeyChecking=no \
	-o UserKnownHostsFile=/dev/null \
	-i $$(pwd)/keys/vagrant_id_rsa \
	-p 2222 \
	pi@localhost

# Start here
.PHONY: docker_asset_build
docker_asset_build:
	set -x ;\
	docker build \
	    --build-arg CONTAINER_VERSION=$(CONTAINER_VERSION) \
	    --build-arg GIT_BRANCH=$(GIT_BRANCH) \
	    --build-arg GIT_SHA=$(GIT_SHA) \
	    --build-arg BUILD_DATE=$(BUILD_DATE) \
	    --build-arg SCARLETT_ENABLE_SSHD=0 \
	    --build-arg SCARLETT_ENABLE_DBUS='true' \
	    --build-arg SCARLETT_BUILD_GNOME='false' \
	    --build-arg TRAVIS_CI='true' \
	    --build-arg STOP_AFTER_GOSS_JHBUILD='false' \
	    --build-arg STOP_AFTER_GOSS_GTK_DEPS='false' \
		--build-arg SKIP_TRAVIS_CI_PYTEST='false' \
		--build-arg STOP_AFTER_TRAVIS_CI_PYTEST='false' \
		--file=Dockerfile.build \
		--tag $(username)/$(container_name):$(GIT_SHA) . ; \
	docker tag $(username)/$(container_name):$(GIT_SHA) $(username)/$(container_name):asset

.PHONY: docker_asset_run
docker_asset_run:
	set -x ;\
	docker run -i -t --rm \
		--name scarlett-asset \
	    -e CONTAINER_VERSION=$(CONTAINER_VERSION) \
	    -e GIT_BRANCH=$(GIT_BRANCH) \
	    -e GIT_SHA=$(GIT_SHA) \
	    -e BUILD_DATE=$(BUILD_DATE) \
	    -e SCARLETT_ENABLE_SSHD=0 \
	    -e SCARLETT_ENABLE_DBUS='true' \
	    -e SCARLETT_BUILD_GNOME='false' \
	    -e TRAVIS_CI='true' \
	    -e STOP_AFTER_GOSS_JHBUILD='false' \
	    -e STOP_AFTER_GOSS_GTK_DEPS='false' \
	    -e SKIP_GOSS_TESTS_JHBUILD='false' \
	    -e SKIP_GOSS_TESTS_GTK_DEPS='false' \
		-e SKIP_TRAVIS_CI_PYTEST='true' \
		-e STOP_AFTER_TRAVIS_CI_PYTEST='false' \
		-e TRAVIS_CI_PYTEST='false' \
		-v $$(pwd)/:/home/pi/dev/bossjones-github/scarlett_os:rw \
	    $(username)/$(container_name):asset /bin/bash

# Start here
.PHONY: docker_build_dev
docker_build_dev:
	set -x ;\
	mkdir -p wheelhouse; \
	docker build \
	    --build-arg CONTAINER_VERSION=$(CONTAINER_VERSION) \
	    --build-arg GIT_BRANCH=$(GIT_BRANCH) \
	    --build-arg GIT_SHA=$(GIT_SHA) \
	    --build-arg BUILD_DATE=$(BUILD_DATE) \
	    --build-arg SCARLETT_ENABLE_SSHD=0 \
	    --build-arg SCARLETT_ENABLE_DBUS='true' \
	    --build-arg SCARLETT_BUILD_GNOME='false' \
	    --build-arg TRAVIS_CI='true' \
	    --build-arg STOP_AFTER_GOSS_JHBUILD='false' \
	    --build-arg STOP_AFTER_GOSS_GTK_DEPS='false' \
		--build-arg SKIP_TRAVIS_CI_PYTEST='false' \
		--build-arg STOP_AFTER_TRAVIS_CI_PYTEST='false' \
		--file=Dockerfile \
		--tag $(username)/$(container_name):$(GIT_SHA) . ; \
	docker tag $(username)/$(container_name):$(GIT_SHA) $(username)/$(container_name):dev

.PHONY: docker_run_dev
docker_run_dev:
	set -x ;\
	docker run -i -t --rm \
		--name scarlett-dev \
	    -e CONTAINER_VERSION=$(CONTAINER_VERSION) \
	    -e GIT_BRANCH=$(GIT_BRANCH) \
	    -e GIT_SHA=$(GIT_SHA) \
	    -e BUILD_DATE=$(BUILD_DATE) \
	    -e SCARLETT_ENABLE_SSHD=0 \
	    -e SCARLETT_ENABLE_DBUS='true' \
	    -e SCARLETT_BUILD_GNOME='false' \
	    -e TRAVIS_CI='true' \
	    -e STOP_AFTER_GOSS_JHBUILD='false' \
	    -e STOP_AFTER_GOSS_GTK_DEPS='false' \
	    -e SKIP_GOSS_TESTS_JHBUILD='true' \
	    -e SKIP_GOSS_TESTS_GTK_DEPS='true' \
		-e SKIP_TRAVIS_CI_PYTEST='false' \
		-e STOP_AFTER_TRAVIS_CI_PYTEST='false' \
		-v $$(pwd)/:/home/pi/dev/bossjones-github/scarlett_os:rw \
	    $(username)/$(container_name):dev /bin/bash


.PHONY: docker_run_ssh
docker_run_ssh:
	set -x ;\
	docker run -i -t --rm \
        -p 2222:22 \
		--name scarlett-ssh \
	    -e CONTAINER_VERSION=$(CONTAINER_VERSION) \
	    -e GIT_BRANCH=$(GIT_BRANCH) \
	    -e GIT_SHA=$(GIT_SHA) \
	    -e BUILD_DATE=$(BUILD_DATE) \
	    -e SCARLETT_ENABLE_SSHD='true' \
	    -e SCARLETT_ENABLE_DBUS='true' \
	    -e SCARLETT_BUILD_GNOME='false' \
	    -e TRAVIS_CI='true' \
	    -e STOP_AFTER_GOSS_JHBUILD='false' \
	    -e STOP_AFTER_GOSS_GTK_DEPS='false' \
	    -e SKIP_GOSS_TESTS_JHBUILD='true' \
	    -e SKIP_GOSS_TESTS_GTK_DEPS='true' \
		-e SKIP_TRAVIS_CI_PYTEST='true' \
		-e STOP_AFTER_TRAVIS_CI_PYTEST='false' \
		-v $$(pwd)/:/home/pi/dev/bossjones-github/scarlett_os:rw \
	    $(username)/$(container_name):dev /home/pi/dev/bossjones-github/scarlett_os/container/root/remote_debugging

# Start here
.PHONY: docker_build_test
docker_build_test:
	set -x ;\
	docker build \
	    --build-arg CONTAINER_VERSION=$(CONTAINER_VERSION) \
	    --build-arg GIT_BRANCH=$(GIT_BRANCH) \
	    --build-arg GIT_SHA=$(GIT_SHA) \
	    --build-arg BUILD_DATE=$(BUILD_DATE) \
	    --build-arg SCARLETT_ENABLE_SSHD=0 \
	    --build-arg SCARLETT_ENABLE_DBUS='true' \
	    --build-arg SCARLETT_BUILD_GNOME='false' \
	    --build-arg TRAVIS_CI='true' \
	    --build-arg STOP_AFTER_GOSS_JHBUILD='false' \
	    --build-arg STOP_AFTER_GOSS_GTK_DEPS='false' \
		--build-arg SKIP_TRAVIS_CI_PYTEST='false' \
		--build-arg STOP_AFTER_TRAVIS_CI_PYTEST='true' \
		--file=Dockerfile \
		--tag $(username)/$(container_name):$(GIT_SHA) . ; \
	docker tag $(username)/$(container_name):$(GIT_SHA) $(username)/$(container_name):test

.PHONY: docker_run_test
docker_run_test:
	set -x ;\
	docker run -i -t --rm \
		--privileged \
		--cap-add=ALL \
		--name scarlett-test \
	    -e CONTAINER_VERSION=$(CONTAINER_VERSION) \
	    -e GIT_BRANCH=$(GIT_BRANCH) \
	    -e GIT_SHA=$(GIT_SHA) \
	    -e BUILD_DATE=$(BUILD_DATE) \
	    -e SCARLETT_ENABLE_SSHD=0 \
	    -e SCARLETT_ENABLE_DBUS='true' \
	    -e SCARLETT_BUILD_GNOME='false' \
	    -e TRAVIS_CI='true' \
	    -e STOP_AFTER_GOSS_JHBUILD='false' \
	    -e STOP_AFTER_GOSS_GTK_DEPS='false' \
	    -e SKIP_GOSS_TESTS_JHBUILD='true' \
	    -e SKIP_GOSS_TESTS_GTK_DEPS='true' \
		-e SKIP_TRAVIS_CI_PYTEST='false' \
		-e STOP_AFTER_TRAVIS_CI_PYTEST='true' \
		-e FIXUID=$(FIXUID) \
		-e FIXGID=$(FIXGID) \
		-v $$(pwd)/:/home/pi/dev/bossjones-github/scarlett_os:rw \
	    $(username)/$(container_name):test /init

.PHONY: docker_build_wheelhouse
docker_build_wheelhouse:
	set -x ;\
	mkdir -p wheelhouse; \
	docker build \
	    --build-arg CONTAINER_VERSION=$(CONTAINER_VERSION) \
	    --build-arg GIT_BRANCH=$(GIT_BRANCH) \
	    --build-arg GIT_SHA=$(GIT_SHA) \
	    --build-arg BUILD_DATE=$(BUILD_DATE) \
	    --build-arg SCARLETT_ENABLE_SSHD=0 \
	    --build-arg SCARLETT_ENABLE_DBUS='true' \
	    --build-arg SCARLETT_BUILD_GNOME='false' \
	    --build-arg TRAVIS_CI='true' \
	    --build-arg STOP_AFTER_GOSS_JHBUILD='false' \
	    --build-arg STOP_AFTER_GOSS_GTK_DEPS='false' \
		--build-arg SKIP_TRAVIS_CI_PYTEST='false' \
		--build-arg STOP_AFTER_TRAVIS_CI_PYTEST='false' \
		--file=Dockerfile.build \
		--tag $(username)/$(container_name)-build:$(GIT_SHA) . ; \
	docker tag $(username)/$(container_name)-build:$(GIT_SHA) $(username)/$(container_name)-build:dev

.PHONY: docker_run_wheelhouse
docker_run_wheelhouse:
	set -x ;\
	mkdir -p wheelhouse; \
	docker run -i -t --rm \
		--name scarlett-dev-wheelhouse \
	    -e CONTAINER_VERSION=$(CONTAINER_VERSION) \
	    -e GIT_BRANCH=$(GIT_BRANCH) \
	    -e GIT_SHA=$(GIT_SHA) \
	    -e BUILD_DATE=$(BUILD_DATE) \
	    -e SCARLETT_ENABLE_SSHD=0 \
	    -e SCARLETT_ENABLE_DBUS='true' \
	    -e SCARLETT_BUILD_GNOME='false' \
	    -e TRAVIS_CI='true' \
	    -e STOP_AFTER_GOSS_JHBUILD='false' \
	    -e STOP_AFTER_GOSS_GTK_DEPS='false' \
	    -e SKIP_GOSS_TESTS_JHBUILD='false' \
	    -e SKIP_GOSS_TESTS_GTK_DEPS='false' \
		-e SKIP_TRAVIS_CI_PYTEST='true' \
		-e STOP_AFTER_TRAVIS_CI_PYTEST='false' \
		-e TRAVIS_CI_PYTEST='false' \
		-v $$(pwd)/:/home/pi/dev/bossjones-github/scarlett_os:rw \
		-v $$(pwd)/wheelhouse/:/wheelhouse:rw \
	    $(username)/$(container_name)-build:dev /bin/bash

# ENV TRAVIS_CI_RUN_PYTEST ${TRAVIS_CI_RUN_PYTEST:-'false'}
# ENV TRAVIS_CI_SKIP_PYTEST ${TRAVIS_CI_SKIP_PYTEST:-'false'}

.PHONY: update_requirements
update_requirements:
	pur -r requirements.txt
	pur -r requirements_dev.txt
	pur -r requirements_test_all.txt
	pur -r requirements_test.txt
	pur -r requirements_test_experimental.txt

# Fix all py files with autopep8
.PHONY: apply-autopep8
apply-autopep8:
	find . -name "*.py" -exec autopep8 --max-line-length 200 --in-place --aggressive --aggressive {} \;

.PHONY: apply-isort
apply-isort:
	isort --recursive --diff --verbose scarlett_os/

.PHONY: setup-pre-commit
setup-pre-commit:
	pip install pre-commit
	pre-commit install -f --install-hooks

.PHONY: pre-commit-run
pre-commit-run:
	pre-commit run

.PHONY: pre-commit-try
pre-commit-try:
	pre-commit try-repo .

.PHONY: makelint-install
makelint-install:
	go get github.com/mrtazz/checkmake
	cd $$GOPATH/src/github.com/mrtazz/checkmake
	make

# github_changelog_generator comes from
# https://github.com/skywinder/github-changelog-generator
# Follow the instructions to generate a github api token
# VERSION = $(firstword $(subst -, ,$(RELEASE) ))
# LAST_COMMIT_MSG = $(shell git log -1 --pretty=%B | sed -e 's/\x27/"/g')
# github_changelog_generator comes from
# https://github.com/skywinder/github-changelog-generator
# Follow the instructions to generate a github api token
# release:
# 	dch -v $(RELEASE) --distribution xenial --changelog ../debian/changelog $$'$(VERSION) tagged with \'make release\'\rCommit: $(LAST_COMMIT_MSG)'
# 	sed -i -e "s/__version__ = .*/__version__ = '$(VERSION)'/" ../paasta_tools/__init__.py
# 	@echo "$(RELEASE) has the changelog set."
# 	github_changelog_generator -u Yelp -p paasta --since-tag v0.68.0 --max-issues=200 --future-release $(RELEASE) --output ../CHANGELOG.md || echo github_changelog_generator not installed, not generating changelog!! || true
# 	cd .. && make docs || true
# 	@git diff
# 	@echo "Now Run:"
# 	@echo 'git commit -a -m "Released $(RELEASE) via make release"'
# 	@echo 'git tag --force v$(VERSION)'
# 	@echo 'git push --tags origin master'


# NOTE: You can also run pylint with warnings turned into errors using python -W error -m pylint … to get a traceback for the warnings.
# SOURCE: https://github.com/neomake/neomake/issues/1828#issuecomment-377901357
.PHONY: run-pylint-error
run-pylint-error:
	pylint -E scarlett_os

.PHONY: jhbuild-run-pylint-error
jhbuild-run-pylint-error:
	jhbuild run -- pylint -E scarlett_os

.PHONY: jhbuild-run-pylint-warning-stacktrace
jhbuild-run-pylint-warning-stacktrace:
	jhbuild run -- python -W error -m pylint -E scarlett_os

.PHONY: jhbuild-run-pip-compile-upgrade-all
jhbuild-run-pip-compile-upgrade-all:
	jhbuild run -- pip-compile --output-file requirements.txt requirements.in --upgrade ;\
	jhbuild run -- pip-compile --output-file requirements_dev.txt requirements_dev.in --upgrade ;\
	jhbuild run -- pip-compile --output-file requirements_test_all.txt requirements_test_all.in --upgrade ;\
	jhbuild run -- pip-compile --output-file requirements_test_experimental.txt requirements_test_experimental.in --upgrade ;\
	jhbuild run -- pip-compile --output-file requirements_autocomplete.txt requirements_autocomplete.in --upgrade ;\
	jhbuild run -- pip-compile --output-file requirements_packaging.txt requirements_packaging.in --upgrade

.PHONY: jhbuild-run-pip-compile
jhbuild-run-pip-compile:
	jhbuild run -- pip-compile --output-file requirements.txt requirements.in ;\
	jhbuild run -- pip-compile --output-file requirements_dev.txt requirements_dev.in ;\
	jhbuild run -- pip-compile --output-file requirements_test_all.txt requirements_test_all.in ;\
	jhbuild run -- pip-compile --output-file requirements_test_experimental.txt requirements_test_experimental.in ;\
	jhbuild run -- pip-compile --output-file requirements_autocomplete.txt requirements_autocomplete.in ;\
	jhbuild run -- pip-compile --output-file requirements_packaging.txt requirements_packaging.in

# sshfs testing

.PHONY: sshfs-mount-fake-venv
sshfs-mount-fake-venv:
	sshfs -p 2222 \
	pi@127.0.0.1:/home/pi/fake-venv \
	~/fake-venv \
	-o reconnect -o delay_connect \
	-o sshfs_debug \
	-o allow_other \
	-o defer_permissions \
	-o IdentityFile=~/dev/bossjones/scarlett-ansible/keys/vagrant_id_rsa \
	-o UserKnownHostsFile=/dev/null \
	-o StrictHostKeyChecking=no \
	-o PasswordAuthentication=no\
	-o IdentitiesOnly=yes \
	-o LogLevel=VERBOSE \
	-o volname=fake-venv

.PHONY: sshfs-unmount-fake-venv
sshfs-unmount-fake-venv:
	umount ~/fake-venv

# Mount virtualenv
.PHONY: sshfs-mount-scarlett_os-sshfs-virtualenv
sshfs-mount-scarlett_os-sshfs-virtualenv:
	mkdir -p ~/.virtualenvs/scarlett_os-sshfs ; \
	sshfs -p 2222 \
	pi@127.0.0.1:/home/pi/.virtualenvs/scarlett_os-sshfs \
	~/.virtualenvs/scarlett_os-sshfs \
	-o reconnect \
	-o delay_connect \
	-o sshfs_debug \
	-o allow_other \
	-o defer_permissions \
	-o IdentityFile=~/dev/bossjones/scarlett-ansible/keys/vagrant_id_rsa \
	-o UserKnownHostsFile=/dev/null \
	-o StrictHostKeyChecking=no \
	-o PasswordAuthentication=no \
	-o IdentitiesOnly=yes \
	-o LogLevel=VERBOSE \
	-o volname=scarlett_os-sshfs-virtualenv \
	-o ServerAliveInterval=30 ; \

.PHONY: sshfs-unmount-scarlett_os-sshfs-virtualenv
sshfs-unmount-scarlett_os-sshfs-virtualenv:
	umount ~/.virtualenvs/scarlett_os-sshfs

# mount source code
.PHONY: sshfs-mount-scarlett_os-sshfs-code
sshfs-mount-scarlett_os-sshfs-code:
	mkdir -p ~/scarlett_os-sshfs ; \
	sshfs -p 2222 \
	pi@127.0.0.1:/home/pi/dev/bossjones-github/scarlett_os-sshfs \
	~/scarlett_os-sshfs \
	-o reconnect \
	-o delay_connect \
	-o sshfs_debug \
	-o allow_other \
	-o defer_permissions \
	-o IdentityFile=~/dev/bossjones/scarlett-ansible/keys/vagrant_id_rsa \
	-o UserKnownHostsFile=/dev/null \
	-o StrictHostKeyChecking=no \
	-o PasswordAuthentication=no \
	-o IdentitiesOnly=yes \
	-o LogLevel=VERBOSE \
	-o volname=scarlett_os-sshfs-code \
	-o ServerAliveInterval=30 ; \

.PHONY: sshfs-unmount-scarlett_os-sshfs-code
sshfs-unmount-scarlett_os-sshfs-code:
	umount ~/scarlett_os-sshfs

.PHONY: sshfs-unmount-all
sshfs-unmount-all:
	$(MAKE) sshfs-unmount-scarlett_os-sshfs-code
	$(MAKE) sshfs-unmount-scarlett_os-sshfs-virtualenv

.PHONY: flatpak-shell
flatpak-shell:
	flatpak-builder --run app org.scarlett.Listener.json sh

.PHONY: flatpak-build
flatpak-build:
	flatpak-builder app-dir org.scarlett.Listener.json

.PHONY: flatpak-builder
flatpak-build-force:
	flatpak-builder --force-clean app-dir --force-clean org.scarlett.Listener.json

.PHONY: run-gnome-builder
run-gnome-builder: TRACE=1
run-gnome-builder:
	$(call check_defined, interface, Please set interface)
	./run-gnome-builder-docker.sh $(interface)

pull-gnome-builder:
	docker pull $(gnome_username)/$(gnome_container_name):latest

# TODO: Use this to autogenerate the flatpak-pip-update json files!!!!
# SOURCE: https://github.com/freedomofpress/ansible-role-jenkins-config/blob/master/requirements.txt
# This file is autogenerated by pip-compile
# To update, run:
#
#    pip-compile --output-file requirements.txt requirements.in
#
pip-compile:
	pip-compile --output-file requirements_all.txt requirements.txt



# sensible pylint ( Lots of press over this during pycon 2018 )
.PHONY: run-black-check
run-black-check:
	black --check --verbose .

.PHONY: run-black
run-black:
	black --verbose .


.PHONY: reinstall-deps
reinstall-deps:
	pip install --force-reinstall -r requirements.txt

.PHONY: install-deps-all
reinstall-deps-all:
	pip install --force-reinstall -r requirements.txt; \
	pip install --force-reinstall -r requirements-dev.txt; \

.PHONY: install-deps-osx
install-deps-osx:
	env ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip install -r requirements.txt

.PHONY: install-deps-all-osx
install-deps-all-osx:
	env ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip install -r requirements.txt; \
	env ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip install -r requirements_dev.txt; \



# NOTE: This assumes that all of your repos live in the same workspace!
# link_roles:
# 	# add aliases for dotfiles
# 	@for file in $(shell find $(CURDIR)/.. -name "*ansible-role*" -type d -print); do \
# 		echo $$file; \
# 		f=$$(basename $$file); \
# 		ln -sfn $$file $(CURDIR)/roles/$f; \
# 	done; \
# 	ls -lta $(CURDIR)/roles/; \

meson-build:
	meson mesonbuild/

ninja-install:
	ninja-build -C mesonbuild/

meson-install: meson-build ninja-install

meson-build-uninstalled:
	meson mesonbuild/ --prefix=./uninstalled --libdir=lib

ninja-install-uninstalled:
	ninja-build -C mesonbuild/

meson-install-uninstalled: meson-build-uninstalled ninja-install-uninstalled
