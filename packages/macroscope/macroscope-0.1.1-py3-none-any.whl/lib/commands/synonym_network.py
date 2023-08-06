# External libraries
import click

# Local libraries
from lib.globals import synonym_network_year_range
from lib.handlers.SynonymNetworkResponseHandler import SynonymNetworkResponseHandler
from lib.decorators import pass_config

#  macroscope synonym-network -w hello -y 1990
@click.command()
@click.option("-w", "--word", required=True)
@click.option("-y", "--year", type=synonym_network_year_range, required=True)
@click.option("-s", "--synonyms-per-target", type=click.IntRange(3, 10), default=5)
@click.option("-t", "--similarity-threshold", type=click.FloatRange(0.5, 1), default=0.72)
@pass_config
def synonym_network(config, word, year, synonyms_per_target, similarity_threshold):
    handler = SynonymNetworkResponseHandler(config.dataReader)
    result = handler.handle(word, year, synonyms_per_target, similarity_threshold)
    click.echo(result)
