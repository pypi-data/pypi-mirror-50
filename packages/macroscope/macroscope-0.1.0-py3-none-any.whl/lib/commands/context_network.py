# External libraries
import click

# Local libraries
from lib.enums import ContextNetworkMethod
from lib.globals import network_year_range
from lib.handlers.ContextNetworkResponseHandler import ContextNetworkResponseHandler
from lib.decorators import pass_config

#  macroscope context-network -w hello -y 1990
@click.command()
@click.option("-w", "--word", required=True)
@click.option("-y", "--year", type=network_year_range, required=True)
@click.option("-n", "--maximum-nodes", type=click.IntRange(10, 400), default=300)
@click.option("-r", "--context-relevance", type=click.FloatRange(0, 1), default=0.7)
@click.option("-c", "--context-cohesiveness", type=click.FloatRange(0, 1), default=0.7)
@click.option("-f", "--word-relevance", type=click.FloatRange(2, 4), default=3.5)  # -f for fitness
@click.option("-e", "--minimum-edges", type=click.IntRange(4, 6), default=5)
@click.option("-d", "--display-nodes", type=click.IntRange(20, 200), default=70)
@click.option("-m", "--method", type=click.Choice(["PMI", "COR"]), default="PMI")
@pass_config
def context_network(
    config,
    word,
    year,
    context_relevance,
    maximum_nodes,
    context_cohesiveness,
    word_relevance,
    minimum_edges,
    display_nodes,
    method
):
    handler = ContextNetworkResponseHandler(config.dataReader)
    result = handler.handle(
        word,
        year,
        context_relevance,
        maximum_nodes,
        context_cohesiveness,
        word_relevance,
        minimum_edges,
        display_nodes,
        parseMethodParameter(method)
    )

    click.echo(result)


def parseMethodParameter(input: str) -> ContextNetworkMethod:
    lowercase_method = input.lower()
    method = None

    if lowercase_method == 'pmi':
        method = ContextNetworkMethod.PMI
    elif lowercase_method == 'cor':
        method = ContextNetworkMethod.COR
    else:
        raise NotImplementedError("No handler implemented for method " + method.upper())

    return method
