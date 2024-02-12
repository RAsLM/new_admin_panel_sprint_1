import sqlite3
from contextlib import contextmanager


@contextmanager
def sqlite_conn_context(db_path: str):
    connection = sqlite3.connect(db_path)
    try:
        yield connection
    finally:
        connection.close()

