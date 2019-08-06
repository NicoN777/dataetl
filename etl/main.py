from etl.data.db.base import read_chunks, read, write_chunks
from etl.data.db.connection import OracleConnection
from etl.data.s3.s3helper import S3Bucket
from multiprocessing import Pool
from etl.processes import ora_to_ora, ora_to_bucket
from etl.properties import csv_dir
from etl.coros.coroutines import printer, upload_to_bucket



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


def bucket_load(job):
    print('****')
    try:
        with OracleConnection.from_properties(job.key_source) as source:
            # destination = S3Bucket.from_properties(job.key_destination)
            with S3Bucket.from_properties(job.key_destination) as destination:
                df = read(source, job.read_query)
                full_path = f'{csv_dir}/{job.name}.csv'
                df.to_csv(full_path, index=False)
                upload_to_bucket().send((destination, full_path))
    except Exception as e:
            print(e)

    return job.name

def done(x):
    print(x, 'DONE!')

def error(x):
    print(x, 'ERROR!')

if __name__ == '__main__':
    pool1 = Pool()
    for o in ora_to_ora:
        pool1.apply_async(func=load, args=(o,), callback=done)
    pool1.close()
    pool1.join()

    pool2 = Pool()
    for ob in ora_to_bucket:
        print(ob)
        pool2.apply_async(func=bucket_load, args=(ob,), callback=done, error_callback=error)

    pool2.close()
    pool2.join()

#raise SystemExit(0)
