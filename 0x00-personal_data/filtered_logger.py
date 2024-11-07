import os
import mysql.connector
import logging
from typing import List

# Define PII fields that should be filtered
PII_FIELDS = ("name", "email", "phone", "ssn", "password")

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] user_data INFO %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Redacts fields in log messages."""
    for field in fields:
        message = re.sub(
            f"{field}=([^;]+)", 
            f"{field}={redaction}", 
            message
        )
    return message

def get_logger() -> logging.Logger:
    """Returns a logger configured to redact sensitive data."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger

def get_db():
    """Returns a connection to the MySQL database."""
    return mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )

def main():
    """Main function to retrieve and log user data with sensitive info redacted."""
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    logger = get_logger()

    for row in rows:
        message = (
            f"name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]}; "
            f"password={row[4]}; ip={row[5]}; last_login={row[6]}; user_agent={row[7]};"
        )
        logger.info(message)

    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
