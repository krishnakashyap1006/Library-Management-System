import os
from contextlib import contextmanager

import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "1234"),
        database=os.getenv("MYSQL_DATABASE", "lib_management"),
    )


@contextmanager
def db_session():
    connection = None
    try:
        connection = get_connection()
        yield connection
        connection.commit()
    except Exception:
        if connection is not None and connection.is_connected():
            connection.rollback()
        raise
    finally:
        if connection is not None and connection.is_connected():
            connection.close()
