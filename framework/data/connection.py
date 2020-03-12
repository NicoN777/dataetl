from abc import ABCMeta, abstractmethod
import cx_Oracle
from pymongo import MongoClient


class ConnectionDirector:
    def __init__(self):
        self.builder = None

    def construct(self, builder):
        self.builder = builder
        self.builder._build_connection()


class ConnectionBuilder(metaclass=ABCMeta):

    def __init__(self, configuration):
        pass

    @abstractmethod
    def _build_connection(self):
        pass

class ConcreteConnectionBuilder(ConnectionBuilder):

    def __init__(self, connection_type, configuration):
        self.connection_type = connection_type
        self.configuration = configuration

    def _build_connection(self):
        self.connection = self.connection_type(self.configuration)


class Connection:

    def __init__(self, user=None, password=None, host=None, port=None, *args, **kwargs):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.uri
        print(self.uri)
        # pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class OracleConnection(Connection):
    pool = None

    def __init__(self, user=None, password=None, dsn=None, *args, **kwargs):
        self.dsn = dsn
        self.pool = cx_Oracle.SessionPool(user, password, self.dsn, min=1, max=10, increment=1)

    def __enter__(self):
        print('Connected!')
        self.connection = self.pool.acquire()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pool.release(self.connection)
        print('Buh bye!')


class MongoConnection(Connection):
    uri = 'mongodb://'


class MySQLConnection(Connection):
    uri = 'mysql://'

if __name__ == '__main__':
    mongo = MongoConnection()
    client = MongoClient()
    print(client.address)
