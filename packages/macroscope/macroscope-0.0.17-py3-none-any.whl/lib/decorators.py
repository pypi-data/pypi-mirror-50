# External libraries
import click


class Config(object):
    def __init__(self):
        self.dataReader = None


pass_config = click.make_pass_decorator(Config, ensure=True)
