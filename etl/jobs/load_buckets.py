from etl.processes import ora_to_bucket
from multiprocessing import Pool
from etl.properties import csv_dir
from etl.coros.coroutines import upload_to_bucket
from etl.callbacks import done, error
from data import OracleConnection, S3Bucket, read

def load(job):
    try:
        with OracleConnection.from_properties(job.key_source) as source:
            with S3Bucket.from_properties(job.key_destination) as destination:
                df = read(source, job.read_query)
                full_path = f'{csv_dir}/{job.name}.csv'
                df.to_csv(full_path, index=False)
                destination.upload(full_file_path=full_path)
    except Exception as e:
            print(e)

    return job.name

if __name__ == '__main__':
    pool = Pool()
    for job in ora_to_bucket:
        pool.apply_async(func=load, args=(job,), callback=done, error_callback=error)

    pool.close()
    pool.join()