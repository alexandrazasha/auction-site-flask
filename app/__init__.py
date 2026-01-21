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

    # Importera och initiera databasen
    from . import db
    db.init_app(app)
    
    # Importera och registrera blueprints
    from .blueprints.public.routes import public_bp
    from .blueprints.auth.routes import auth_bp
    from .blueprints.admin.routes import admin_bp
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app
