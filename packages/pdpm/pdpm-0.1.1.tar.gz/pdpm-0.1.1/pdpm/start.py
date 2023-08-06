import os

from pdpm._open import _open_launcher


import os
import pickle
import shutil
import sys
import click

from pdpm._open import _open


@click.command()
@click.argument('launcher')
def set_launcher(launcher):
    """Set the launcher"""
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'launcher.pickle'), 'wb') as f:
        pickle.dump(launcher, f)
    click.echo('Successfully changed launcher')


@click.command()
@click.argument('project_name')
def start(project_name):
    """Start project"""
    file_path = _open()
    project_path = os.path.join(file_path, project_name)
    if not os.path.isdir(project_path):
        raise FileExistsError('No project named ' + project_name)
    _start(project_path)


def _start(path):
    click.echo('Launching project')
    os.system(_open_launcher() + ' ' + path)
