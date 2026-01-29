from app.repositories.base_repo import BaseRepo


class BidRepository(BaseRepo):

    # =========================
    # BUD
    # =========================

    def create_bid(self, auction_id, bidder_email, amount):
        """Sparar ett nytt bud i databasen."""
        self.execute(
            "INSERT INTO bids (auction_id, bidder_email, amount) VALUES (?, ?, ?)",
            (auction_id, bidder_email, amount)
        )

    def get_highest_bid(self, auction_id):
        """Hämtar det nuvarande högsta budet för en auktion."""
        return self.query_one(
            "SELECT * FROM bids WHERE auction_id = ? ORDER BY amount DESC LIMIT 1",
            (auction_id,)
        )

    def get_top_bids(self, auction_id, limit=2):
        """Hämtar de X högsta buden för en auktion."""
        return self.query_all(
            "SELECT * FROM bids WHERE auction_id = ? ORDER BY amount DESC LIMIT ?",
            (auction_id, limit)
        )

    def get_all_bids_for_auction(self, auction_id):
        """Hämtar alla bud för en auktion."""
        return self.query_all(
            "SELECT * FROM bids WHERE auction_id = ? ORDER BY amount DESC, created_at DESC",
            (auction_id,)
        )

    def delete_bid(self, bid_id):
        """Tar bort ett bud."""
        self.execute(
            "DELETE FROM bids WHERE id = ?",
            (bid_id,)
        )

    # =========================
    # SÖK & FILTER (AUKTIONER)
    # =========================

    def search_auctions(self, keyword=None, category=None, max_price=None, end_before=None):
        """
        Hämtar auktioner baserat på:
        - keyword (titel + beskrivning)
        - category
        - max_price (startbud)
        - end_before (sluttid)
        """
        query = "SELECT * FROM auctions WHERE 1=1"
        params = []

        # Sökord
        if keyword:
            query += " AND (title LIKE ? OR description LIKE ?)"
            kw = f"%{keyword}%"
            params.extend([kw, kw])

        # Kategori
        if category:
            query += " AND LOWER(TRIM(category)) = LOWER(TRIM(?))"
            params.append(category)

        # Maxpris
        if max_price not in (None, ""):
            try:
                query += " AND starting_bid <= ?"
                params.append(int(max_price))
            except ValueError:
                pass

        # Sluttid-filter
        if end_before:
            end_before = end_before.replace("T", " ")
            query += " AND end_datetime <= ?"
            params.append(end_before)

        query += " ORDER BY end_datetime ASC"
        return self.query_all(query, tuple(params))
