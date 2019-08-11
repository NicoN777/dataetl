import requests
from data import OracleConnection
from data import S3Bucket
from etl.properties import get_properties
from etl.message.rabbit import RabbitConnection, RabbitChannel, RQ

class Job:
    def __init__(self, name=None, key_source=None, key_destination=None):
        self.name = name
        self.key_source = key_source
        self.key_destination = key_destination

    def __str__(self):
        return f'Name: {self.name} | Source: {self.key_source} | Destination: {self.key_destination}'

    def __repr__(self):
        return f'Job({self.name}, {self.key_source}, {self.key_destination})'

class DB(Job):
    def __init__(self, name, key_source, key_destination, read_query, write_stmt):
        super().__init__(name, key_source, key_destination)
        self.read_query = read_query
        self.write_stmt = write_stmt

class Bucket(Job):
    def __init__(self, name, key_source, key_destination, read_query):
        super().__init__(name, key_source, key_destination)
        self.read_query = read_query

class MessageQ(Job):
    def __init__(self, name, key_source, read_query, connection_key, exchange_key):
        super().__init__(name, key_source)
        self.read_query = read_query
        self.connection_key = connection_key
        self.exchange = get_properties(exchange_key)

class Http(Job):
    def __init__(self,name, key_source, key_destination):
        super().__init__(name, key_source, key_destination)


    def get(self, url, payload=None or {}):
        response = requests.get(url=url, headers=self._headers, params=payload)

        if not response.ok:
            print('Response from server: ', response.text)
            raise requests.RequestException(f'Something went wrong! {response.status_code}')
        print(response.url)
        data = response.json()
        return data['data']

    def post(self, url, payload=None or {}):
        if payload is None:
            raise ValueError('Payload cannot be empty for post')

        response = requests.post(url=url, data=payload)
        if not response.ok:
            print('Response from server: ', response.text)
            raise requests.RequestException(f'Something went wrong! {response.status_code}')
        print(response.url)
        data = response.json()
        return data['data']

