from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy.orm import relationship
from ..core.db import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    zipcode = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    productstotal = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)
    freight = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    paymentterm = Column(Integer, nullable=False)
    installments = Column(Integer, nullable=False)

    status = Column(
        Enum("pending", "completed", "canceled", name="order_status"),
        nullable=False,
        default="pending"
    )

    # Relationship with Product
    products = relationship("Product", back_populates="order")