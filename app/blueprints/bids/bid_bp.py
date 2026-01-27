from flask import Blueprint, render_template, request, flash, redirect, url_for

# Importera dina repositories
from app.repositories.bid_repo import BidRepository
from app.repositories.vote_repo import VoteRepository
from app.repositories.auction_repo import AuctionRepository

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

    bid_repo = BidRepository()
    resultat = bid_repo.search_auctions(keyword=sokord, category=kategori, max_price=max_pris)

    # Bygg samma struktur som index.html förväntar sig (auction + likes/dislikes)
    vote_repo = VoteRepository()

    auctions_with_votes = []
    for a in resultat:
        auctions_with_votes.append({
            "auction": a,
            "likes": vote_repo.count_likes(a["id"]),
            "dislikes": vote_repo.count_dislikes(a["id"]),
        })

    return render_template("index.html", auctions=auctions_with_votes)

# --- RUTT 2: LÄGGER BUD och kollar så det är högre än senaste bud ---
@bid_bp.post("/place/<int:auction_id>")
def place_bid(auction_id: int):
    bidder_email = request.form.get("bidder_email")
    bid_repo = BidRepository()

    try:
        amount = int(request.form.get("amount"))
    except (ValueError, TypeError):
        flash("Ogiltigt belopp!")
        return redirect(url_for("public.auction_detail", auction_id=auction_id))
    
    # Hämta auktionen för att kolla om den är stängd
    auction_repo = AuctionRepository()
    auction = auction_repo.get_by_id(auction_id)
    if not auction or auction['is_closed']:
        flash("Denna auktion är avslutad och tar inte emot nya bud.", "error")
        return redirect(url_for("public.auction_detail", auction_id=auction_id))


    # Hämta nuvarande högsta bud för validering
    current_top_bids = bid_repo.get_top_bids(auction_id, limit=1)

    if current_top_bids:
        highest_bid = current_top_bids[0]["amount"]
        if amount <= highest_bid:
            flash(f"Ditt bud måste vara högre än nuvarande bud ({highest_bid} kr)!")
            return redirect(url_for("public.auction_detail", auction_id=auction_id))

    # Spara bud
    bid_repo.create_bid(auction_id, bidder_email, amount)
    flash("Ditt bud har registrerats!")

    # Tillbaka till din auktion-detaljsida
    return redirect(url_for("public.auction_detail", auction_id=auction_id))
