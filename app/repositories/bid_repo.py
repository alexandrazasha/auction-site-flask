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