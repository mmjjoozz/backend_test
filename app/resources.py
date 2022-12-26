import json

from flask import make_response, request, Response
from flask_restful import Resource, abort
from marshmallow.exceptions import ValidationError
from sqlalchemy.sql import func

from app.db import db_session as db
from app.models import Orders, Products
from app.schemas import OrderSchema, OrderUpdateSchema


class Order(Resource):
    def get(self, order_id=None):
        if not order_id:
            args = request.args
            if args and "product_name" in args:
                product_name = args.get("product_name")
                orders = db.query(Orders).join(Products).filter(Products.name == product_name)
            else:
                orders = db.query(Orders).all()

            resp_json = OrderSchema(many=True).dump(orders)
            return make_response(resp_json, 200)

        schema = OrderSchema()
        order = db.query(Orders).get(order_id)
        if not order:
            abort(404, message="Order ID not found.")

        resp_json = schema.dump(order)
        return make_response(resp_json, 200)

    def delete(self, order_id):
        order = db.query(Orders).get(order_id)
        if not order:
            abort(404, message="Product ID not found.")

        db.delete(order)
        db.commit()
        return make_response("Success.", 200)

    def put(self, order_id):
        order = db.query(Orders).get(order_id)
        if not order:
            abort(404, message="Order ID not found.")

        data = request.get_json()
        schema = OrderUpdateSchema()
        try:
            schema.load(data)
        except ValidationError as e:
            abort(422, message=e)

        if data.get("product_id"):
            if not db.query(Products).get(data["product_id"]):
                abort(404, message="Product ID not found.")

            order.product_id = data["product_id"]
        if data.get("actual_price"):
            order.actual_price = data["actual_price"]

        db.commit()

        resp_json = OrderSchema().dump(order)
        return make_response(resp_json, 200)

    def post(self):
        data = request.get_json()
        schema = OrderSchema()
        try:
            schema.load(data)
        except ValidationError as e:
            abort(422, message=e)

        product = db.query(Products).get((data["product_id"]))
        if not product:
            abort(404, message="Product ID not found.")

        actual_price = data["actual_price"]

        order = Orders(
            product_id=product.id,
            actual_price=actual_price,
        )
        db.add(order)
        db.commit()

        resp_json = schema.dump(order)
        return make_response(resp_json, 201)


class Metrics(Resource):
    """
    I am not limiting the amount of times a single boat can be bought - in a real life scenario we'd probably
    have multiple boats in stock and that's an assumption I'm basing my API on.
    Since price can be decided on negotiations, I'm assuming that a single boat can have different discounts
    depending on the order. This endpoint will return the average of all discounts per boat.
    Bear in mind that if a boat is MORE expensive (e.g. there's a shortage or a bidding war) the discount will simply
    be 0 - I'm assuming we're not interested in including price increases for this metric.
    Averages are rounded to two decimals places
    """

    def get(self):
        metrics = {}
        qs = db.query(Orders).join(Products)
        for q in qs:
            product = q.product
            discount_pct = (1 - (q.actual_price / product.list_price)) * 100
            if product.name not in metrics.keys():
                metrics[product.name] = [discount_pct]
            else:
                metrics[product.name].append(discount_pct)

        metrics_avg = {
            k: 0 if sum(v) / len(v) <= 0 else round((sum(v) / len(v)), 2) for k, v in metrics.items() if sum(v) != 0
        }
        return make_response(json.dumps(dict(metrics_avg)), 200)
