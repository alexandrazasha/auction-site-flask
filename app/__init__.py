from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev"

    # importera blueprint
    from app.blueprints.public.routes import public_bp

    # registrera blueprint
    app.register_blueprint(public_bp)

    return app
