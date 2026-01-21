from flask import Blueprint, render_template, redirect
from app.repositories.auction_repo import AuctionRepository
from app.repositories.vote_repo import VoteRepository

auction_bp = Blueprint("auction_bp", __name__)

@auction_bp.get("/health-auctions")
def health_auctions():
    return "auction_bp OK"


@auction_bp.get("/auctions")
def auctions_index():
    auction_repo = AuctionRepository()
    vote_repo = VoteRepository()

    auctions = auction_repo.get_all()

    auctions_with_votes = []
    for a in auctions:
        auctions_with_votes.append({
            "auction": a,
            "likes": vote_repo.count_likes(a["id"]),
            "dislikes": vote_repo.count_dislikes(a["id"]),
        })

    return render_template("index.html", auctions=auctions_with_votes)


@auction_bp.get("/auction/<int:auction_id>")
def auction_detail(auction_id: int):
    auction_repo = AuctionRepository()
    vote_repo = VoteRepository()

    auction = auction_repo.get_by_id(auction_id)
    likes = vote_repo.count_likes(auction_id)
    dislikes = vote_repo.count_dislikes(auction_id)

    top_bids = auction_repo.get_top_two_bids(auction_id)

    return render_template(
        "auction_detail.html",
        auction=auction,
        likes=likes,
        dislikes=dislikes,
        top_bids=top_bids
    )



@auction_bp.post("/auction/<int:auction_id>/like")
def like_auction(auction_id: int):
    vote_repo = VoteRepository()
    vote_repo.add_like(auction_id)
    # tillbaka till detaljsidan
    return redirect(f"/auction/{auction_id}")


@auction_bp.post("/auction/<int:auction_id>/dislike")
def dislike_auction(auction_id: int):
    vote_repo = VoteRepository()
    vote_repo.add_dislike(auction_id)
    return redirect(f"/auction/{auction_id}")

