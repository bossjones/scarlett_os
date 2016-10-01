#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

# import logging
import click

from . import __version__

# source: Doc2Dash
# class ClickEchoHandler(logging.Handler):
#     """
#     Use click.echo() for logging.  Has the advantage of stripping color codes
#     if output is redirected.  Also is generally more predictable.
#     """
#     _level_to_fg = {
#         logging.ERROR: "red",
#         logging.WARN: "yellow",
#     }
#
#     def emit(self, record):
#         click.echo(click.style(
#             record.getMessage(),
#             fg=self._level_to_fg.get(record.levelno, "reset")
#         ), err=record.levelno >= logging.WARN)


@click.command()
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
    "--slave",
    "-s",
    is_flag=True,
    help="Run ScarlettOS process as a Slave",
    default=False
)
@click.option(
    "--master",
    "-m",
    is_flag=True,
    help="Run ScarlettOS process as a Master",
    default=False
)
@click.option(
    '--type',
    type=click.Choice(['dbus_server', 'listener', 'tasker', 'check_all_services']),
    help="ScarlettOS type",
    default='check_all_services'
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
    "-v",
    is_flag=True,
    help="Be verbose.",
    default=False
)
@click.version_option(version=__version__)
def main(name, daemon, slave, quiet, verbose, master, type, etcd_host):
    """Console script for scarlett_os."""
    click.echo("Replace this message by putting your code into "
               "scarlett_os.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")


if __name__ == "__main__":
    main()
