# from properties import *
#
#
# def load(job):
#     try:
#         source = BaseRequest()
#         df.read
#         with S3Bucket.from_properties(job.key_destination) as destination:
#             df = read(source, job.read_query)
#             full_path = f'{csv_dir}/{job.name}.csv'
#             df.to_csv(full_path, index=False)
#             upload_to_bucket().send((destination, full_path))
#     except Exception as e:
#             print(e)
#
#     return job.name
#
# if __name__ == '__main__':
#     pool = Pool()
#     for ob in ora_to_bucket:
#         print(ob)
#         pool.apply_async(func=load, args=(ob,), callback=done, error_callback=error)
#
#     pool.close()
#     pool.join()