
from flask import make_response, request
from flask_restful import Resource, abort

from app.db import db_session as db
from app.models import Orders, Products
from app.schemas import OrderSchema


class Order(Resource):
    def get(self, order_id=None):
        if not order_id:
            args = request.args
            if args:
                product_name = args.get("product_name")
                orders = db.query(Orders).join(Products).filter(Products.name == product_name)
            else:
                orders = db.query(Orders).all()
            resp_json = OrderSchema(many=True).dump(orders)
            return make_response(resp_json, 200)
        pass

    def delete(self, order_id):
        pass

    def update(self, order_id):
        pass

    def post(self):
        data = request.get_json()
        product = db.query(Products).get((data["product_id"]))
        order_price = data["order_price"]
        discount_pc = (1 - (order_price / product.list_price)) * 100
        order = Orders(
            product_id=product.id,
            order_price=order_price,
            discount_pc=discount_pc,
        )
        db.add(order)
        db.commit()
        resp_json = OrderSchema().dump(order)
        return make_response(resp_json, 201)


class Metrics(Resource):
    def get(self):
        pass
