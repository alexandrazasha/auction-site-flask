from flask import Flask
from pathlib import Path


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev"

    app.config["DATABASE"] = str(Path(app.root_path).parent / "database.db")

    # Importera och initiera databasen
    from . import db
    db.init_app(app)
    
    # Importera och registrera blueprints
    from .blueprints.public.routes import public_bp
    from .blueprints.auth.routes import auth_bp # Din blueprint
    from .blueprints.admin.routes import admin_bp # Din blueprint
    from .blueprints.auction.routes import auction_bp # Från main
    from .blueprints.bids.bid_bp import bid_bp # Från main

    app.register_blueprint(public_bp)
    app.register_blueprint(auction_bp)
    app.register_blueprint(bid_bp, url_prefix="/bids")
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app
