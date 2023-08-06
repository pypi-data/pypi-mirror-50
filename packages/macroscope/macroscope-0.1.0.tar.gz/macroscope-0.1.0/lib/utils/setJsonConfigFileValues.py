# External libraries
import click

# Local libraries
from lib.utils.jsonfs import getJsonFromFile, writeJsonToFile
from lib.globals import configFileAbsolutePath, dataDirPropName


def setJsonConfigFileValues(data_dir: str):
    # Get config from file. If the file is not found then we create one and write "{}"
    fileConfig = {}
    try:
        fileConfig = getJsonFromFile(configFileAbsolutePath)
    except FileNotFoundError:
        writeJsonToFile(configFileAbsolutePath, fileConfig)

    if data_dir is not None and len(data_dir) > 0:
        fileConfig[dataDirPropName] = data_dir
        writeJsonToFile(configFileAbsolutePath, fileConfig)

    dataDirectoryAbsolutePath = fileConfig.get(dataDirPropName)
    if not dataDirectoryAbsolutePath:
        value = click.prompt('Please specify the absolute path of the Macroscope data directory', type=str)
        fileConfig[dataDirPropName] = value
        writeJsonToFile(configFileAbsolutePath, fileConfig)
