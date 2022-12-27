from marshmallow import Schema, fields
from marshmallow.validate import Range

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
    product_id = fields.Int(strict=True, required=True, validate=[Range(min=1, error="Value must be greater than 0")])
    actual_price = fields.Int(strict=True, required=True)


class OrderUpdateSchema(Schema):
    """
    Only use for validating incoming PUT requests to check that no extraneous fields are provided and no
    nonsense gets inserted.
    """

    class Meta:
        model = Orders
        fields = ("product_id", "actual_price")

    product_id = fields.Int(strict=True, required=False, validate=[Range(min=1, error="Value must be greater than 0")])
    actual_price = fields.Int(strict=True, required=False)
