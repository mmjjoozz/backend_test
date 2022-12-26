from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db import Base


class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    list_price = Column(Integer())
    __table_args__ = (UniqueConstraint("name", "list_price", name="_name_price_uc"),)


class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    actual_price = Column(Integer())
    product_id = Column(Integer(), ForeignKey("products.id"))
    product = relationship("Products")
