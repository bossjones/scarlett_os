#!/usr/bin/env python
# -*- coding: utf-8 -*-

# NOTE: fab --show=debug if you need to debug stuff

import sys
import os
import pprint
import re
import string

# import collections
import time
from fabric.operations import sudo, os
from fabric.api import (
    abort,
    cd,
    env,
    get,
    hide,
    hosts,
    local,
    prompt,
    put,
    require,
    roles,
    run,
    runs_once,
    settings,
    show,
    sudo,
    warn,
    prefix,
)
from fabric.contrib.project import rsync_project, upload_project
from fabric.contrib.files import append, sed
from textwrap import dedent
import yaml
import csv

pp = pprint.PrettyPrinter(indent=4, width=80)

# from fabric.operations import run, put
# from fabric.contrib.files import exists
# from fabric.operations import reboot
# from fabric.colors import red, green, yellow, blue
# from fabric.utils import puts
# from fabric.tasks import execute
# from fabric.contrib.files import exists, sed

VM_PATTERN = "travis-ci/ubuntu1404"
USER = "vagrant"
HOME = "/home/{}".format(USER)
WORKON_HOME = "{}/.virtualenvs".format(HOME)
PROJECT_HOME = "{}/dev".format(HOME)
REPO_NAME = "scarlett_os"
REPO_ORG = "bossjones"
VENV_NAME = "{}".format(REPO_NAME)
PATH_TO_PROJECT = "{}/{}-github/{}".format(PROJECT_HOME, REPO_ORG, REPO_NAME)


def vagrant():
    """USAGE:
    fab vagrant uname

    Note that the command to run Fabric might be different on different
    platforms.
    """

    # global VM_PATTERN
    # change from the default user to 'vagrant'
    vagrant_ssh_config = local(
        "cd $HOME/dev/{0} && vagrant ssh-config".format(VM_PATTERN), capture=True
    )

    hostname = re.findall(r"HostName\s+([^\n]+)", vagrant_ssh_config)[0]
    port = re.findall(r"Port\s+([^\n]+)", vagrant_ssh_config)[0]
    env.hosts = ["%s:%s" % (hostname, port)]
    env.user = re.findall(r"User\s+([^\n]+)", vagrant_ssh_config)[0]

    identity_file = re.findall(r"IdentityFile\s+([^\n]+)", vagrant_ssh_config)[0]

    env.key_filename = identity_file[1:-1]
    env.disable_known_hosts = True
    env.forward_agent = True
    env.colorize_errors = True
    env.skip_bad_hosts = True
    env.warn_only = True

    print(
        """
    hostname = {}
    port = {}
    env.hosts = {}
    env.user = {}
    env.key_filename = {}
    env.disable_known_hosts = {}
    env.forward_agent = {}
""".format(
            hostname,
            port,
            env.hosts,
            env.user,
            env.key_filename,
            env.disable_known_hosts,
            env.forward_agent,
        )
    )

    result = local(
        "cd $HOME/dev/{0} && vagrant global-status | grep running | grep '{0}'".format(
            VM_PATTERN
        ),
        capture=True,
    )
    print("result: {}".format(result))
    machineId = result.split()[0]
    print("machineId: {}".format(machineId))


def uname():
    """Testing vagrant connections with uname -a."""
    run("uname -a")


def deploy():
    rsync_project(
        local_dir=".",
        remote_dir="/home/vagrant/dev/bossjones-github/scarlett_os/",
        exclude=[
            "*.git",
            "*.pyc",
            "*.vagrant",
            "*.vendor",
            ".Python",
            "env/",
            "build/",
            "develop-eggs/",
            "dist/",
            "downloads/",
            "eggs/",
            ".eggs/",
            "lib/",
            "lib64/",
            "parts/",
            "sdist/",
            "var/",
            "*.egg-info/",
            ".installed.cfg",
            "*.egg",
            ".tox/",
            ".bundle/",
            ".cache/",
            "__pycache__/",
        ],
        ssh_opts="-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no",
    )


def clean_build():
    """Nuke all testing directories before we get started."""
    # export WORKON_HOME=${HOME}/.virtualenvs
    # export PROJECT_HOME=${HOME}/dev
    # export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    # export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
    # source /usr/local/bin/virtualenvwrapper.sh
    # export PYTHONSTARTUP=$HOME/.pythonrc
    # export PIP_DOWNLOAD_CACHE=$HOME/.pip/cache
    ################################################################################

    with prefix("export VIRTUALENV_WRAPPER_SH=`which virtualenvwrapper.sh`"):
        with prefix("export VIRTUALENVWRAPPER_PYTHON=`which python3.5`"):
            with prefix("export VIRTUALENVWRAPPER_VIRTUALENV=`which virtualenv`"):
                with prefix("export WORKON_HOME=${HOME}/.virtualenvs"):
                    with prefix("export PROJECT_HOME=${HOME}/dev"):
                        with prefix("source $VIRTUALENV_WRAPPER_SH"):
                            with prefix("export PYTHONSTARTUP=$HOME/.pythonrc"):
                                with prefix(
                                    "export PIP_DOWNLOAD_CACHE=$HOME/.pip/cache"
                                ):
                                    with prefix("workon scarlett_os"):
                                        with cd("/home/vagrant"):
                                            sudo(
                                                "pip3.5 install virtualenv virtualenvwrapper"
                                            )
                                            run(
                                                "rm -rf /home/vagrant/dev/bossjones-github/scarlett_os"
                                            )
                                            run("rm -rf /home/vagrant/gnome")
                                            run("rm -rf /home/vagrant/jhbuild")
                                            with prefix("deactivate"):
                                                run("rmvirtualenv scarlett_os")


