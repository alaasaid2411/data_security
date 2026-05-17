from flask import Flask

from src.routes import register_routes


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="styles",
        static_url_path="/static",
    )
    app.secret_key = "data_security_secret_key"

    register_routes(app)

    return app
