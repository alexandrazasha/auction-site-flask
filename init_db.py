import sqlite3
import os

def init_db():
    db_path = 'database.db'
    schema_path = 'schema.sql'
    
    if not os.path.exists(schema_path):
        print(f"FEL: Hittar inte {schema_path}. Kontrollera sökvägen!")
        return

    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Succé! database.db har skapats med alla tabeller.")

if __name__ == '__main__':
    init_db()