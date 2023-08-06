import os
import pickle
import shutil
import sys
import click

from pdpm._open import _open


@click.command()
@click.argument('project_name')
def remove(project_name):
    """remove project"""
    # get path
    file_path = _open()
    project_path = os.path.join(file_path, project_name)
    if not os.path.isdir(project_path):
        raise FileExistsError('No project named ' + project_name)
    shutil.rmtree(project_path)
