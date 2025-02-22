from sqlalchemy.orm import Session
from ..models.order import Order
from ..models.product import Product
from ..schemas.order import CheckoutSchema, CheckoutCreateSchema
import httpx

def create_order(db: Session, order: CheckoutCreateSchema) -> CheckoutSchema:
    # Convert the Pydantic model to a dictionary
    order_data = order.model_dump()

    # Separate the products from the order data
    products = order_data.pop("products")

    # Create the Order object using the remaining data
    db_order = Order(**order_data)

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Insert the Products and associate them with the Order
    for product in products:
        product["order_id"] = db_order.id  
        db_product = Product(**product)
        db.add(db_product)

    db.commit()
    db.refresh(db_order)
    return db_order