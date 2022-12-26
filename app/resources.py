import json
import requests
from flask import make_response, request
from flask_restful import Resource, abort
from app.schemas import OrderSchema, ProductSchema
from app.models import Products, Orders
from app.db import db_session as db

class Order(Resource):
    def get(self, order_id=None):
        if not order_id:
            schema = OrderSchema(many=True)
            orders = db.query(Orders).all()
            return make_response(schema.dump(orders), 200)
        pass

    def delete(self, order_id):
        pass

    def update(self, order_id):
        pass

    def post(self):
        data = request.get_json()
        product = db.query(Products).get((data["product_id"]))
        order_price = data["order_price"]
        discount_pc = (1-(order_price/product.list_price))*100
        order = Orders(
            product_id=product.id,
            order_price=order_price,
            discount_pc=discount_pc,
        )
        db.add(order)
        db.commit()
        order_schema = OrderSchema()
        return make_response(order_schema.dump(order), 201)

class Metrics(Resource):
    def get(self):
        pass