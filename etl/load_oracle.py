from multiprocessing import Pool
from etl.processes import ora_to_ora
from data import OracleConnection, read_chunks, write_chunks
from etl.callbacks import *


def load(job):
    try:
        with OracleConnection.from_properties(job.key_source) as source:
            with OracleConnection.from_properties(job.key_destination) as destination:
                for df in read_chunks(source, job.read_query):
                    try:
                        # printer().send(df)
                        write_chunks(destination, job.write_stmt, df.to_dict(orient='record'))
                    except Exception as e:
                        # print(e)
                        continue
    except Exception as e:
            print(e)
    return job.name

if __name__ == '__main__':
    pool1 = Pool()
    for o in ora_to_ora:
        pool1.apply_async(func=load, args=(o,), callback=done)
    pool1.close()
    pool1.join()