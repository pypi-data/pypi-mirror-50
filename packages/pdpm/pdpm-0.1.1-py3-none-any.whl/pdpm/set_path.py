import os
import pickle
import click


@click.command()
# ERROR when changing setpath to set_path
def setpath():
    """set projects path"""
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'path.pickle'), 'wb') as f:
        pickle.dump(os.getcwd(), f)
    click.echo('Successfully changed projects directory')
