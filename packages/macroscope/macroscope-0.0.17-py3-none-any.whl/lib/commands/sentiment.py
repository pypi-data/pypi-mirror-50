# External libraries
import click

# Local libraries
from lib.enums import SentimentPlotType
from lib.decorators import pass_config
from lib.handlers.SentimentHandler import SentimentHandler

#  macroscope sentiment -w hello -w there -t v
@click.command()
@click.option("-w", "--word", required=True, multiple=True)
@click.option(
    "-t",
    "--plot-type",
    type=click.Choice(['v', 'a', 'c']),
    default='v',
    help="Valence, Arousal, or Concreteness"
)
@pass_config
def sentiment(config, word, plot_type):
    handler = SentimentHandler(config.dataReader)
    result = handler.handle(word, parseTypeParameter(plot_type))

    click.echo(result)


def parseTypeParameter(input: str) -> SentimentPlotType:
    lowercase_type = input.lower()
    plotType = None

    if lowercase_type == 'v':
        plotType = SentimentPlotType.V
    elif lowercase_type == 'a':
        plotType = SentimentPlotType.A
    elif lowercase_type == 'c':
        plotType = SentimentPlotType.C
    else:
        raise NotImplementedError("No handler implemented for type " + type.upper())

    return plotType
