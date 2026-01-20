from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.repositories.bid_repo import BidRepository 

# Detta namn måste matcha det importerade i __init__.py
bid_bp = Blueprint('bid_bp', __name__)

@bid_bp.route('/place/<int:auction_id>', methods=['POST'])
def place_bid(auction_id):
    # 1. Hämta data från formuläret
    email = request.form.get('bidder_email')
    amount = float(request.form.get('amount'))

    # 2. Logik: Är budet högre än det nuvarande?
    highest_bid = BidRepository.get_highest_bid(auction_id)
    
    if highest_bid and amount <= highest_bid['amount']:
        flash("Budet måste vara högre än nuvarande högsta bud!", "error")
    else:
        # 3. Spara budet
        BidRepository.create_bid(auction_id, email, amount)
        flash("Budet är lagt!", "success")

    # 4. Skicka tillbaka användaren till auktionssidan
    return redirect(url_for('auction_bp.auction_detail', auction_id=auction_id))

