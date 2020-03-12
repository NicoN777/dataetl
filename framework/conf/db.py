from cx_Oracle import makedsn
from conf.configuration import Configuration


class OracleConfiguration(Configuration):
    filename = 'oracle_connections.ini'

    def get_properties(self):
        temp = self.properties
        if temp ['sid']== '' and temp['service_name'] == '':
            raise ValueError('sid or service_name must be specified')
        if temp['sid'] is '':
            temp.pop('sid')
        if temp['service_name'] is '':
            temp.pop('service_name')
        connection_details = {'user':temp.pop('user'), 'password': temp.pop('password'), 'dsn': makedsn(**temp)}
        return  connection_details

    def make_dsn(self):
        print(self.get_properties())


class MongoConfiguration(Configuration):
    pass


class CassandraConfiguration(Configuration):
    pass


class PostgresConfiguration(Configuration):
    pass


if __name__ == '__main__':
    print('hmm')