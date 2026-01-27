# Hjälpskript för att sätta upp databasen från grunden.
# Kör denna fil en gång i början för att skapa databasfilen och tabellerna.
import sqlite3
import os


def init_database():
    # Skapa DB i instance/
    base_dir = os.path.dirname(__file__)
    db_path = os.path.join(base_dir, "instance", "database.db")
    schema_path = os.path.join(base_dir, "schema.sql")

    if not os.path.exists(schema_path):
        print("FEL: Kunde inte hitta 'schema.sql' i projektets rotmapp.")
        return

    # Ren start: radera DB om den finns
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Raderade befintlig databasfil: {db_path}")

    # Se till att instance/ finns
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Skapa tabeller från schema.sql
    conn = sqlite3.connect(db_path)
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

    print("\n✅ Databasen har initierats från schema.sql!")
    print(f"✅ Databasfilen finns nu på: {os.path.abspath(db_path)}")
    print("👉 Starta appen med: python run.py")


if __name__ == "__main__":
    init_database()
