# -*- coding: utf-8 -*-
"""
Main click group for CLI
"""

import logging
import os
import sys

import click
from click_plugins import with_plugins
from pkg_resources import iter_entry_points

import scarlett_os
from scarlett_os.compat import configparser


def configure_logging(verbosity):
    log_level = max(10, 30 - 10 * verbosity)
    logging.basicConfig(stream=sys.stderr, level=log_level)


def read_config(cfg):
    parser = configparser.ConfigParser()
    parser.read(cfg)
    rv = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            rv['{0}.{1}'.format(section, key)] = value
    return rv


@with_plugins(
    ep for ep in list(iter_entry_points('scarlett_os.scarlett_os_commands')))
@click.group()
@click.version_option(
    version=scarlett_os.__version__,
    message='%(version)s'
)
@click.option(
    "--name",
    "-n",
    help="Name ScarlettOS process explicitly.",
    metavar="NAME",
    default="scarlett_system"
)
@click.option(
    "--daemon",
    "-d",
    is_flag=True,
    help="Daemon mode, background process.",
    default=False
)
@click.option(
    '--mode',
    '-m'
    type=click.Choice(
        ['dbus_server', 'listener', 'tasker', 'check_all_services']
    ),
    help="ScarlettOS type",
    default='check_all_services'
)
@click.option(
    "--master",
    "-m",
    is_flag=True,
    help="Run ScarlettOS process as a Master",
    default=False
)
@click.option(
    "--slave",
    "-s",
    is_flag=True,
    help="Run ScarlettOS process as a Slave",
    default=False
)
@click.option(
    '--etcd-host',
    help="Etcd Host for distributed mode.",
    default=False
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Limit output to errors and warnings.",
    default=False
)
@click.option(
    "--verbose",
    "-V",
    is_flag=True,
    help="Be verbose.",
    default=False
)
@click.option(
    '--config',
    '-c',
    type=click.Path(exists=True, resolve_path=True),
    help="Config file"
)
@click.pass_context
def main_group(ctx, name, daemon, mode, master, slave, etcd_host, quiet, verbose, config):
    """This is the command line interface to ScarlettOS.
    """
    # NOTE: ctx
    # Most public functions are actually methods of a 'context' object which
    # is passed as the first parameter (ctx). The context object stores the
    # precision, cached data, and a few other things. It also defines
    # conversions so that the same high-level code can be used for several
    # different base types (mpf, mpfs in Sage, intervals, Python floats) by
    # switching contexts.
    #
    # The default context is called 'mp'. You can call most functions as
    # mpmath.mp.foo(). The top-level function mpmath.foo() is just an alias
    # for this.

    ctx.obj = {}
    config = config or os.path.join(click.get_app_dir('scarlett_os'), 'scarlett_os.ini')
    cfg = read_config(config)
    if cfg:
        ctx.obj['config_file'] = config
    ctx.obj['cfg'] = cfg
    ctx.default_map = cfg

    verbosity = (os.environ.get('SCARLETTOS_VERBOSE') or
                 ctx.lookup_default('scarlett_os.verbosity') or 0)
    if verbose or quiet:
        verbosity = verbose - quiet
    verbosity = int(verbosity)
    configure_logging(verbosity)

    ctx.obj['verbosity'] = verbosity
