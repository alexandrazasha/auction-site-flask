import os
from flask import Flask

def create_app(test_config=None):
    """
    Skapar och konfigurerar en instans av Flask-appen (Application Factory).

    `instance_relative_config=True` talar om för appen att konfigurationsfiler
    och databasen är relativa till 'instance'-mappen. Detta är en bra praxis
    för att hålla hemligheter och konfiguration separerade från koden.

    :param test_config: En valfri konfiguration att använda för tester.
    :return: En konfigurerad Flask-appinstans.
    """
    app = Flask(__name__, instance_relative_config=True)

    # Grundläggande konfiguration
    app.config.from_mapping(
        # En hemlig nyckel behövs för att hålla sessioner säkra.
        SECRET_KEY='dev',
        # Sökvägen till SQLite-databasfilen.
        # app.instance_path pekar nu korrekt till 'instance'-mappen.
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    # Se till att 'instance'-mappen existerar. Flask skapar den inte automatiskt.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        # Mappen finns redan, vilket är förväntat.
        pass

    # Initiera databasfunktioner med appen
    from . import db
    db.init_app(app)

    # Importera och registrera dina blueprints
    # (Vi antar att ni har dessa tre blueprints baserat på er projektstruktur)
    from .blueprints.public.routes import public_bp
    from .blueprints.admin.routes import admin_bp
    from .blueprints.auth.routes import auth_bp
    from .blueprints.bids.bid_bp import bid_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(bid_bp)

    return app
