from flask import Flask
from pathlib import Path

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev"

    # --- DATABASE CONFIG ---
    # database.db hamnar i projektroten
    app.config["DATABASE"] = str(
        Path(app.root_path).parent / "database.db"
    )

    # koppla in db-hjälpfunktioner
    from app import db
    db.init_app(app)

    # --- BLUEPRINTS ---

    from app.blueprints.bids.routes import bid_bp
    app.register_blueprint(bid_bp, url_prefix='/bids')

    return app

