from flask import Flask
from .db import db
from .api import api_bp, math_operations_bp
from .web import web_bp


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    db.init_app(app)

    with app.app_context():
        app.register_blueprint(api_bp, url_prefix='/api')
        app.register_blueprint(math_operations_bp)
        app.register_blueprint(web_bp)
        db.create_all()

    return app
