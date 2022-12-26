from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey, Float, DateTime
from app.db import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    list_price = Column(Integer())
    __table_args__ = (UniqueConstraint('name', 'list_price', name='_name_price_uc'),)

class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    order_price = Column(Integer())
    discount_pc = Column(Float())
    product_id = Column(Integer(), ForeignKey("products.id"))
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())
    product = relationship("Products")
