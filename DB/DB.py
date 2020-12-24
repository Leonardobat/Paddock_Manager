import sqlite3
from pathlib import Path


def get_db():
    path = Path.cwd() / 'sav' / 'Data.db'
    db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    return db


def create_new_db(name):
    path = Path.cwd() / 'sav' / '{}.db'.format(name)
    db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    with open('schema_db.sql') as f:
        db.executescript(f.read())
        db.execute("VACUUM")
        db.commit()
        db.close()

    return 'Done'


def init_db():
    print("Starting Databases...")
    db = get_db()
    path = Path.cwd() / 'sav' / 'schema_db.sql'
    with Path.open(path) as f:
        db.executescript(f.read())
        db.execute("VACUUM")
        db.commit()
        db.close()
    print("DB initialized")


def create_new_save(name):
    path = Path.cwd() / 'sav' / '{}.sav'.format(name)
    db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    return db


if __name__ == '__main__':
    init_db()
