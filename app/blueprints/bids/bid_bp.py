from flask import Blueprint, render_template, request
# Importera din BidRepository från rätt ställe 
from app.repositories.bid_repo import BidRepository

# Skapar en blueprint för att gruppera budgivnings- och sökfunktionalitet [cite: 56]
bid_bp = Blueprint('bid_bp', __name__)

@bid_bp.route('/search')
def search():
    # Hämtar söksträng från URL-parametern 'keyword' [cite: 49]
    sokord = request.args.get('keyword')
    
    # Hämtar vald kategori från formulärets rullista [cite: 51]
    kategori = request.args.get('category')
    
    # Hämtar angivet maxpris för filtrering av sökresultat [cite: 52]
    max_pris = request.args.get('max_price')

    # Anropar metoden direkt på klassnamnet eftersom den är en staticmethod [cite: 57, 64]
    # Här skickar vi med sökord, kategori och maxpris som parametrar [cite: 61, 64]
    resultat = BidRepository.search_auctions(keyword=sokord, category=kategori, max_price=max_pris)

    # Returnerar HTML-mallen med listan på de auktioner som matchar filtren [cite: 35]
    return render_template('index.html', auctions=resultat)