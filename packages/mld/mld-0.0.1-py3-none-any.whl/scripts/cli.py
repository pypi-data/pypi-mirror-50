import logging

import click

from mld.configurator import Configurator

logging.basicConfig(level=logging.INFO, format='%(name)-12s: %(levelname)-8s: %(message)s')
log = logging.getLogger(__name__)

configurator = Configurator()


@click.group()
def cli():
    pass


@cli.command(help="Database connection")
@click.option('--host', prompt=True, required=True)
@click.option('--username', prompt=True, required=True)
@click.option('--password', prompt=True, required=True, hide_input=True)
def configure(host, username, password):
    try:
        configurator.persist(host, username, password)
    except Exception as e:
        log.error("Failed to store configuration. {}".format(str(e)))


@cli.command(help="Full path to configuration file")
def pwd():
    click.echo(configurator.get_config_path())


if __name__ == "__main__":
    cli()