def bootstrap_travisci():
    with prefix("export VIRTUALENV_WRAPPER_SH=`which virtualenvwrapper.sh`"):
        with prefix("export VIRTUALENVWRAPPER_PYTHON=`which python3.5`"):
            with prefix("export VIRTUALENVWRAPPER_VIRTUALENV=`which virtualenv`"):
                with prefix("export WORKON_HOME=${HOME}/.virtualenvs"):
                    with prefix("export PROJECT_HOME=${HOME}/dev"):
                        with prefix("source $VIRTUALENV_WRAPPER_SH"):
                            with prefix("export PYTHONSTARTUP=$HOME/.pythonrc"):
                                with prefix(
                                    "export PIP_DOWNLOAD_CACHE=$HOME/.pip/cache"
                                ):
                                    with prefix(
                                        "mkvirtualenv --python=`which python3.5` scarlett_os"
                                    ):
                                        run(
                                            "mkdir -p /home/vagrant/dev/bossjones-github/scarlett_os"
                                        )
                                        with prefix("workon scarlett_os"):
                                            run("which python")


def read_yaml():
    with cd("/home/vagrant/dev/bossjones-github/scarlett_os"):
        with open(".travis.yml", "r") as f:
            travis_config = yaml.safe_load(f)
            print(yaml.dump(travis_config))
            travis_lines = [
                "#!/bin/bash",
                "set -x",
                "export DEBIAN_FRONTEND=noninteractive",
            ]

            matrix = travis_config["matrix"]["include"]
            print("****************************matrix****************************")
            for line in matrix:
                print(line)
                split_line = line["env"].split(" ")
                print(split_line)
                for l in split_line:
                    travis_lines.append("export {}".format(l))

            before_install = travis_config["before_install"]
            print(before_install)
            print(
                "****************************before_install****************************"
            )
            for line in before_install:
                line = re.sub("mkvirtualenv scarlett_os", "", line)
                # line = re.sub('travis_retry ', '', line)
                # line = re.sub('pip install', 'pip3.5 install', line)
                # line = re.sub('pip install -I path.py==7.7.1', '', line)
                # line = re.sub('which python3', 'which python3.5', line)
                #############################################################################
                # export TOXENV=typing
                # export PYTHON="python3.5"
                # export PACKAGES="python3-gi
                # export python3-gi-cairo"
                # export TOXENV=py35
                # export SKIP_ON_TRAVIS=yes
                # export CURRENT_DIR=$(pwd)
                # export GSTREAMER=1.0
                # export ENABLE_PYTHON2=yes
                # export ENABLE_PYTHON3=yes
                # export ENABLE_GTK=yes
                # export PYTHON_VERSION_MAJOR=3
                # export PYTHON_VERSION=3.5
                # export CFLAGS="-fPIC -O0 -ggdb -fno-inline -fno-omit-frame-pointer"
                # export MAKEFLAGS="-j4"
                # export PREFIX="${HOME}/jhbuild"
                # export JHBUILD="${HOME}/gnome"
                # export PATH=${PREFIX}/bin:${PREFIX}/sbin:${PATH}
                # export LD_LIBRARY_PATH=${PREFIX}/lib:${LD_LIBRARY_PATH}
                # export PYTHONPATH=${PREFIX}/lib/python${PYTHON_VERSION}/site-packages:/usr/lib/python${PYTHON_VERSION}/site-packages
                # export PKG_CONFIG_PATH=${PREFIX}/lib/pkgconfig:${PREFIX}/share/pkgconfig:/usr/lib/pkgconfig
                # export XDG_DATA_DIRS=${PREFIX}/share:/usr/share
                # export XDG_CONFIG_DIRS=${PREFIX}/etc/xdg
                # export PACKAGES="python3-gi python3-gi-cairo"
                # export CC=gcc
                #############################################################################
                travis_lines.append(line)
                print(line)

            install = travis_config["install"]
            print("****************************install****************************")
            for line in install:
                line = re.sub("travis_retry ", "", line)
                travis_lines.append(line)
                print(line)

            print(
                "****************************travis_lines****************************"
            )
            print(travis_lines)

            run("rm /home/vagrant/test_travis.sh")
            append("/home/vagrant/test_travis.sh", travis_lines)
            print(
                "****************************patch test_travis****************************"
            )
            sed("/home/vagrant/test_travis.sh", "travis_retry ", "")
            sed("/home/vagrant/test_travis.sh", "pip install", "pip3.5 install")
            sed("/home/vagrant/test_travis.sh", "pip install -I path.py==7.7.1", "")
            sed("/home/vagrant/test_travis.sh", "which python3", "which python3.5")
            sed(
                "/home/vagrant/test_travis.sh",
                "/usr/bin/python3",
                "/usr/local/bin/python3.5",
            )
            sed(
                "/home/vagrant/test_travis.sh", 'PYTHON="python3"', 'PYTHON="python3.5"'
            )
            sed("/home/vagrant/test_travis.sh", "pip3.5 install -I path.py==7.7.1", "")
            print(
                "****************************patch test_travis****************************"
            )
            sed(
                "/home/vagrant/dev/bossjones-github/scarlett_os/ci/set_postactivate.sh",
                "travis_retry ",
                "",
            )
            sed(
                "/home/vagrant/dev/bossjones-github/scarlett_os/ci/set_postactivate.sh",
                "pip install",
                "pip3.5 install",
            )
            sed(
                "/home/vagrant/dev/bossjones-github/scarlett_os/ci/set_postactivate.sh",
                "pip install -I path.py==7.7.1",
                "",
            )
            sed(
                "/home/vagrant/dev/bossjones-github/scarlett_os/ci/set_postactivate.sh",
                "which python3",
                "which python3.5",
            )
            sed(
                "/home/vagrant/dev/bossjones-github/scarlett_os/ci/set_postactivate.sh",
                "/usr/bin/python3",
                "/usr/local/bin/python3.5",
            )
            sed(
                "/home/vagrant/dev/bossjones-github/scarlett_os/ci/set_postactivate.sh",
                'PYTHON="python3"',
                'PYTHON="python3.5"',
            )
            print(
                "****************************patch test_travis****************************"
            )
            sed(
                "/home/vagrant/dev/bossjones-github/scarlett_os/ci/travis.sh",
                "travis_retry ",
                "",
            )
            sed(
                "/home/vagrant/dev/bossjones-github/scarlett_os/ci/travis.sh",
                "pip install",
                "pip3.5 install",
            )
            sed(
                "/home/vagrant/dev/bossjones-github/scarlett_os/ci/travis.sh",
                "pip install -I path.py==7.7.1",
                "",
            )
            sed(
                "/home/vagrant/dev/bossjones-github/scarlett_os/ci/travis.sh",
                "which python3",
                "which python3.5",
            )
            sed(
                "/home/vagrant/dev/bossjones-github/scarlett_os/ci/travis.sh",
                "/usr/bin/python3",
                "/usr/local/bin/python3.5",
            )
            sed(
                "/home/vagrant/dev/bossjones-github/scarlett_os/ci/travis.sh",
                'PYTHON="python3"',
                'PYTHON="python3.5"',
            )
            print(
                "****************************final-travis-script****************************"
            )
            run("cat /home/vagrant/test_travis.sh")
            run("chmod +x /home/vagrant/test_travis.sh")


