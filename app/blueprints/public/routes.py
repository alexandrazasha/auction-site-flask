from flask import Blueprint, render_template
from app.repositories.auction_repo import AuctionRepository

public_bp = Blueprint("public", __name__)

@public_bp.route("/")
def index():
    """Visar en lista över alla auktioner på startsidan."""
    auction_repo = AuctionRepository()
    all_auctions = auction_repo.get_all() # Använder den befintliga get_all()
    return render_template("index.html", auctions=all_auctions)
