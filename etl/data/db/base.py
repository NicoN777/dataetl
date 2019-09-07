import pandas as pd
from etl.properties import _chunk_size

def read_chunks(connection, query=None, params={}):
    cursor = connection.cursor()
    result_set = cursor.execute(query, params)
    columns = list(map(lambda x: x[0], result_set.description))
    while True:
        data = result_set.fetchmany(_chunk_size)
        if not data:
            break
        df = pd.DataFrame(columns=columns, data=data)
        yield df

def read(connection, query=None, params={}):
    df = pd.read_sql(sql=query, con=connection)
    return df

def write_chunks(connection, stmt=None, params={}):
    cursor = connection.cursor()
    result_set = cursor.executemany(stmt, params)
    connection.commit()
