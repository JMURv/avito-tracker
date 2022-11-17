from avito_tracker.data_base.connection import get_connection, disconnect


def insert_values(user_id, name, url):
    cursor, connection = get_connection()
    insert_query = f"""
    INSERT INTO workers
    (USER_ID, TASK_NAME, TASK_URL)
    VALUES ({user_id}, {name}, {url});
    """
    cursor.execute(insert_query)
    connection.commit()
    disconnect(cursor, connection)


def read_data(user_id):
    cursor, connection = get_connection()
    read_query = f"""
    SELECT TASK_NAME, TASK_URL
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
        AND TASK_NAME = '{worker_name}';"""
        cursor.execute(delete_query)
        connection.commit()
        return f'Успешное удаление {worker_name}'
    except Exception:
        return f'Неправильное имя задачи {worker_name}'
    finally:
        disconnect(cursor, connection)
