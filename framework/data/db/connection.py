from framework.framework.conf.properties import get_oracle_properties
import cx_Oracle


class OracleConnection:
    pool = None
    def __init__(self, user=None, password=None, dsn=None, *args, **kwargs):
        self.pool = cx_Oracle.SessionPool(user, password, dsn, min=1, max=10, increment=1)

    @classmethod
    def from_properties(cls, key:str):
        return cls(**get_oracle_properties(key))

    def __enter__(self):
        print('Connected!')
        self.connection = self.pool.acquire()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pool.release(self.connection)
        print('Buh bye!')


if __name__ == '__main__':
    w = OracleConnection.from_properties('WOLF')
    # l = OracleConnection.from_properties('LION')

    print('')