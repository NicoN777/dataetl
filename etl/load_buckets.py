from etl.processes import ora_to_bucket
from multiprocessing import Pool
from etl.properties import csv_dir
from etl.coros.coroutines import upload_to_bucket
from etl.callbacks import done, error
from data import OracleConnection, S3Bucket, read

def bucket_load(job):
    try:
        with OracleConnection.from_properties(job.key_source) as source:
            with S3Bucket.from_properties(job.key_destination) as destination:
                df = read(source, job.read_query)
                full_path = f'{csv_dir}/{job.name}.csv'
                df.to_csv(full_path, index=False)
                upload_to_bucket().send((destination, full_path))
    except Exception as e:
            print(e)

    return job.name

if __name__ == '__main__':
    pool2 = Pool()
    for ob in ora_to_bucket:
        print(ob)
        pool2.apply_async(func=bucket_load, args=(ob,), callback=done, error_callback=error)

    pool2.close()
    pool2.join()