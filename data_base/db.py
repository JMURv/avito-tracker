import psycopg2


def get_connection():
    connection = psycopg2.connect(
        user="d6b8k9ium6edr8",
        password="1c601a8274218059c21b51c002e90d8a69996dd335f745e9e8f2c42e5c8240cb",
        host="ec2-52-18-116-67.eu-west-1.compute.amazonaws.com",
        port="5432",
        database="d6b8k9ium6edr8"
    )
    cursor = connection.cursor()
    return cursor, connection


def disconnect(cursor, connection):
    cursor.close()
    connection.close()


def insert_values(user_id, name, url):
    cursor, connection = get_connection()
    insert_query = f"""
    INSERT INTO workers
    (USER_ID, WORKER_NAME, URL)
    VALUES ({user_id}, {name}, {url});
    """
    cursor.execute(insert_query)
    connection.commit()
    disconnect(cursor, connection)


def read_data(user_id):
    cursor, connection = get_connection()
    read_query = f"""
    SELECT WORKER_NAME, URL
    FROM workers
    WHERE USER_ID = {user_id}"""
    cursor.execute(read_query)
    data = cursor.fetchall()
    result = {}
    for row in data:
        result[row[0]] = row[1]
    connection.commit()
    disconnect(cursor, connection)
    return result


def delete_data(user_id, worker_name):
    cursor, connection = get_connection()
    try:
        delete_query = f"""
        DELETE FROM workers
        WHERE USER_ID = {user_id}
        AND WORKER_NAME = '{worker_name}';"""
        cursor.execute(delete_query)
        connection.commit()
        return f'Успешное удаление {worker_name}'
    except Exception:
        return f'Неправильное имя задачи {worker_name}'
    finally:
        disconnect(cursor, connection)


def count_data(user_id):
    cursor, connection = get_connection()
    count_query = f"""
    SELECT COUNT(WORKER_NAME)
    FROM workers
    WHERE USER_ID = {user_id};"""
    cursor.execute(count_query)
    data = cursor.fetchone()[0]
    connection.commit()
    disconnect(cursor, connection)
    return data
