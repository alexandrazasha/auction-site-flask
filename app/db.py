import sqlite3
from pathlib import Path
import os
from flask import current_app, g

def get_db():
    # Returnerar en SQLite-connection (återanvänds per request).
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db

def close_db(_e=None):
    # Stänger DB-connection efter request.
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    # Skapar tabeller enligt schema.sql.
    # Stänger befintlig connection om den finns
    close_db()
    # Radera den gamla databasfilen för att säkerställa en ren start
    db_path = Path(current_app.config["DATABASE"])
    if db_path.exists():
        os.remove(db_path)
    db = get_db()
    schema_path = Path(current_app.root_path).parent / "schema.sql"
    db.executescript(schema_path.read_text(encoding="utf-8"))
    db.commit()

def init_app(app):
    # Kopplas in i create_app().
    app.teardown_appcontext(close_db)

    @app.cli.command("init-db")
    def init_db_command():
        init_db()
        print("Initialized the database.")
