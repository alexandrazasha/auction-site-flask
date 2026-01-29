# Denna fil är ett "Repository" för auktioner.
# Innehåller alla funktioner för att hämta, skapa, uppdatera och ta bort
# auktioner från databasen.
from app.repositories.base_repo import BaseRepo


class AuctionRepository(BaseRepo):
    def get_all(self):
        """Hämtar alla auktioner från databasen, sorterade efter slutdatum."""
        sql = """
        SELECT *
        FROM auctions
        ORDER BY end_datetime ASC
        """
        return self.query_all(sql)

    def get_all_with_bid_count(self):
        """
        Hämtar alla auktioner från databasen och inkluderar antalet bud för varje auktion.
        """
        sql = """
        SELECT a.*, COUNT(b.id) as bid_count
        FROM auctions a
        LEFT JOIN bids b ON a.id = b.auction_id
        GROUP BY a.id
        ORDER BY a.end_datetime ASC
        """
        return self.query_all(sql)

    def get_by_id(self, auction_id: int):
        """Hämtar en specifik auktion baserat på dess ID."""
        sql = """
        SELECT *
        FROM auctions
        WHERE id = ?
        """
        return self.query_one(sql, (auction_id,))

    def get_top_two_bids(self, auction_id: int):
        """Hämtar de två högsta buden för en specifik auktion."""
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

    def delete(self, auction_id: int):
        """Tar bort en auktion från databasen."""
        # Denna SQL-fråga tar bort en rad från 'auctions'-tabellen.
        # Om databasen är inställd med "ON DELETE CASCADE" för bud och röster,
        # kommer de också att tas bort automatiskt.
        self.execute("DELETE FROM auctions WHERE id = ?", (auction_id,))

    def mark_as_closed(self, auction_id: int):
        """Markerar en auktion som avslutad (is_closed = 1)."""
        sql = "UPDATE auctions SET is_closed = 1 WHERE id = ?"
        self.execute(sql, (auction_id,))
