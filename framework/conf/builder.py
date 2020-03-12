from abc import ABCMeta, abstractmethod
from conf.db import OracleConfiguration
from conf.s3 import S3Configuration


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
oracle_config_builder = ConcreteConfigurationBuilder(OracleConfiguration, 'WOLF')
s3_buckets_config_builder = ConcreteConfigurationBuilder(S3Configuration, 'CAT')

configuration_director.construct(oracle_config_builder)
configuration_director.construct(s3_buckets_config_builder)
oracle_wolf = oracle_config_builder.configuration
s3_cat = s3_buckets_config_builder.configuration

print(oracle_wolf.get_properties())
print(s3_cat.get_properties())