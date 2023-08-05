import click
from rtm import api


@click.command()
def rtm_cli():
    api.validate()
