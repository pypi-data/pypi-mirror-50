# External libraries
import click

# Local libraries
from lib.handlers.CooccurrenceResponseHandler import CooccurrenceResponseHandler
from lib.decorators import pass_config


#  macroscope co-occurrence -w hello -c there -c hi
@click.command()
@click.option("-w", "--word", required=True)
@click.option("-c", "--context-word", required=True, multiple=True)
@click.option("-n", "--normalize", is_flag=True, default=False)
@pass_config
def co_occurrence(config, word, context_word, normalize):
    """Returns co-occurrence between target word and context words for every year."""

    handler = CooccurrenceResponseHandler(config.dataReader)

    result = handler.handle(word, context_word, normalize)
    click.echo(result)
