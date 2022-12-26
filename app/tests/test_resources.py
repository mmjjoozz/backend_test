import pytest

from app.api import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


def test_make_new_order(client):
    resp = client.post(
        "/orders",
        json={
            "product_id": 1,
            "order_price": 10,
        },
    )
    assert "product" in resp.json
    assert resp.json["product"]["id"] == 1
    assert resp.status_code == 201


def test_get_all_orders(client):
    resp = client.get("/orders")
    assert resp.ststus_code == 200
    assert len(resp.json) == 10
