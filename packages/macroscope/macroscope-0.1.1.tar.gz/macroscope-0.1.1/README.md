# Macroscope-cli

Macroscope cli written in python3.

## Usage

Install using pip

```shell
pip3 install macroscope
```

To verify install, run the command

```shell
macroscope --help
```

This should output help text about the available commands.

To start using the Macroscope cli you must download the Macroscope data and specify it's absolute location.

TODO: host macroscope data publicly and provide download instructions

Set the data location with the following command

```shell
macroscope set-data-dir ~/macroscope-data
```

Assuming the location of your Macroscope data is ```~/macroscope-data```.

## Development

### Setup

To setup the project environment and install the required packages, run the command

```shell
make install
```

Then activate the ```venv``` environment. Instructions to do so are given below.

### Venv

Venv is a tool to create a virtual python environment for a project.

#### Create environment

```shell
make create-venv
```

This will create a ```venv``` directory which should not be committed to source control.

#### Activate environment

```shell
source ./venv/bin/activate
```

or equivalently

```shell
. ./venv/bin/activate
```

When the environment is activated, the prefix ```./venv/bin/``` used for commands can be dropped.

For example ```./venv/bin/pip3 install package-name``` becomes ```pip3 install package-name```

#### Deactivate environment

```shell
deactivate
```

### Installing new packages

Install new packages with ```pip```

```shell
pip install package-name
```

When new packages are installed, the following command must be run to output installed packages to ```requirements.txt```

```shell
pip freeze > requirements.txt
```

### Publishing package to PyPI

To publish package to PyPI, run the command

```shell
make publish
```

and enter your PyPI credentials

## Possible errors when developing

### Vscode linter doesn't recognise imported packages in venv environment

* Use ```flake8``` linter
* Open ```vscode``` from activated ```venv``` terminal using the command

```shell
code .
```

### Removing existing ```macroscope-config.json``` file

After installing the ```macroscope``` cli from PyPI for the first time, you will be prompted to enter the location of the data directory. When uninstalling the ```macroscope```, this config file will not be deleted. This means that if you reinstall the ```macroscope``` you will not be prompted. You can delete this config file with the following command.

```shell
rm ~/.local/lib/python3.6/site-packages/macroscope-config.json
```

## Blogs

* [Why I hate virtualenv and pip](https://pythonrants.wordpress.com/2013/12/06/why-i-hate-virtualenv-and-pip/)
* [Things you are probably not using in python3 but should](https://datawhatnow.com/things-you-are-probably-not-using-in-python-3-but-should/)
* [Installing python on debian](https://matthew-brett.github.io/pydagogue/installing_on_debian.html)
* [Publishing python packages](https://realpython.com/pypi-publish-python-package/)

### Package management

* [Reference blog](https://chriswarrick.com/blog/2018/09/04/python-virtual-environments/)

## Possible tools

* [pip-tools](https://github.com/jazzband/pip-tools)
* [poetry](https://github.com/sdispater/poetry)
* [conda](https://github.com/conda/conda)
* [hatch](https://github.com/ofek/hatch)
* [flit](https://github.com/takluyver/flit)
* [buildout](https://github.com/buildout/buildout)

## Notes

* [Public, Private, and Protected in python](https://radek.io/2011/07/21/private-protected-and-public-in-python/)
* [MakeFiles](https://krzysztofzuraw.com/blog/2016/makefiles-in-python-projects.html)
* [Example type hinting](https://github.com/ActivityWatch/aw-core/blob/master/aw_core/models.py)

* [Possible existing python package](https://github.com/williamleif/histwords) - [Blog outlining method](https://aryamccarthy.github.io/hamilton2016diachronic/) - [Another paper](https://www.aclweb.org/anthology/C18-1117)

### Method acronyms

* [SGNS](https://mccormickml.com/2016/04/19/word2vec-tutorial-the-skip-gram-model/)
* [SVD](https://en.wikipedia.org/wiki/Singular_value_decomposition)

## Implementations of similar projects

* [sgns-hamilton](https://nlp.stanford.edu/projects/histwords/) - [source code](https://github.com/williamleif/histwords)

## TODO:

* All ```getWordObj``` functions should only take wordValue as a parameter and no other parameters. Possible DataReader refactor needed where each word space controls the getting and caching of data and the DataReader is simply a wrapper round the data directory - more details in todos in DataReader
* Test non decade years for all commands using years - for example ```macroscope closest -y 1997```. Some commands should only accept decades - drift for example
* Add proper cli exception handling - https://stackoverflow.com/questions/52213375/python-click-exception-handling-under-setuptools
* consider case sensitivity with word inputs
* Add MANIFEST.in file
* figure out what to do with data directory
    * Download data using wget and add command to build and dev process - host zipped data file online - use https and all
* sgns-hamilton doesn't have a year 2000 file
* Look into running python in a virtual machine
* Use a MakeFile
* Logging?
* use tox?
* use [mypy](https://github.com/python/mypy)?
* Start of context change function looks very similar to plotCooccurrence function
* make cli compatible with windows

## Discussion to have

* Make project open source? Which LICENSE?
