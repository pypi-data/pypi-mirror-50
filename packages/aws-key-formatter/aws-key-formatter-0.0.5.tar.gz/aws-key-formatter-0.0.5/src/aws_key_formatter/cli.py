# -*- coding: utf-8 -*-

import sys

import click

from . import aws_key_formatter
from .__version__ import __version__


@click.command()
@click.version_option(version=__version__, prog_name='aws-key-formatter')
@click.option('-p', '--profile', default='default', show_default=True, help='AWS CLI Profile name')
@click.option('--token/--no-token', ' -t/', default=False, show_default=True, help='Include AWS Session Token?')
def main(profile: str, token: bool):
    """Console script for aws_key_formatter."""
    # TODO: Have the aws_key_formatter function return the string,
    # then have this function do the `click.echo` to output it.
    aws_key_formatter.main(profile, token)

    return 0


if __name__ == "__main__":
    sys.exit(main())
