import os
import sqlite3
from contextlib import closing

from sqlite_context import sqlite_conn_context

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from models import FilmWork, Person, Genre, PersonFilmWork, GenreFilmWork
from dataclasses import fields, astuple


class SQLiteExtractor:

    def __init__(self):
        self.queries = {
            FilmWork: "SELECT title, description, creation_date, file_path, type, created_at, updated_at, id, rating FROM film_work;",
            Genre: "SELECT name, description, created_at, updated_at, id from genre;",
            GenreFilmWork: "SELECT film_work_id, genre_id, created_at, id from genre_film_work;",
            Person: "SELECT full_name, created_at, updated_at, id from person;",
            PersonFilmWork: "SELECT film_work_id, person_id, role, created_at, id from person_film_work;",
        }

    def extract_tables(self, connection, dt, query):
        with closing(connection.cursor()) as sqlite_cursor:

            sqlite_cursor.execute(query)
            data = sqlite_cursor.fetchmany()
            dt_data = [dt(*element) for element in data]

            return dt_data


class PostgresSaver:

    def __init__(self):
        self.tables = {
            FilmWork: "film_work",
            Genre: "genre",
            GenreFilmWork: "genre_film_work",
            Person: "person",
            PersonFilmWork: "person_film_work",
        }

    def save_all_data(self, data, connection, dt):
        column_names = [field.name for field in fields(data[0])]  # [id, name]
        column_names_str = ','.join(column_names)
        # В зависимости от количества колонок генерируем под них %s.
        col_count = ', '.join(['%s'] * len(column_names))  # '%s, %

        bind_values = ','.join(connection.cursor().mogrify(f"({col_count})", astuple(field)).decode('utf-8') for field in data)

        table_name = self.tables[dt]

        query = f"INSERT INTO content.{table_name} ({column_names_str}) VALUES {bind_values} ON CONFLICT (id) DO NOTHING"

        connection.cursor().execute(query)


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver()
    sqlite_extractor = SQLiteExtractor()

    for dt, query in sqlite_extractor.queries.items():
        data_from_sqlite = sqlite_extractor.extract_tables(connection, dt, query)
        postgres_saver.save_all_data(data_from_sqlite, pg_conn, dt)


if __name__ == '__main__':
    load_dotenv()
    dsl = {
        "dbname": os.environ.get("DB_NAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
        "host": os.environ.get("DB_HOST"),
        "port": os.environ.get("DB_PORT"),
        'options': '-c search_path=public,content',
    }
    SQLITE_NAME = os.environ.get("SQLITE_NAME")
    with sqlite_conn_context(SQLITE_NAME) as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
