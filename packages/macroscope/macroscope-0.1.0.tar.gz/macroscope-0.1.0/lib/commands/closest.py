# External libraries
import click

# Local libraries
from lib.enums import ClosestSearchMethod
from lib.globals import closest_year_range, positive_int_range
from lib.handlers.ClosestResponseHandler import ClosestResponseHandler
from lib.decorators import pass_config


def parseMethodEnum(method: str):
    if method == "svd":
        return ClosestSearchMethod.SVD
    elif method == "sgns":
        return ClosestSearchMethod.SGNS


#  macroscope closest -w hello -y 1990
@click.command()
@click.option("-w", "--word", required=True, multiple=True)
@click.option("-y", "--year", type=closest_year_range, required=True)
@click.option("-k", "--number-of-closest-words", type=positive_int_range, default=10)
@click.option("-m", "--method", type=click.Choice(["svd", "sgns"]), default="svd")
@pass_config
def closest(config, word, year, number_of_closest_words, method):
    """
    Returns closest synonyms to word for a given year.
    """
    # TODO: Year must be a multiple of 10 - how shall I deal with this?
    # same for context change

    handler = ClosestResponseHandler(config.dataReader)

    result = handler.handle(word, year, number_of_closest_words, parseMethodEnum(method))
    click.echo(result)
