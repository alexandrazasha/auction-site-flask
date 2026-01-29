#Denna fil hanterar "framsidan" av appen. Hämtar auktionerna, räknar likes/dislikes
from flask import Blueprint, render_template, redirect, url_for
from app.repositories.auction_repo import AuctionRepository
from app.repositories.bid_repo import BidRepository
from app.repositories.vote_repo import VoteRepository

public_bp = Blueprint('public', __name__)

categories = ['Accessoarer', 'Elektronik', 'Konst', 'Sport'] # Definiera kategorilistan på modulnivå

@public_bp.route('/')
def index():
    """Visar startsidan med en lista över alla auktioner."""
    auction_repo = AuctionRepository()
    vote_repo = VoteRepository()

    auctions_from_db = auction_repo.get_all()
    auctions_with_votes = []
    for a in auctions_from_db:
        auctions_with_votes.append({
            "auction": a,
            "likes": vote_repo.count_likes(a["id"]),
            "dislikes": vote_repo.count_dislikes(a["id"]),
        })

    return render_template('index.html', auctions=auctions_with_votes, categories=categories)

@public_bp.route('/auction/<int:auction_id>')
def auction_detail(auction_id):
    """Visar detaljsidan för en specifik auktion."""
    auction_repo = AuctionRepository()
    bid_repo = BidRepository()
    vote_repo = VoteRepository()

    auction = auction_repo.get_by_id(auction_id)
    all_bids = bid_repo.get_all_bids_for_auction(auction_id)
    
    # Hämta likes och dislikes för auktionen
    likes = vote_repo.count_likes(auction_id)
    dislikes = vote_repo.count_dislikes(auction_id)

    return render_template('auction_detail.html', auction=auction, bids=all_bids, likes=likes, dislikes=dislikes)


@public_bp.post("/auction/<int:auction_id>/like")
def like_auction(auction_id: int):
    """Hanterar att LIKEA en auktion."""
    vote_repo = VoteRepository()
    vote_repo.add_like(auction_id)
    # Tillbaka till detaljsidan
    return redirect(url_for("public.auction_detail", auction_id=auction_id))


@public_bp.post("/auction/<int:auction_id>/dislike")
def dislike_auction(auction_id: int):
    """Hanterar att DISLIKEA en auktion."""
    vote_repo = VoteRepository()
    vote_repo.add_dislike(auction_id)
    # Tillbaka till detaljsidan
    return redirect(url_for("public.auction_detail", auction_id=auction_id))