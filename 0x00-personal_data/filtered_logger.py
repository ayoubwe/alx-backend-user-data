#!/usr/bin/env python3
"""A module for filtering logs.
"""
import logging
import os
import mysql.connector
from typing import List
from . import filter_datum

PII_FIELDS = ("email", "phone", "ssn", "password", "name")

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        return filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)

def get_logger() -> logging.Logger:
    """ Create and configure logger """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    
    logger.addHandler(handler)
    
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Connect to the MySQL database using environment variables """
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME', '')

    return mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_name
    )

def main():
    """ Main function to read and filter data """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    
    for row in cursor:
        message = "; ".join(f"{key}={value}" for key, value in row.items())
        logger.info(message)
    
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
