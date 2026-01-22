from .base_repo import BaseRepo

class UserRepo(BaseRepo):
    def get_by_email(self, email: str):
        """Hämtar en användare baserat på e-post."""
        sql = "SELECT * FROM users WHERE email = ?;"
        return self.query_one(sql, (email,))