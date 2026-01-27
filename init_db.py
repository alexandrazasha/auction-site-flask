# Hjälpskript för att sätta upp databasen från grunden.
# Man kör denna fil en gång i början för att skapa databasfilen och tabellerna. /karolina
import sqlite3
import os
def init_database():
    # Initierar databasen genom att radera den gamla (om den finns)
    # och köra SQL-skriptet från schema.sql för att skapa tabeller och seed-data.
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'database.db')
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')

    # Kontrollerar om schema.sql finns
    if not os.path.exists(schema_path):
        print(f"FEL: Kunde inte hitta filen 'schema.sql'. Se till att den ligger i projektets rotmapp.")
        return

    # Radera den gamla databasfilen om den finns för en ren start
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Raderade befintlig databasfil: {db_path}")

    # Se till att 'instance'-mappen finns. exist_ok=True gör att programmet inte kraschar om mappen redan finns.
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    try:
        # Anslut till databasen (detta skapar filen om den inte finns)
        connection = sqlite3.connect(db_path)
        with open(schema_path) as f:
            # Kör alla SQL-kommandon från schema.sql-filen
            connection.executescript(f.read())
        connection.close()
        print(f"\nDatabasen har initierats framgångsrikt från schema.sql!")
        print(f"Databasfilen finns nu på: {os.path.abspath(db_path)}")
        print("Du kan nu starta appen med 'python3 run.py'")
    except Exception as e:
        print(f"Ett fel uppstod vid initiering av databasen: {e}")

# denna kod körs bara om man startar filen direkt med "python3 init_db.py"
if __name__ == '__main__':
    init_database()import sqlite3
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