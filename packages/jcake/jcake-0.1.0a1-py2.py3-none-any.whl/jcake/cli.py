#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Console script for jcake."""

from __future__ import absolute_import

import click
import crayons

from .meta import __version__
from .options import CONTEXT_SETTINGS, JCakeGroup
from .cli_utils import format_help


@click.group(cls=JCakeGroup, invoke_without_command=True,
             context_settings=CONTEXT_SETTINGS)
@click.version_option(prog_name=crayons.yellow("jcake", bold=True),
                      version=__version__)
@click.pass_context
def cli(ctx, **kwargs):
    if ctx.invoked_subcommand is None:
        click.echo(format_help(ctx.get_help()))


@cli.command(
    short_help="Create new Java Project based Maven.",
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True),
)
@click.option('--ms', help="MicroService Project", is_flag=True)
def create(ms, **kwargs):
    from .commands import create

    project_dir = create(ms)

    click.echo('\n\nThe target project is: {}\n'.format(project_dir))


@cli.command(
    short_help="Add sub Module for the Project created by Jcake.",
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True),
)
@click.option('--name', help="The module name")
def add_module(name, **kwargs):
    from .commands import add_module

    add_content = add_module(name)

    click.echo('\nAdd module {} successfully!\n'.format(
        str(crayons.green(name, bold=True))
    ))

    click.echo('\nAdd to you pom.xml with:\n {}\n\n'.format(
        str(crayons.yellow(add_content, bold=True))
    ))


if __name__ == "__main__":
    cli()  # pragma: no cover
