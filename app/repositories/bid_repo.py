from app.repositories.base_repo import BaseRepo

class BidRepository(BaseRepo):
    def create_bid(self, auction_id, bidder_email, amount):
        # Sparar ett nytt bud i databasen.
        self.execute(
            "INSERT INTO bids (auction_id, bidder_email, amount) VALUES (?, ?, ?)",
            (auction_id, bidder_email, amount)
        )

    def get_highest_bid(self, auction_id):
        # Hämtar det nuvarande högsta budet för en auktion.
        return self.query_one(
            "SELECT * FROM bids WHERE auction_id = ? ORDER BY amount DESC LIMIT 1",
            (auction_id,)
        )

    def get_top_bids(self, auction_id, limit=2):
        # Hämtar de X senaste/högsta buden (för budhistoriken).
        return self.query_all(
            "SELECT * FROM bids WHERE auction_id = ? ORDER BY amount DESC LIMIT ?",
            (auction_id, limit)
        )
    
    def get_all_bids_for_auction(self, auction_id):
        """Hämtar alla bud för en specifik auktion, sorterade från högst till lägst och sedan efter tid."""
        return self.query_all(
            "SELECT * FROM bids WHERE auction_id = ? ORDER BY amount DESC, created_at DESC",
            (auction_id,)
        )

    def search_auctions(self, keyword=None, category=None, max_price=None):
        """Hämtar auktioner baserat på sökord, kategori och prisintervall."""
        # Hämtar auktioner baserat på sökord, kategori och prisintervall.
        query = "SELECT * FROM auctions WHERE 1=1" # 1=1 är ett trick för att enkelt kunna lägga till AND-satser
        params = []

        if keyword:
            query += " AND title LIKE ?"
            params.append(f"%{keyword}%")
        if category:
            query += " AND category = ?"
            params.append(category)
        if max_price:
            query += " AND starting_bid <= ?"
            params.append(max_price)
        return self.query_all(query, tuple(params))

    def delete_bid(self, bid_id: int):
        # Tar bort ett specifikt bud från databasen.
        self.execute("DELETE FROM bids WHERE id = ?", (bid_id,))