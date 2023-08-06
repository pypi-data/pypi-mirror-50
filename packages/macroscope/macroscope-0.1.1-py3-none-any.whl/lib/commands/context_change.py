# External libraries
import click

# Local libraries
from lib.handlers.ContextChangeResponseHandler import ContextChangeResponseHandler
from lib.globals import context_change_year_range, positive_int_range
from lib.decorators import pass_config

#  macroscope context-change -w hello -s 1990 -e 2000
@click.command()
@click.option("-w", "--word", required=True, multiple=True)
@click.option("-s", "--start-year", type=context_change_year_range, required=True)
@click.option("-e", "--end-year", type=context_change_year_range, required=True)
@click.option("-k", "--number-of-context-words", type=positive_int_range, default=10)
@click.option("-i/-d", "--increase/--decrease", default=True)
@pass_config
def context_change(config, word, start_year, end_year, number_of_context_words, increase):
    """
    Returns context change of search term over given period of years.
    """

    # TODO: figure out why the current macroscope returns positive and negative values for words

    if start_year > end_year:
        click.echo("Start year: " + str(start_year) + " must be before End year: " + str(end_year))
        return

    handler = ContextChangeResponseHandler(config.dataReader)

    result = handler.handle(word, start_year, end_year, number_of_context_words, increase)
    click.echo(result)
