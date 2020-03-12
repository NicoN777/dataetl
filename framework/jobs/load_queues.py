from multiprocessing import Pool
from data import OracleConnection, read_chunks
from framework.processes import ora_to_rmq
from framework.callbacks import *
from framework.message.rabbit import RabbitConnection, RabbitChannel
import json


def load(job):
    try:
        with OracleConnection.from_properties(job.key_source) as source:
            rabbit_connection = RabbitConnection.from_properties(job.connection_key).connection
            with RabbitChannel(rabbit_connection) as destination:
                for df in read_chunks(source, job.read_query):
                    try:
                        destination.basic_publish(exchange=job.exchange.get('exchange'),
                                                  routing_key='',
                                                  body=json.dumps(df.to_dict(orient='record'), default=str))
                    except Exception as e:
                        print(e)
    except Exception as e:
            print(e)
    return job.name

if __name__ == '__main__':
    pool = Pool()
    for job in ora_to_rmq():
        pool.apply_async(func=load, args=(job,), callback=done, error_callback=error)
    pool.close()
    pool.join()