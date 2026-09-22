from sqlalchemy import text
from . import db


def _to_text(query):
    if isinstance(query, str):
        return text(query)
    return query


def execute_query(query, params=None):
    """Run any statement and commit. Returns the result cursor."""
    try:
        stmt = _to_text(query)
        result = db.session.execute(stmt, params or {})
        db.session.commit()
        return result
    except Exception as e:
        db.session.rollback()
        raise e


def insert_record(query, params=None):
    """Run an INSERT and commit. Returns the new row id (lastrowid)."""
    try:
        stmt = _to_text(query)
        result = db.session.execute(stmt, params or {})
        db.session.commit()
        return result.lastrowid
    except Exception as e:
        db.session.rollback()
        raise e


def update_record(query, params=None):
    """Run an UPDATE and commit. Returns number of affected rows."""
    try:
        stmt = _to_text(query)
        result = db.session.execute(stmt, params or {})
        db.session.commit()
        return result.rowcount
    except Exception as e:
        db.session.rollback()
        raise e


def delete_record(query, params=None):
    """Run a DELETE and commit. Returns number of affected rows."""
    try:
        stmt = _to_text(query)
        result = db.session.execute(stmt, params or {})
        db.session.commit()
        return result.rowcount
    except Exception as e:
        db.session.rollback()
        raise e


def fetch_records(query, params=None):
    """Run a SELECT. Returns list of result rows."""
    try:
        stmt = _to_text(query)
        result = db.session.execute(stmt, params or {})
        return [dict(row) for row in result.mappings().all()]
    except Exception as e:
        db.session.rollback()
        raise e
