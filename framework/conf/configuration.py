import configparser
from properties import RESOURCES


class Configuration:
    __config = configparser.ConfigParser()
    filename = ''

    def __init__(self, key):
        self.key = key
        self.__config.read((f'{RESOURCES}/{self.filename}'))
        if self.key in self.__config.sections():
            self.properties = dict(self.__config[self.key])
        else:
            raise ValueError(f'Section: {self.key}, not in properties')

    def get_properties(self):
        return self.properties



