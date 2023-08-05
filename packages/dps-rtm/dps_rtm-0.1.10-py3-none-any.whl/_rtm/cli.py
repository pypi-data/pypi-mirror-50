import click
from _rtm import api


@click.command()
def rtm_cli():
    api.validate()
