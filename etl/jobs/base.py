from etl.data.s3.s3helper import S3Bucket
from etl.data.db.connection import OracleConnection

class Job:
    def __init__(self, name, key_source, key_destination):
        self.name = name
        self.key_source = key_source
        self.key_destination = key_destination

    def __str__(self):
        return f'Name: {self.name} | Source: {self.key_source} | Destination: {self.key_destination}'

    def __repr__(self):
        return f'Job({self.name}, {self.key_source}, {self.key_destination})'

class OracleETL(Job):
    def __init__(self, name, key_source, key_destination, read_query, insert_stmt):
        super().__init__(name, key_source, key_destination)
        self.read_query = read_query
        self.insert_stmt = insert_stmt

class LoadBucket(Job):
    def __init__(self, name, key_source, key_destination):
        super().__init__(name, key_source, key_destination)
        self.bucket = S3Bucket.from_properties(key_destination)



