from flask import Flask
from flask_cors import CORS

from .main import blueprints

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    # chinese display
    app.config["JSON_AS_ASCII"] = False
    for blueprint in blueprints:
        app.register_blueprint(blueprint, url_prefix="/v1.0")
    return app
