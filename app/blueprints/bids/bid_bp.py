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

    resultat = BidRepository.search_auctions(keyword=sokord, category=kategori, max_price=max_pris)

    # Bygg samma struktur som index.html förväntar sig (auction + likes/dislikes)
    from app.repositories.vote_repo import VoteRepository
    vote_repo = VoteRepository()

    auctions_with_votes = []
    for a in resultat:
        auctions_with_votes.append({
            "auction": a,
            "likes": vote_repo.count_likes(a["id"]),
            "dislikes": vote_repo.count_dislikes(a["id"]),
        })

    return render_template("index.html", auctions=auctions_with_votes)


# --- RUTT 2: VISAR DE TVÅ SENASTE BUDEN ---
@bid_bp.route('/auction/<int:auction_id>')
def auction_detail(auction_id):
    # Här hämtar vi de 2 högsta buden för just denna auktion
    topp_bud = BidRepository.get_top_bids(auction_id)
    
    # Vi skickar med 'bids' till detail.html
    return render_template('detail.html', bids=topp_bud, auction_id=auction_id)


# --- RUTT 3: LÄGGER BUD och kollar så det är högre än senaste bud ---
@bid_bp.post("/place/<int:auction_id>")
def place_bid(auction_id: int):
    bidder_email = request.form.get("bidder_email")

    try:
        amount = int(request.form.get("amount"))
    except (ValueError, TypeError):
        flash("Ogiltigt belopp!")
        return redirect(url_for("auction_bp.auction_detail", auction_id=auction_id))

    # Hämta nuvarande högsta bud för validering
    current_top_bids = BidRepository.get_top_bids(auction_id, limit=1)

    if current_top_bids:
        highest_bid = current_top_bids[0]["amount"]
        if amount <= highest_bid:
            flash(f"Ditt bud måste vara högre än nuvarande bud ({highest_bid} kr)!")
            return redirect(url_for("auction_bp.auction_detail", auction_id=auction_id))

    # Spara bud
    BidRepository.create_bid(auction_id, bidder_email, amount)
    flash("Ditt bud har registrerats!")

    # Tillbaka till din auktion-detaljsida
    return redirect(url_for("auction_bp.auction_detail", auction_id=auction_id))
