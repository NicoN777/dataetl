from unittest import TestCase, mock
from message import Kafka
from conf.builder import get_configuration
from message.kafkie import Kafka
from conf.kafka import KafkaTopicConfiguration
import json


class TestKafka(TestCase):

    def setUp(self) -> None:
        self.kafka_conf = get_configuration('kafka', 'TOPIC')

    def test_configuration_is_of_type(self):
        self.assertIs(type(self.kafka_conf), KafkaTopicConfiguration, 'types are A-OK')


    def test_init_config(self):
        expected = {
            'topic.name': 'default-topic',
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'default-group',
            'client.id': 'default-id',
            'enable.auto.commit': 'True',
            'session.timeout.ms': '6000,',
            'default.topic.config': {'auto.offset.reset': 'earliest'}
        }

        actual = self.kafka_conf.properties
        assert expected == actual
        assert type(actual) == dict

    def test_kafka_produce(self):
        pass
        with mock.patch('message.kafkie.Kafka.produce') as mock_produce:
            payload = dict(key=1, value=dict(name='Toast', breed='Boxer'))

    def test_kafka_consume(self):
        pass
        with mock.patch('message.kafkie.Kafka.consume') as mock_consume:
            mock_consume.create

    def tearDown(self) -> None:
        del self.kafka_conf
        # print('bye!')
