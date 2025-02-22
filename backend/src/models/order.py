from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..core.db import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    zipcode = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    productsvalue = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)
    freight = Column(Float, nullable=False)
    producttotal = Column(Float, nullable=False)
    paymentterm = Column(Integer, nullable=False)
    installments = Column(Integer, nullable=False)

    # Relationship with Product
    products = relationship("Product", back_populates="order")