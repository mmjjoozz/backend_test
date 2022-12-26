import pytest
from app.api import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


def test_make_new_order(client):
    resp = client.post("/orders", data={
        "product_id": "1",
        "order_price": "10",
    })
    assert resp.status_code == 201