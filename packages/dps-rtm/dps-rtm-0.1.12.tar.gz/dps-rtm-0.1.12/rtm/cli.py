import click
from rtm import api


@click.command()
def main():
    api.validate()
