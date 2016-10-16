#!/usr/bin/env python
# -*- coding: utf-8 -*-

# NOTE: fab --show=debug if you need to debug stuff

import sys
import os
import pprint
import re
# import string
# import collections
import time
from fabric.api import abort, cd, env, get, hide, hosts, local, prompt, \
    put, require, roles, run, runs_once, settings, show, sudo, warn
from fabric.contrib.project import rsync_project
from textwrap import dedent
# from fabric.operations import run, put
# from fabric.contrib.files import exists
# from fabric.operations import reboot
# from fabric.colors import red, green, yellow, blue
# from fabric.utils import puts
# from fabric.tasks import execute
# from fabric.contrib.files import exists, sed

# env.remote_interrupt = True
# env.use_ssh_config = True
# #env.gateway          = FABRIC_JUMPSERVER
# #env.disable_known_hosts = True
# #env.reject_unknown_hosts = False
# env.forward_agent = False
# env.keepalive = 60
# env.key_filename = FABRIC_KEY_FILENAME
# env.parallel = True
# env.sudo_user = FABRIC_USER
# env.user = FABRIC_USER
# env.abort_on_prompts = True

pp = pprint.PrettyPrinter(indent=4, width=80)
VM_PATTERN = 'travis-ci/ubuntu1404'


def vagrant():
    """USAGE:
    fab vagrant uname

    Note that the command to run Fabric might be different on different
    platforms.
    """

    global VM_PATTERN
    # change from the default user to 'vagrant'
    vagrant_ssh_config = local("cd $HOME/dev/{0} && vagrant ssh-config".format(VM_PATTERN), capture=True)

    hostname = re.findall(r'HostName\s+([^\n]+)', vagrant_ssh_config)[0]
    port = re.findall(r'Port\s+([^\n]+)', vagrant_ssh_config)[0]
    env.hosts = ['%s:%s' % (hostname, port)]
    env.user = re.findall(r'User\s+([^\n]+)', vagrant_ssh_config)[0]

    identity_file = re.findall(r'IdentityFile\s+([^\n]+)', vagrant_ssh_config)[0]

    env.key_filename = identity_file[1:-1]
    env.disable_known_hosts = True
    env.forward_agent = True
    env.colorize_errors = True
    env.skip_bad_hosts = True
    env.warn_only = True

    print("""
    hostname = {}
    port = {}
    env.hosts = {}
    env.user = {}
    env.key_filename = {}
    env.disable_known_hosts = {}
    env.forward_agent = {}
""".format(hostname,
           port,
           env.hosts,
           env.user,
           env.key_filename,
           env.disable_known_hosts,
           env.forward_agent))

    result = local("cd $HOME/dev/{0} && vagrant global-status | grep running | grep '{0}'".format(VM_PATTERN), capture=True)
    print("result: {}".format(result))
    machineId = result.split()[0]
    print("machineId: {}".format(machineId))


def uname():
    result = run('uname -a')


# def copy():
#
#
# def pack(loc):
#
#     rsync_project()
