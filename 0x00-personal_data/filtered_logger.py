#!/usr/bin/env python3
"""masking pii"""

import mysql.connector
from mysql.connector import connection
import os
import logging
from typing import List
import re


# Fields that need to be redacted
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:  # noqa
    """Obfuscates sensitive data in the log messages."""
    pattern = f"({'|'.join(fields)})=[^{separator}]+"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record by redacting sensitive fields."""
        original = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original, self.SEPARATOR)  # noqa


def get_logger() -> logging.Logger:
    """Returns a logger object configured to use the RedactingFormatter."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def get_db() -> connection.MySQLConnection:
    """Connects to the MySQL database using environment variables."""
    get_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    get_dbs = os.getenv("PERSONAL_DATA_DB_NAME")
    get_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    get_usr_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")

    con_db = mysql.connector.connect(
        user=get_username,
        password=get_usr_pwd,
        host=get_host,
        database=get_dbs
    )
    return con_db


def main():
    """Retrieves all rows from the users table and displays them under a filtered format."""  # noqa
    db = get_db()
    cursor = db.cursor()

    # Query to get all rows from the users table
    cursor.execute("SELECT * FROM users;")  #noqa
    users = cursor.fetchall()

    # Setup logger
    logger = get_logger()

    # Format each row and log it
    for user in users:
        log_message = (
            f"name={user[0]}; email={user[1]}; phone={user[2]}; "
            f"ssn={user[3]}; password={user[4]}; ip={user[5]}; "
            f"last_login={user[6]}; user_agent={user[7]};"
        )
        logger.info(log_message)

    # Close the cursor and connection
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
