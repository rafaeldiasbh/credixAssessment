from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..core.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    unitcost = Column(Float, nullable=False)

    # Foreign key to Order
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    # Relationship with Order
    order = relationship("Order", back_populates="products")