def run_travis():
    with cd("/home/vagrant/dev/bossjones-github/scarlett_os"):
        run("/home/vagrant/test_travis.sh")


# fab vagrant clean_build
# fab vagrant bootstrap_travisci
# fab vagrant deploy
# fab vagrant read_yaml
# fab vagrant run_travis
# fab vagrant retest_travis


def retest_travis():
    with prefix("export VIRTUALENV_WRAPPER_SH=`which virtualenvwrapper.sh`"):
        with prefix("export VIRTUALENVWRAPPER_PYTHON=`which python3.5`"):
            with prefix("export VIRTUALENVWRAPPER_VIRTUALENV=`which virtualenv`"):
                with prefix("export WORKON_HOME=${HOME}/.virtualenvs"):
                    with prefix("export PROJECT_HOME=${HOME}/dev"):
                        with prefix("source $VIRTUALENV_WRAPPER_SH"):
                            with prefix("export PYTHONSTARTUP=$HOME/.pythonrc"):
                                with prefix(
                                    "export PIP_DOWNLOAD_CACHE=$HOME/.pip/cache"
                                ):
                                    with prefix("workon scarlett_os"):
                                        with cd(
                                            "/home/vagrant/dev/bossjones-github/scarlett_os"
                                        ):
                                            run("jhbuild run python setup.py install")
                                            run("jhbuild run -- pip install -e .[test]")
                                            run(
                                                "jhbuild run -- coverage run -- setup.py test"
                                            )
