import psycopg2
from psycopg2 import Error


def insert_values(user_id, name, url):
    connection = psycopg2.connect(
        user="postgres",
        password="794613825Zx",
        host="127.0.0.1",
        port="5432",
        database="postgres"
    )
    cursor = connection.cursor()
    insert_query = f"INSERT INTO workers (USER_ID, WORKER_NAME, URL) VALUES ({user_id}, {name}, {url});"
    cursor.execute(insert_query)
    connection.commit()


def delete_values(user_id, name):
    pass

