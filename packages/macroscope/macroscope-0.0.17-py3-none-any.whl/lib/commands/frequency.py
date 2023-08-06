# External libraries
import click

# Local libraries
from lib.decorators import pass_config
from lib.handlers.FrequencyResponseHandler import FrequencyResponseHandler


#  macroscope frequency -w hello -w there
@click.command()
@click.option("-w", "--word", required=True, multiple=True)
@click.option("-f", "--match-full-word", is_flag=True)
@click.option("-s", "--match-start", is_flag=True)
@click.option("-m", "--match-middle", is_flag=True)
@click.option("-e", "--match-end", is_flag=True)
@pass_config
def frequency(config, word, match_full_word, match_start, match_middle, match_end):
    # If no flags provided, default result to match full word
    if match_full_word is False and match_start is False and match_middle is False and match_end is False:
        match_full_word = True

    handler = FrequencyResponseHandler(config.dataReader)
    result = handler.handle(word, match_full_word, match_start, match_middle, match_end)

    click.echo(result)
