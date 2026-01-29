# Denna fil är ett "Repository" för användare.
# Den innehåller funktioner för att hämta och hantera användardata från databasen. /Karolina
from .base_repo import BaseRepo
class UserRepo(BaseRepo):
    def get_by_email(self, email: str):
        # Hämtar en användare baserat på e-post.
        # SQL-fråga för att hämta en rad från 'users'-tabellen där e-posten matchar.
        sql = "SELECT * FROM users WHERE email = ?;"
        return self.query_one(sql, (email,))