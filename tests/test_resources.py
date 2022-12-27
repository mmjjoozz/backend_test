def test_make_new_order(client):
    resp = client.post(
        "/orders",
        json={
            "product_id": 1,
            "actual_price": 10,
        },
    )
    assert resp.status_code == 201
    assert resp.json == {
        "actual_price": 10,
        "id": 6,
        "product_id": 1,
        "product_info": {"name": "Catamaran", "list_price": 5000},
    }


def test_make_new_order_resp_422_if_field_missing(client):
    resp = client.post(
        "/orders",
        json={
            "actual_price": 10,
        },
    )
    assert resp.status_code == 422
    assert resp.json["message"] == "Validation error."


def test_make_new_order_resp_422_if_invalid_type(client):
    resp = client.post(
        "/orders",
        json={
            "actual_price": 10,
            "product_id": "string",
        },
    )
    assert resp.status_code == 422
    assert resp.json["message"] == "Validation error."


def test_get_all_orders(client):
    resp = client.get("/orders")
    assert resp.status_code == 200
    assert len(resp.json) == 5


def test_get_all_orders_filter_by_query_params(client):
    resp = client.get("/orders?product_name=Catamaran")
    assert resp.status_code == 200
    assert len(resp.json) == 2
    for elem in resp.json:
        assert elem["product_id"] == 1


def test_get_all_orders_returns_all_orders_if_query_params_wrong(client):
    resp = client.get("/orders?prodcut_nae=Catamaran")
    assert resp.status_code == 200
    assert len(resp.json) == 5


def test_get_all_orders_returns_no_orders_if_query_params_product_does_not_exist(client):
    resp = client.get("/orders?product_name=")
    assert resp.status_code == 200
    assert len(resp.json) == 0
    assert resp.json == []
    resp = client.get("/orders?product_name=Nonsense")
    assert resp.status_code == 200
    assert len(resp.json) == 0
    assert resp.json == []


def test_get_all_orders_no_db_records(empty_db_client):
    resp = empty_db_client.get("/orders")
    assert resp.status_code == 200
    assert len(resp.json) == 0
    assert resp.json == []


def test_get_order(client):
    resp = client.get("/orders/1")
    assert resp.status_code == 200
    assert resp.json == {
        "actual_price": 2500,
        "id": 1,
        "product_id": 1,
        "product_info": {"list_price": 5000, "name": "Catamaran"},
    }


def test_get_order_not_found(client):
    resp = client.get("/orders/6000")
    assert resp.status_code == 404
    assert resp.json["message"] == "Order ID not found."


def test_delete_success(client):
    resp = client.delete("orders/1")
    assert resp.status_code == 204


def test_delete_nonexistent_order(client):
    resp = client.delete("orders/6000")
    assert resp.status_code == 404
    assert resp.json["message"] == "Order ID not found."


def test_delete_404_on_empty_db(empty_db_client):
    resp = empty_db_client.delete("orders/1")
    assert resp.status_code == 404
    assert resp.json["message"] == "Order ID not found."


def test_put_success(client):
    resp = client.put(
        "orders/1",
        json={
            "product_id": 2,
        },
    )
    assert resp.status_code == 200
    assert resp.json == {
        "actual_price": 2500,
        "id": 1,
        "product_id": 2,
        "product_info": {"name": "Dinghy", "list_price": 90},
    }


def test_put_404_if_nonexistent_order(client):
    resp = client.put("orders/6000", json={"product_id": 2, "actual_price": 40})
    assert resp.status_code == 404
    assert resp.json["message"] == "Order ID not found."


def test_put_404_on_empty_db(empty_db_client):
    resp = empty_db_client.put("orders/1", json={"product_id": 2, "actual_price": 40})
    assert resp.status_code == 404
    assert resp.json["message"] == "Order ID not found."


def test_put_422_nonsense_field_content(client):
    resp = client.put("orders/1", json={"actual_price": "string"})
    assert resp.status_code == 422
    assert resp.json["message"] == "Validation error."


def test_get_metrics(client):
    resp = client.get("orders/metrics")
    assert resp.status_code == 200
    assert resp.json == {"Catamaran": 65.0, "Dinghy": 20.0}


def test_get_metrics_empty_db_client(empty_db_client):
    resp = empty_db_client.get("orders/metrics")
    assert resp.status_code == 200
    assert resp.json == {}
