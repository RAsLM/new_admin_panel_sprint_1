import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

from sqlite_to_postgres.sqlite_context import sqlite_conn_context


def test_count_rows():
    load_dotenv()
    dsl = {
        "dbname": os.environ.get("DB_NAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
        "host": os.environ.get("DB_HOST"),
        "port": os.environ.get("DB_PORT"),
        'options': '-c search_path=public,content',
    }
    SQLITE_NAME = "../db.sqlite"
    with sqlite_conn_context(SQLITE_NAME) as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        sqlite_cursor = sqlite_conn.cursor()
        pg_cursor = pg_conn.cursor()

        table_names = ["film_work", "genre", "genre_film_work", "person", "person_film_work"]
        for table_name in table_names:
            query = f"SELECT COUNT(id) FROM {table_name};"
            sqlite_cursor.execute(query)
            pg_cursor.execute(query)
            assert sqlite_cursor.fetchone()[0] == pg_cursor.fetchone()[0], (
                f"Количество строк в таблице {table_name} различается для "
                "баз данных SQLite и PostgreSQL"
            )
