from functools import wraps


def coroutine(func):
    print(f'Initializing {func.__qualname__} coroutine')
    @wraps(func)
    def start(*args, **kwargs):
        cr = func()
        cr.send(None)
        return cr
    return start


@coroutine
def printer():
    while True:
        item = yield
        print(item)

@coroutine
def upload_to_bucket():
    while True:
        bucket, path = yield
        bucket.upload(full_file_path=path)





