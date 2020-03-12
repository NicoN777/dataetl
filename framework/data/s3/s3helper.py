from boto3.session import Session, Config
from framework.framework.conf.properties import get_properties
import os


def get_bucket(key, secret, host, bucket_name):
    try:
        session = Session(aws_access_key_id=key,
                          aws_secret_access_key=secret,
                          region_name='us-east-2')
        s3 = session.resource('s3',
            endpoint_url=host,
            config=Config(signature_version='s3v4',
                          s3={'addressing_style':'path'}))
        bucket = s3.Bucket(bucket_name)
        return bucket
    except Exception as e:
        print(e)

class S3Bucket:
    def __init__(self, key=None, secret=None, host=None, bucket_name=None):
            self.__bucket = get_bucket(key, secret, host, bucket_name)

    @classmethod
    def from_properties(cls, key):
        return cls(**get_properties(key))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def list_objects(self):
        for object in self.__bucket.objects.all():
            print(object.key)

    def get_objects_info(self):
        objs = [dict(key=obj.key,
                     # owner=obj.id,
                     e_tag=obj.e_tag,
                     last_modified=obj.last_modified)
                for obj in self.__bucket.objects.all()]
        return objs

    def upload(self, full_file_path):
        try:
            path = os.path.abspath(full_file_path)
            file = os.path.basename(full_file_path)
            self.__bucket.upload_file(Filename=path, Key=file)
            print(f'{file}, uploaded.')
        except Exception as e:
            print(e)

    def delete(self, file):
        try:
            obj = self.__bucket.Object(file)
            obj.delete()
            print(f'{file}, deleted.')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    kowka = S3Bucket.from_properties('CAT')
    kowka.list_objects()
