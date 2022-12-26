from app.models import Orders, Products
from marshmallow import Schema
from marshmallow.fields import Nested

class ProductSchema(Schema):
    class Meta:
        model = Products
        fields = ("id", "name", "list_price")
    # id = auto_field()
    # name = auto_field()
    # list_price = auto_field()

class OrderSchema(Schema):
    class Meta:
        model = Orders
        fields = ("id", "order_price", "discount_pc", "date_created", "date_updated", "product")
    product = Nested(ProductSchema)

    # id = auto_field()
    # product_id = auto_field()
    # order_price = auto_field()
    # discount_pc = auto_field()
    # date_created = auto_field()
    # date_updated = auto_field()

