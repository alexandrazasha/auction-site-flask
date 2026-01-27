from flask import Blueprint, render_template
from app.repositories.auction_repo import AuctionRepository
from app.repositories.bid_repo import BidRepository
from app.repositories.vote_repo import VoteRepository

public_bp = Blueprint('public', __name__)

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

    return render_template('index.html', auctions=auctions_with_votes)

@public_bp.route('/auction/<int:auction_id>')
def auction_detail(auction_id):
    """Visar detaljsidan för en specifik auktion."""
    auction_repo = AuctionRepository()
    bid_repo = BidRepository()
    auction = auction_repo.get_by_id(auction_id)
    top_bids = bid_repo.get_top_bids(auction_id, limit=2)

    return render_template('detail.html', auction=auction, bids=top_bids)