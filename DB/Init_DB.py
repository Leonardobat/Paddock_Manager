import sqlite3
from pathlib import Path
"""Implement 3 Databases independent each other to reduce threading-limits"""


def get_db():
    path = Path.cwd() / 'Data.db'
    db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    return db


def create_new_db(name):
    path = Path.cwd() / name / '.db'
    db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    return db


def create_new_save(name):
    path = Path.cwd() / name / '.sav'
    db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    print("Starting Databases...")

    db = get_db()
    with open('schema_db.sql') as f:
        db.executescript(f.read())
        db.execute("VACUUM")
        db.commit()
        db.close()

    print("DB initialized")


if __name__ == '__main__':
    init_db()
