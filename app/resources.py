import json

from flask import make_response, request
from flask_restful import Resource, abort
from marshmallow.exceptions import ValidationError
from sqlalchemy.sql import func

from app.db import db_session as db
from app.models import Orders, Products
from app.schemas import OrderSchema


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
            abort(404, message="Order not found.")

        resp_json = schema.dump(order)
        return make_response(resp_json, 200)

    def delete(self, order_id):
        pass

    def update(self, order_id):
        pass

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

        order_price = data["order_price"]

        if order_price >= product.list_price:
            discount_pc = 0
        else:
            discount_pc = (1 - (order_price / product.list_price)) * 100

        order = Orders(
            product_id=product.id,
            order_price=order_price,
            discount_pc=discount_pc,
        )
        db.add(order)
        db.commit()

        resp_json = schema.dump(order)
        return make_response(resp_json, 201)


class Metrics(Resource):
    def get(self):
        res = db.query(Products.name, func.avg(Orders.discount_pc)).join(Products).group_by(Products.name).all()
        return make_response(json.dumps(dict(res)), 200)
