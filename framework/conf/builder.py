from abc import ABCMeta, abstractmethod
from conf.db import *
from conf.s3 import *
from conf.logger import *
from conf.kafka import *
from conf.slacker import *


class ConfigurationDirector:
    def __init__(self):
        self.builder = None

    def construct(self, builder):
        self.builder = builder
        self.builder._build_config()


class ConfigurationBuilder(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, configuration_kind):
        pass

    @abstractmethod
    def _build_config(self):
        pass


class ConcreteConfigurationBuilder(ConfigurationBuilder):
    def __init__(self, configuration_kind, key):
        self.configuration_kind = configuration_kind
        self.key = key

    def _build_config(self):
        self.configuration = self.configuration_kind(self.key)
        return self.configuration


configuration_director = ConfigurationDirector()


def get_configuration(kind, key):
    if kind == 'ora':
        concrete_builder = ConcreteConfigurationBuilder(OracleConfiguration, key)
    if kind == 'mongo':
        concrete_builder = ConcreteConfigurationBuilder(MongoConfiguration, key)
    if kind == 'cassandra':
        concrete_builder = ConcreteConfigurationBuilder(CassandraConfiguration, key)
    if kind == 'postgres':
        concrete_builder = ConcreteConfigurationBuilder(PostgresConfiguration, key)
    if kind == 'kafka':
        concrete_builder = ConcreteConfigurationBuilder(KafkaTopicConfiguration, key)
    if kind == 'logger':
        concrete_builder = ConcreteConfigurationBuilder(LoggerConfiguration, key)
    if kind == 's3':
        concrete_builder = ConcreteConfigurationBuilder(S3Configuration, key)
    if kind == 'slack':
        concrete_builder = ConcreteConfigurationBuilder(SlackConfiguration, key)
    configuration_director.construct(concrete_builder)
    return concrete_builder.configuration
