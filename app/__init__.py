import os
from flask import Flask

def create_app(test_config=None):
# Den här funktionen startar upp hela Flask-appen (alltså Application Factory).
    # Vi använder instance_relative_config för att databasen ska ligga i 
    # 'instance'-mappen, vilket är säkrare och håller ordning i projektet.
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        # En hemlig nyckel för att hålla sessioner säkra!
        SECRET_KEY='dev',
        # Sökvägen till SQLite-databasfilen.
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    # Ser till att 'instance'-mappen existerar
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initiera databasfunktioner med appen
    from . import db
    db.init_app(app)

    # Importerar och registrera blueprints
    from .blueprints.public.routes import public_bp
    from .blueprints.admin.routes import admin_bp
    from .blueprints.auth.routes import auth_bp
    from .blueprints.bids.bid_bp import bid_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(bid_bp)

    return app
