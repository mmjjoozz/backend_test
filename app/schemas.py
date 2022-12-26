from marshmallow import Schema, fields

from app.models import Orders, Products


class ProductSchema(Schema):
    class Meta:
        model = Products
        fields = ("name", "list_price")


class OrderSchema(Schema):
    class Meta:
        model = Orders
        fields = ("id", "actual_price", "product_id", "product")

    product = fields.Nested(ProductSchema, data_key="product_info")
    product_id = fields.Int(required=True)
    actual_price = fields.Int(required=True)


class OrderUpdateSchema(Schema):
    """
    Only use for validating incoming PUT requests to check that no extraneous fields are provided and no
    nonsense (strings etc) gets inserted.
    """

    class Meta:
        model = Orders

    product_id = fields.Int(required=False)
    actual_price = fields.Int(required=False)
