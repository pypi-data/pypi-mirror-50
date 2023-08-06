import os
import sys
import click
from pdpm._open import _open
from pdpm.start import _start


@click.command()
@click.option('-s/-ns', '--start/--dont-start', default=False)
@click.argument('project_name')
def create(start, project_name):
    """create project"""
    # get path
    file_path = _open()
    project_path = os.path.join(file_path, project_name)
    readme_path = os.path.join(project_path + '/readme.md')
    if os.path.isdir(project_path):
        raise FileExistsError('This project already exists')
    os.mkdir(project_path)
    with open(readme_path, 'a') as f:
        pass
    if start:
        _start(project_path)
