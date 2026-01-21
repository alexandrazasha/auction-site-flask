from app.repositories.base_repo import BaseRepo


class AuctionRepository(BaseRepo):
    def get_all(self):
        sql = """
        SELECT *
        FROM auctions
        ORDER BY end_datetime ASC
        """
        return self.query_all(sql)

    def get_by_id(self, auction_id: int):
        sql = """
        SELECT *
        FROM auctions
        WHERE id = ?
        """
        return self.query_one(sql, (auction_id,))

    def get_top_two_bids(self, auction_id: int):
        sql = """
        SELECT bidder_email, amount, created_at
        FROM bids
        WHERE auction_id = ?
        ORDER BY amount DESC, created_at DESC
        LIMIT 2
        """
        return self.query_all(sql, (auction_id,))

    def create(self, title, description, category, starting_bid, end_datetime):
        """Skapar en ny auktion och sparar den i databasen."""
        sql = """
            INSERT INTO auctions (title, description, category, starting_bid, end_datetime)
            VALUES (?, ?, ?, ?, ?)
        """
        return self.execute(sql, (title, description, category, starting_bid, end_datetime))

    def update(self, auction_id, title, description, category, starting_bid, end_datetime):
        """Uppdaterar en befintlig auktion i databasen."""
        sql = """
            UPDATE auctions
            SET title = ?, description = ?, category = ?, starting_bid = ?, end_datetime = ?
            WHERE id = ?
        """
        self.execute(sql, (title, description, category, starting_bid, end_datetime, auction_id))
