import configparser
from properties import RESOURCES


class Configuration:
    __config = configparser.ConfigParser()
    filename = ''

    def __init__(self, key):
        self.key = key
        self.__config.read((f'{RESOURCES}/{self.filename}'))
        if self.key in self.__config.sections():
            self.props = dict(self.__config[self.key])
        else:
            raise ValueError(f'Section: {self.key}, not in properties')

    @property
    def properties(self):
        return self.props

    def __str__(self):
        return ''.join(f'{k},{v}' for k, v in self.props.items())




