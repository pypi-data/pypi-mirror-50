import click
from pdpm.create import create as create
from pdpm.remove import remove as remove
from pdpm.set_path import setpath as setpath
from pdpm.show import show as show
from pdpm.start import set_launcher, start


@click.group()
def cli():
    pass


cli.add_command(create)
cli.add_command(remove)
cli.add_command(setpath)
cli.add_command(show)
cli.add_command(start)
cli.add_command(set_launcher)
