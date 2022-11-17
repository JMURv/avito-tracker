import psycopg2
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def get_connection():
    connection = psycopg2.connect(
        user=os.getenv('user'),
        password=os.getenv('password'),
        host=os.getenv('host'),
        port=os.getenv('port'),
        database=os.getenv('database')
    )
    cursor = connection.cursor()
    return cursor, connection


def disconnect(cursor, connection):
    cursor.close()
    connection.close()
