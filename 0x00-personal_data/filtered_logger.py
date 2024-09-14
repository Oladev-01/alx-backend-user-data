#!/usr/bin/env python3
"""masking pii"""
import mysql.connector
from mysql.connector import connection
import os
from typing import List
import re
import logging


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:  # noqa
    """obsfucating"""
    pattern = f"({'|'.join(fields)})=[^{separator}]+"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formatting"""
        original = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original, self.SEPARATOR)  # noqa


def get_logger() -> logging.Logger:
    """returns a logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(["ssn", "password", "ip", "user_agent"])  # noqa
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """connects to a database"""
    get_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    get_dbs = os.getenv("PERSONAL_DATA_DB_NAME")
    get_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    get_usr_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    try:
        con_db = mysql.connector.connect(
        user=get_username,
        host=get_host,
        password=get_usr_pwd,
        database=get_dbs
        )
        return con_db
    except mysql.connector.Error:
        pass
