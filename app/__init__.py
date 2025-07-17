from flask import Flask
from .db import db
from .api import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    db.init_app(app)

    with app.app_context():
        app.register_blueprint(api_bp, url_prefix='/api')
        db.create_all()

    return app
