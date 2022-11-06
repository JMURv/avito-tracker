import psycopg2
from psycopg2 import Error


def get_connection():
    connection = psycopg2.connect(
        user="postgres",
        password="794613825Zx",
        host="127.0.0.1",
        port="5432",
        database="postgres"
    )
    cursor = connection.cursor()
    return cursor, connection


def disconnect(cursor, connection):
    cursor.close()
    connection.close()


def insert_values(user_id, name, url):
    cursor, connection = get_connection()
    insert_query = f"INSERT INTO workers (USER_ID, WORKER_NAME, URL) VALUES ({user_id}, {name}, {url});"
    cursor.execute(insert_query)
    connection.commit()
    disconnect(cursor, connection)


def read_data(user_id):
    cursor, connection = get_connection()
    read_query = f"SELECT WORKER_NAME, URL FROM workers WHERE USER_ID = {user_id}"
    cursor.execute(read_query)
    data = cursor.fetchall()
    result = {}
    for row in data:
        result[row[0]] = row[1]
    connection.commit()
    disconnect(cursor, connection)
    return result


def delete_values(user_id, name):
    pass

