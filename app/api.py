from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from app.config import DevConfig


def create_app(config=DevConfig):
    from app.models import Orders, Products
    from app.urls import api

    app = Flask(__name__)
    app.config.from_object(config)
    api.init_app(app)

    with app.app_context():
        db.init_app(app)
        db.create_all()

        return app


app = create_app()
