from flask import Blueprint, render_template, request, flash, redirect, url_for

# Importera repositories
from app.repositories.bid_repo import BidRepository
from app.repositories.vote_repo import VoteRepository
from app.repositories.auction_repo import AuctionRepository

bid_bp = Blueprint("bid_bp", __name__, url_prefix="/bids")

# SÖKFUNKTION
@bid_bp.route("/search")
def search():
    sokord = request.args.get("keyword")
    kategori = request.args.get("category")
    max_pris = request.args.get("max_price")
    end_before = request.args.get("end_before")

    bid_repo = BidRepository()
    resultat = bid_repo.search_auctions(
        keyword=sokord,
        category=kategori,
        max_price=max_pris,
        end_before=end_before
    )

    vote_repo = VoteRepository()

    auctions_with_votes = []
    for a in resultat:
        auctions_with_votes.append({
            "auction": a,
            "likes": vote_repo.count_likes(a["id"]),
            "dislikes": vote_repo.count_dislikes(a["id"]),
        })

    # Matcha våra kategorier
    categories = ["Accessoarer", "Sport"]

    return render_template(
        "index.html",
        auctions=auctions_with_votes,
        categories=categories
    )




# LÄGGA BUD 
@bid_bp.post("/place/<int:auction_id>")
def place_bid(auction_id: int):
    bidder_email = request.form.get("bidder_email")
    bid_repo = BidRepository()

    # Validera beloppet
    try:
        amount = int(request.form.get("amount"))
    except (ValueError, TypeError):
        flash("Ogiltigt belopp!", "error")
        return redirect(url_for("public.auction_detail", auction_id=auction_id))

    # Kontrollera om auktionen är stängd
    auction_repo = AuctionRepository()
    auction = auction_repo.get_by_id(auction_id)

    if not auction or auction["is_closed"]:
        flash("Denna auktion är avslutad och tar inte emot nya bud.", "error")
        return redirect(url_for("public.auction_detail", auction_id=auction_id))

    # Hämta nuvarande högsta bud
    current_top_bids = bid_repo.get_top_bids(auction_id, limit=1)

    if current_top_bids:
        highest_bid = current_top_bids[0]["amount"]
        if amount <= highest_bid:
            flash(
                f"Tyvärr, någon har redan bjudit {highest_bid} kr. Du måste bjuda högre!",
                "error"
            )
            return redirect(url_for("public.auction_detail", auction_id=auction_id))

    # Spara budet
    bid_repo.create_bid(auction_id, bidder_email, amount)
    flash("Tack! Ditt bud är registrerat.", "success")

    return redirect(url_for("public.auction_detail", auction_id=auction_id))
