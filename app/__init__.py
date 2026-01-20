from flask import Flask
from pathlib import Path


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev"

    app.config["DATABASE"] = str(Path(app.root_path).parent / "database.db")

    from app import db
    db.init_app(app)

    # --- BLUEPRINTS ---
    from app.blueprints.public.routes import public_bp
    from app.blueprints.auction.routes import auction_bp
    from app.blueprints.bids.bid_bp import bid_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auction_bp)
    app.register_blueprint(bid_bp, url_prefix="/bids")

    return app


