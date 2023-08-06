import os

import click

from pdpm._open import _open


@click.command()
def show():
    """Show all projects"""
    path = _open()
    projects = [p for p in os.listdir(path) if os.path.isdir(os.path.join(path, p))]
    for p in projects:
        click.echo(p)
