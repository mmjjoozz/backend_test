import pytest

from app.api import create_app
from app.api import db
from app.models import Products

@pytest.fixture
def client():
    app = create_app()

    app.config["TESTING"] = True
    app.testing = True

    # This creates an in-memory sqlite db
    # See https://martin-thoma.com/sql-connection-strings/
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    client = app.test_client()
    with app.app_context():
        db.create_all()
        p = Products(id=1, name="Catamaran", list_price=5000)
        db.session.add(p)
        db.session.commit()
    yield client
