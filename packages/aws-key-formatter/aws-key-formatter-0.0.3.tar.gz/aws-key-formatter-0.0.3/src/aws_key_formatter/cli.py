# -*- coding: utf-8 -*-

import sys

import click

from .__version__ import __version__


@click.command()
@click.version_option(version=__version__, prog_name='aws-key-formatter')
@click.option('-p', '--profile', default='default', show_default=True, help='AWS CLI Profile name')
@click.option('--token/--no-token', ' -t/', default=False, show_default=True, help='Include AWS Session Token?')
# '--profile', '-p', default='default', help='AWS CLI Profile name'
# '--include_token', '-t', action='store_true', help='Include AWS Session Token?'
def main(profile: str, token: bool):
    """Console script for aws_key_formatter."""
    click.echo(
        "Replace this message by putting your code into aws_key_formatter.cli.main"
    )
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
