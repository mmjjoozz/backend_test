def test_make_new_order(client):
    resp = client.post(
        "/orders",
        json={
            "product_id": 1,
            "actual_price": 10,
        },
    )
    assert resp.status_code == 201


# def test_get_all_orders(client):
#     resp = client.get("/orders")
#     assert resp.ststus_code == 200
#     assert len(resp.json) == 10
