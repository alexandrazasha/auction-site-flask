from app.db import get_db

class BidRepository:
    @staticmethod
    def create_bid(auction_id, bidder_email, amount):
        """Sparar ett nytt bud i databasen."""
        db = get_db()
        db.execute(
            "INSERT INTO bids (auction_id, bidder_email, amount) VALUES (?, ?, ?)",
            (auction_id, bidder_email, amount)
        )
        db.commit()

    @staticmethod
    def get_highest_bid(auction_id):
        """Hämtar det nuvarande högsta budet för en auktion."""
        db = get_db()
        return db.execute(
            "SELECT * FROM bids WHERE auction_id = ? ORDER BY amount DESC LIMIT 1",
            (auction_id,)
        ).fetchone()

    @staticmethod
    def get_top_bids(auction_id, limit=2):
        """Hämtar de X senaste/högsta buden (för budhistoriken)."""
        db = get_db()
        return db.execute(
            "SELECT * FROM bids WHERE auction_id = ? ORDER BY amount DESC LIMIT ?",
            (auction_id, limit)
        ).fetchall()
    
    @staticmethod
    def search_auctions(keyword=None, category=None, max_price=None):
       
        """Hämtar auktioner baserat på sökord, kategori och prisintervall."""
        db = get_db()
        
        # Startar SQL-frågan som hämtar alla rader från auktionstabellen
        query = "SELECT * FROM auctions WHERE 1=1"
        params = []

        # Lägger till filter för sökord i titeln om ett ord har skickats med
        if keyword:
            query += " AND title LIKE ?"
            params.append(f"%{keyword}%")

        # Lägger till filter för kategori om en sådan är vald
        if category:
            query += " AND category = ?"
            params.append(category)

        # Lägger till filter för högsta pris för att begränsa sökresultaten
        if max_price:
            query += " AND current_bid <= ?"
            params.append(max_price)

        # Utför sökningen i databasen och returnerar alla matchande rader
        return db.execute(query, params).fetchall()