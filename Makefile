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

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

list:
	@$(MAKE) -qp | awk -F':' '/^[a-zA-Z0-9][^$#\/\t=]*:([^=]|$$)/ {split($$1,A,/ /);for(i in A)print A[i]}' | sort

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts


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

lint: ## check style with flake8
	flake8 scarlett_os tests

pytest-install-test-deps: clean
	pip install -e .[test]
	python setup.py install

pytest-run:
	py.test

jhbuild-run-test:
	jhbuild run python setup.py install
	jhbuild run -- pip install -e .[test]
	jhbuild run -- coverage run -- setup.py test
	jhbuild run -- coverage report -m

test: ## run tests quickly with the default Python
	python setup.py test

test-clean-all: ## run tests on every Python version with tox
	pip install -e .[test]
	python setup.py install
	coverage run setup.py test

test-docker:
	sudo chown -R vagrant:vagrant *
	grep -q -F 'privileged: true' docker-compose.yml || sed -i "/build: ./a \ \ privileged: true" docker-compose.yml
	docker-compose -f docker-compose.yml -f ci/build.yml build
	docker run --privileged -v `pwd`:/home/pi/dev/bossjones-github/scarlett_os -i -t --rm scarlettos_scarlett_master make test
	sudo chown -R vagrant:vagrant *

coverage: ## check code coverage quickly with the default Python
		coverage run --source scarlett_os setup.py test
		coverage report -m
		coverage html
		$(BROWSER) htmlcov/index.html

coverage-no-html: ## check code coverage quickly with the default Python

	coverage run --source scarlett_os setup.py test

	coverage report -m

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
