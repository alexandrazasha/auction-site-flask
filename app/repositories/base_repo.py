from app.db import get_db

class BaseRepo:
    def query_all(self, sql: str, params: tuple = ()):
        db = get_db()
        return db.execute(sql, params).fetchall()

    def query_one(self, sql: str, params: tuple = ()):
        db = get_db()
        return db.execute(sql, params).fetchone()

    def execute(self, sql: str, params: tuple = ()):
        db = get_db()
        cur = db.execute(sql, params)
        db.commit()
        return cur.lastrowid
