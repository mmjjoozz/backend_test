from app.api import db


class Products(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    list_price = db.Column(db.Integer())
    __table_args__ = (db.UniqueConstraint("name", "list_price", name="_name_price_uc"),)


class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    actual_price = db.Column(db.Integer())
    product_id = db.Column(db.Integer(), db.ForeignKey("products.id"))
    product = db.relationship("Products")
