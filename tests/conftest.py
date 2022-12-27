import pytest

from app.api import app, create_app, db
from app.config import TestConfig
from app.models import Orders, Products


def preload_data():
    objects = [
        Products(name="Catamaran", list_price=5000),
        Products(name="Dinghy", list_price=90),
        Orders(product_id=1, actual_price=2500),
        Orders(product_id=1, actual_price=1000),
        Orders(product_id=2, actual_price=40),
        Orders(product_id=2, actual_price=56),
        Orders(product_id=2, actual_price=120)
    ]
    db.session.bulk_save_objects(objects)
    db.session.commit()


@pytest.fixture()
def client():
    app = create_app(TestConfig)
    client = app.test_client()
    with app.app_context():
        db.create_all()
        preload_data()
    yield client


@pytest.fixture()
def empty_db_client():
    app = create_app(TestConfig)
    client = app.test_client()
    with app.app_context():
        db.create_all()
    yield client
