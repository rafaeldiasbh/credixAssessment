from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy.orm import relationship
from ..core.db import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    uuid = Column(String, nullable=False, unique=True)
    credixid = Column(String, nullable=True, unique=True)
    name = Column(String, nullable=False)
    taxid = Column(String, nullable=False)
    address = Column(String, nullable=False)
    address2 = Column(String, nullable=True)
    postalcode = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    productstotal = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)
    freight = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    paymentterm = Column(Integer, nullable=False)
    installments = Column(Integer, nullable=False)
    fee = Column(Float, nullable=False, default=0)

    status = Column(
        Enum("new", "created", "accepted", "cancelled," "rejected", "finalized", "captured", "expired", "ineligible", "invalidated", name="order_status"),
        nullable=False,
        default="new"
    )

    # Relationship with Product
    products = relationship("Product", back_populates="order")