from app.db import get_db
from app.repositories.base_repo import BaseRepo


class VoteRepository(BaseRepo):
    def count_likes(self, auction_id: int) -> int:
        sql = """
        SELECT COUNT(*) AS cnt
        FROM votes
        WHERE auction_id = ? AND value = 1
        """
        row = self.query_one(sql, (auction_id,))
        return row["cnt"] if row else 0
    def count_dislikes(self, auction_id: int) -> int:
        sql = """
        SELECT COUNT(*) AS cnt
        FROM votes
        WHERE auction_id = ? AND value = -1
        """
        row = self.query_one(sql, (auction_id,))
        return row["cnt"] if row else 0
    def add_like(self, auction_id: int) -> None:
        sql = """
        INSERT INTO votes (auction_id, value)
        VALUES (?, 1)
        """
        self.execute(sql, (auction_id,))
    def add_dislike(self, auction_id: int) -> None:
        sql = """
        INSERT INTO votes (auction_id, value)
        VALUES (?, -1)
        """
        self.execute(sql, (auction_id,))
