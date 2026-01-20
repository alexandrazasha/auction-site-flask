from flask import Blueprint, render_template, request, flash, redirect, url_for

# Importera din BidRepository från rätt ställe 
from app.repositories.bid_repo import BidRepository


# Skapar en blueprint för att gruppera budgivnings- och sökfunktionalitet [cite: 56]
bid_bp = Blueprint('bid_bp', __name__)

# --- RUTT 1: SÖKFUNKTIONN ---
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

# --- RUTT 2: VISAR DE TVÅ SENASTE BUDEN ---
@bid_bp.route('/auction/<int:auction_id>')
def auction_detail(auction_id):
    # Här hämtar vi de 2 högsta buden för just denna auktion
    topp_bud = BidRepository.get_top_bids(auction_id)
    
    # Vi skickar med 'bids' till detail.html
    return render_template('detail.html', bids=topp_bud, auction_id=auction_id)


# --- RUTT 3: KAN LÄGGA BUD och kollar så det är högre än senaste bud --- 
@bid_bp.route('/place_bid/<int:auction_id>', methods=['POST'])
def place_bid():
    # 1. Hämta data från formuläret
    auction_id = request.form.get('auction_id')
    bidder_email = request.form.get('bidder_email')
    try:
        amount = float(request.form.get('amount'))
    except (ValueError, TypeError):
        flash("Ogiltigt belopp!")
        return redirect(url_for('bid_bp.auction_detail', auction_id=auction_id))

    # 2. Hämta det nuvarande högsta budet för att validera
    current_top_bids = BidRepository.get_top_bids(auction_id, limit=1)
    
    # 3. Validera så det är ett högre bud
    if current_top_bids:
        highest_bid = current_top_bids[0]['amount']
        if amount <= highest_bid:
            flash(f"Ditt bud måste vara högre än nuvarande bud ({highest_bid} kr)!")
            return redirect(url_for('bid_bp.auction_detail', auction_id=auction_id))

    # 4. Om ok -> Spara i databasen
    BidRepository.create_bid(auction_id, bidder_email, amount)
    flash("Ditt bud har registrerats!")
    
    # Skicka användaren tillbaka till auktionssidan så de ser sitt bud i historiken
    return redirect(url_for('bid_bp.auction_detail', auction_id=auction_id))