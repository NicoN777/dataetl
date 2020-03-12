from multiprocessing import Pool
from framework.framework.conf.processes import ora_to_ora
from data import OracleConnection, read_chunks, write_chunks
from framework.callbacks import *


def load(job):
    try:
        with OracleConnection.from_properties(job.key_source) as source:
            with OracleConnection.from_properties(job.key_destination) as destination:
                for df in read_chunks(source, job.read_query):
                    try:
                        write_chunks(destination, job.write_stmt, df.to_dict(orient='records'))
                    except Exception as e:
                        continue
    except Exception as e:
            print(e)
    return job.name

if __name__ == '__main__':
    pool1 = Pool()
    for job in ora_to_ora:
        pool1.apply_async(func=load, args=(job,), callback=done)
    pool1.close()
    pool1.join()