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
        products = db.session.query(Products).all()
        # Pre-populate DB with some info
        if not products:
            objects = [
                Products(name="Catamaran", list_price=1000),
                Products(name="Dinghy", list_price=150),
                Products(name="Narrowboat", list_price=500),
                Products(name="Submarine", list_price=2000)
            ]
            db.session.bulk_save_objects(objects)
            db.session.commit()

        return app


app = create_app()
