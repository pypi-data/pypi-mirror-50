# External libraries
import click

# Local libraries
from lib.globals import drift_year_range, int_gt_one, positive_int_range
from lib.decorators import pass_config
from lib.handlers.DriftResponseHandler import DriftResponseHandler

# TODO: add capability to handle multile words?
#  macroscope drift -w hello -s 1850 -e 2000
@click.command()
@click.option("-w", "--word", required=True)
@click.option("-s", "--start-year", type=drift_year_range, required=True)
@click.option("-e", "--end-year", type=drift_year_range, required=True)
@click.option("-n", "--number-of-years-in-interval", type=int_gt_one, default=5)
@click.option("-k", "--number-of-closest-words", type=positive_int_range, default=10)
@pass_config
def drift(config, word, start_year, end_year, number_of_years_in_interval, number_of_closest_words):
    """Returns drift of words over a given period."""

    handler = DriftResponseHandler(config.dataReader)
    result = handler.handle(word, start_year, end_year, number_of_years_in_interval, number_of_closest_words)

    click.echo(result)
