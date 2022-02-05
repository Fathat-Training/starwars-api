# -*- coding: utf-8 -*-

# ------------------------------------------------
#    External imports
# ------------------------------------------------
from mysql.connector import connect, errors
from mysql.connector.errors import IntegrityError

# ------------------------------------------------
#    Python Imports
# ------------------------------------------------
import json

# ------------------------------------------------
#    Module Imports
# ------------------------------------------------
from errors.v1.handlers import ApiError
from config.v1.app_config import MYSQL


# ------------------------------------------------
#     Database Connection
# ------------------------------------------------

def db_connect() -> tuple:
    """
        Connects to our database

    :return:
    """

    try:
        return connect(
            host=MYSQL["host"],
            user=MYSQL["user"],
            password=MYSQL["password"],
            database=MYSQL["database"]
            )

    except Exception as e:
        # We could use an HTTP error status code of 500 or 503
        raise ApiError(message="Database Connection Error", status_code=503)


def db_insert_update(sql: str, values=None):
    """
        Calls sql on the database and
        returns the result.

    :param sql: The SQL INSERT statement
    :param values: The values to be inserted
    :return: The row ID
    """
    try:
        db = db_connect()
        with db.cursor() as cur:
            if values:
                cur.execute(sql, values)
            else:
                cur.execute(sql)
        db.commit()
        # If it's an INSERT Return the ID of the last row inserted
        if "INSERT" in sql:
            rid = cur.lastrowid
            db.close()
            return rid

    except IntegrityError as e:
        # Integrity Error normally evoked when a duplicate entry is attempted - i.e. same email address, password, etc.
        # Check Unique columns for the database
        raise ApiError(message=e.args[1], status_code=503)
    except Exception as e:
        if e.message == "Database Connection Error":
            message = "service unavailable"
        else:
            message = e.message

        raise ApiError(message=message, status_code=503)


def db_query(sql: str, values: str):
    """
        Calls sql on the database and
        returns the result.
    :param sql: The SQL statement
    :param values: The values to be substituted in the SQL query
    :return:
    """

    try:
        db = db_connect()
        with db.cursor() as cur:
            # Extract row headers
            cur.execute(sql, values)
            headers = [x[0] for x in cur.description]
            return db_json_result(cur.fetchall(), headers)
    except Exception as e:
        if e.message == "Database Connection Error":
            message = "service unavailable"
        else:
            message = e.message
        raise ApiError(message=message, status_code=503)


def db_json_result(data, headers) -> list[dict]:
    json_data = []
    for result in data:
        try:
            json_data.append(dict(zip(headers, result)))
        except TypeError:
            json_data.append(dict(zip(headers, str(result))))
    return json_data


def db_delete(sql: str, values):
    """
        Calls sql on the database for deleting rows
    :param sql: The SQL DELETE statement
    :param values: The values to be matched with rows to be deleted
    :return: The number of rows deleted
    """
    assert "DELETE" in sql, "db_delete should be called only with DELETE statements"

    try:
        db = db_connect()
        with db.cursor() as cur:
            cur.execute(sql, values)
            deleted_row_count = cur.rowcount
        db.commit()
        db.close()
        return deleted_row_count
    except Exception as e:
        if e.message == "Database Connection Error":
            message = "service unavailable"
        else:
            message = e.message

        raise ApiError(message=message, status_code=503)
