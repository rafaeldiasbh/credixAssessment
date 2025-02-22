from sqlalchemy.orm import Session
from ..models.order import Order
from ..models.product import Product
from ..schemas.order import CheckoutSchema

def create_order(db: Session, order: CheckoutSchema):
    # Insert a new Order
    db_order = Order(
        name=order.name,
        address=order.address,
        zipcode=order.zipcode,
        phone=order.phone,
        email=order.email,
        productsvalue=order.productsvalue,
        discount=order.discount,
        freight=order.freight,
        producttotal=order.producttotal,
        paymentterm=order.paymentterm,
        installments=order.installments,
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Insert the Products and associate them with the Order
    for product in order.products:
        db_product = Product(
            name=product.name,
            amount=product.amount,
            unitcost=product.unitcost,
            order_id=db_order.id,
        )
        db.add(db_product)

    db.commit()
    db.refresh(db_order)
    return db_order