from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .db_helpers import (
    execute_query,
    insert_record,
    update_record,
    delete_record,
    fetch_records,
)

__all__ = [
    "db",
    "execute_query",
    "insert_record",
    "update_record",
    "delete_record",
    "fetch_records",
]
