from flask import Blueprint

public_bp = Blueprint("public", __name__)

@public_bp.route("/")
def index():
    return "Auction site is running!"
