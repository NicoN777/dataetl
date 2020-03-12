import pika
# TODO
# from framework.conf.properties import get_properties
import time

class RabbitConnection:

    def __init__(self, user=None, password=None, host=None, port=None, *args, **kwargs):
        print(user, password, host, port)
        self.user = user
        self.__password = password
        self.host = host
        self.port = int(port)
        self.__parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=pika.PlainCredentials(self.user, self.__password)
        )
        self.connection = pika.BlockingConnection(self.__parameters)

    # @classmethod
    # def from_properties(cls, key: str):
        ## TODO
        # connection_parameters = get_properties(key)
        # return cls(**connection_parameters)

    def __enter__(self):
        if self.connection.is_closed or self.connection is None:
            self.connection = pika.BlockingConnection(self.__parameters)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class RabbitChannel:
    def __init__(self, connection=None):
        self.connection = connection
        self.channel = self.connection.channel()

    def exchange_declare(self, exchange=None, exchange_type='direct', durable=True):
        try:
            exchange = self.channel.exchange_declare(exchange=exchange,
                                                      exchange_type=exchange_type,
                                                      durable=durable)
            declare_ok = exchange.method
            print(f'Exchange declared, {declare_ok}')
        except Exception as e:
            print(e)

    def __enter__(self):
        if self.channel.is_closed or self.channel is None:
            self.channel = self.connection.channel()
        return self.channel

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.channel.close()

class RQ:

    def __init__(self, channel, queue=None, durable=True, exchange=None, routing_keys=None):
        self.channel = channel
        self.queue_name = queue
        self.durable = durable
        self.exchange = exchange
        self.routing_keys = routing_keys
        self.queue = self.channel.queue_declare(queue=self.queue_name, durable=self.durable)

    def __declare_ok(self):
        declare_ok = self.channel.queue_declare(queue=self.queue, durable=self.durable)
        return declare_ok

    @property
    def message_count(self):
        return self.__declare_ok().method.message_count

    @property
    def consumer_count(self):
        return self.__declare_ok().method.consumer_count

    def monitor(self):
        print(f'Queue Name: {str(self.queue_name)}')
        while self.consumer_count != 0 and self.message_count != 0:
            print(f'Consumer count: {self.consumer_count}\n'
                  f'Message count: {self.message_count}')
            time.sleep(2)

    def purge(self):
        messages_deleted = self.channel.queue_purge(queue=self.queue)
        print(f'{messages_deleted} messages deleted from queue[{self.queue}]')

    def delete(self):
        self.channel.que_delete(queue=self.queue)

def initialize_exchanges():
    """Take in a dict with queues and exchanges(?) need better ideas, this should do for initial demo"""
    with RabbitConnection.from_properties('General') as rabbconn:
        with RabbitChannel(rabbconn) as rabbchan:
            for exchange in ['CB', 'CMC']:
                rabbchan.exchange_declare(f'{exchange}', 'fanout')


def initialize_queues():
    pass

if __name__ == '__main__':
    # rconn = RabbitConnection.from_properties('General')
    # rchan = RabbitChannel(rconn.connection)
    # queue = RQ(rchan.channel, queue='pidgey', exchange='CMC')
    # print('')
    initialize_exchanges()