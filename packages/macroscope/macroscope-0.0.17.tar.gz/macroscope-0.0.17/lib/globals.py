import os
import click

fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir)

configFileAbsolutePath = parentDir + '/macroscope-config.json'
dataDirPropName = 'dataDirectoryAbsolutePath'

#  Cli Ranges - from default settings in api
#  TODO: try to get everything to work for years between 1800 and 2000
__maxIntValue = 10000
positive_int_range = click.IntRange(1, __maxIntValue)
int_gt_one = click.IntRange(2, __maxIntValue)

closest_year_range = click.IntRange(1800, 1990)
context_change_year_range = click.IntRange(1800, 2000)
drift_year_range = click.IntRange(1800, 2000)
network_year_range = click.IntRange(1800, 2000)
synonym_network_year_range = click.IntRange(1800, 1990)
