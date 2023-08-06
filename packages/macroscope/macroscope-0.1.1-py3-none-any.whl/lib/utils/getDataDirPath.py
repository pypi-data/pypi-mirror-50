from lib.utils.jsonfs import getJsonFromFile
from lib.globals import configFileAbsolutePath, dataDirPropName


def getDataDirPath():
    return getJsonFromFile(configFileAbsolutePath).get(dataDirPropName)
