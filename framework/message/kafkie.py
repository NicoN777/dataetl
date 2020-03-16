from conf.builder import get
from confluent_kafka import Consumer, Producer, KafkaError


class Kafka:
    def __init__(self, configuration=None):
        if configuration is None:
            raise ValueError("Configurations must be specified to initialize")
        self.kafka_settings = configuration
        self.kafka_topic = self.kafka_settings.pop('topic.name')

    def consume(self):
        self.consumer = Consumer(self.kafka_settings)
        self.consumer.subscribe([self.kafka_topic])
        try:
            while True:
                data = self.consumer.poll(0.1)
                if data is None:
                    continue
                elif not data.error():
                    print(f'Consuming from: {data.topic()} \n'
                          f'Partition: {data.partition()} \n'
                          f'Key: {data.key()} \n'
                          f'Value: {data.value()} \n'
                          f'Timestamp: {data.timestamp()}')
                    print('Received message: {0}'.format(data.value()))
                elif data.error().code() == KafkaError._PARTITION_EOF:
                    print('End of partition reached {0}/{1}'.format(data.topic(), data.partition()))
                else:
                    print('Error occured: {0}'.format(data.error().str()))

        except KeyboardInterrupt:
            pass

        finally:
            self.consumer.close()

    def produce(self, key=None, value=None, callback=None):
        self.producer = Producer(dict(self.kafka_settings['bootstrap.servers']))
        try:
            self.producer.produce(self.kafka_topic, value=value, callback=callback)
            self.producer.poll(0.5)
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
   pass