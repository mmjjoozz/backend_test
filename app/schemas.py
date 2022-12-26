from marshmallow import Schema, fields

from app.models import Orders, Products


class ProductSchema(Schema):
    class Meta:
        model = Products
        fields = ("id", "name", "list_price")


class OrderSchema(Schema):
    class Meta:
        model = Orders
        fields = ("id", "order_price", "product_id", "discount_pc", "date_created", "date_updated", "product")

    product = fields.Nested(ProductSchema)
    product_id = fields.Int(required=True)
    order_price = fields.Int(required=True)
