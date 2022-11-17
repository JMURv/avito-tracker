from psycopg2 import errors
from avito_tracker.data_base.connection import get_connection, disconnect


def register_user(user_id):
    is_registered = False
    cursor, connection = get_connection()
    try:
        reg_query = f"""
            INSERT INTO users
            (user_id, is_tracking)
            VALUES ({user_id}, {0});
            """
        cursor.execute(reg_query)
        connection.commit()
    except errors.UniqueViolation:
        is_registered = True
    finally:
        disconnect(cursor, connection)
        return is_registered


def is_tracking_now(user_id):
    cursor, connection = get_connection()
    query = f"""
    SELECT is_tracking
    FROM users
    WHERE user_id = {user_id};"""
    cursor.execute(query)
    data = cursor.fetchone()[0]
    connection.commit()
    disconnect(cursor, connection)
    return data


def enable_track(user_id):
    cursor, connection = get_connection()
    insert_query = f"""
        UPDATE users
        SET is_tracking = 1
        WHERE user_id = {user_id};
        """
    cursor.execute(insert_query)
    connection.commit()
    disconnect(cursor, connection)


def disable_track(user_id):
    cursor, connection = get_connection()
    insert_query = f"""
    UPDATE users
    SET is_tracking = 0
    WHERE user_id = {user_id};
    """
    cursor.execute(insert_query)
    connection.commit()
    disconnect(cursor, connection)
