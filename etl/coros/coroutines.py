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
def load_oracle():
    while True:
        destination, writer, stmt, df = yield
        writer(destination, stmt, df.to_dict(orient='record'))

@coroutine
def push_message():
    pass

@coroutine
def upload_to_bucket():
    while True:
        bucket, path = yield
        bucket.upload(full_file_path=path)


@coroutine
def cb_indicators(df):
    pass

@coroutine
def cmc_indicators(df):
    pass
