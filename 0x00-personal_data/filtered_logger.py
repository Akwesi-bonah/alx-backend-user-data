#!/usr/bin/env python3

import logging
import re
from typing import List
from os import environ
import mysql.connector as mc


PII_FIELDS = ("name", "phone", "email", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Returns an obfuscated log message """
    for key in fields:
        message = re.sub(f'{key}=.*?{separator}',
                         f'{key}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    def __init__(self, fields: List[str]):
        super().__init__(
            environ.get("LOG_FORMAT", "[HOLBERTON] %(name)s " +
                        "%(levelname)s %(asctime)-15s: %(message)s"))
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filters incoming records """
        return filter_datum(self.fields, environ.get("REDACTION", "***"),
                            super().format(record),
                            environ.get("SEPARATOR", ";"))


def get_logger() -> logging.Logger:
    """ Returns a log object """
    log = logging.getLogger("user_data")
    log.setLevel(logging.INFO)
    log.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    log.addHandler(stream_handler)
    return log


def get_db() -> mc.connection.MySQLConnection:
    """ Returns a MySQL Connector """
    uname = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    pwd = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    h = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db = environ.get("PERSONAL_DATA_DB_NAME")
    return mc.connect(user=uname, password=pwd, host=h, database=db)


def main():
    """ Obtains a database connection using get_db and retrieves all rows
    in the users table then display each row under a filtered format """
    try:
        db = get_db()
        with db.cursor() as cur_db:
            cur_db.execute("SELECT * FROM users;")
            field_names = [i[0] for i in cur_db.description]
            log = get_logger()
            for r in cur_db:
                str_r = "".join(f"{f}={str(li)}; " for li,
                                f in zip(r, field_names))
                log.info(str_r.strip())
    except mc.Error as e:
        print(f"Error connecting to the database: {e}")
    finally:
        if db:
            db.close()


if __name__ == "__main__":
    main()
