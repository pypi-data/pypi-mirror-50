# External libraries
import click

# Local libraries
from lib.commands.closest import closest
from lib.commands.context_change import context_change
from lib.commands.co_occurrence import co_occurrence
from lib.commands.drift import drift
from lib.commands.sentiment import sentiment
from lib.commands.frequency import frequency
from lib.commands.context_network import context_network
from lib.commands.synonym_network import synonym_network

from lib.utils.setJsonConfigFileValues import setJsonConfigFileValues
from lib.utils.DataReader import DataReader
from lib.utils.getDataDirPath import getDataDirPath
from lib.decorators import pass_config

#  TODO: document every command """COMMENT""" for help tool


@click.group()
@click.option('--data-dir', help='The absolute path of the Macroscope data directory.')
@pass_config
def cli(config, data_dir):
    setJsonConfigFileValues(data_dir)
    config.dataReader = DataReader(getDataDirPath())


@cli.command()
def health():
    """Returns 'Healthy!' if macroscope is healthy."""
    click.echo("Healthy!")


@cli.command()
@click.argument('data_dir', nargs=1)
def set_data_dir(data_dir):
    """Sets the absolute path where macroscope will look for the data."""
    setJsonConfigFileValues(data_dir)


cli.add_command(health)
cli.add_command(closest)
cli.add_command(context_change)
cli.add_command(co_occurrence)
cli.add_command(drift)
cli.add_command(sentiment)
cli.add_command(frequency)
cli.add_command(context_network)
cli.add_command(synonym_network)
