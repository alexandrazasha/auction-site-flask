from flask import Flask
from pathlib import Path

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev"

    # --- DATABASE CONFIG ---
    app.config["DATABASE"] = str(
        Path(app.root_path).parent / "database.db"
    )

    from app import db
    db.init_app(app)

    # --- BLUEPRINTS ---
    # Vi ändrar importen så den pekar på din fil bid_bp.py i mappen bids
    from app.blueprints.bids.bid_bp import bid_bp
    # Vi registrerar den. Nu nås dina funktioner via /bids/
    app.register_blueprint(bid_bp, url_prefix='/bids')

    return app

