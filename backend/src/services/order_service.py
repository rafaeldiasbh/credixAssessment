from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.order import Order
from ..models.product import Product
from ..schemas.order import CheckoutSchema, CheckoutCreateSchema, ProductSchema
from datetime import datetime, timedelta, timezone
from typing import List
from uuid import UUID
from http import HTTPStatus
import httpx
import json

async def get_all_orders(db: Session) -> List[CheckoutSchema]:
    # Fetch all orders
    orders = db.query(Order).all()
    
    if not orders:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="No orders found"
        )
    
    return orders

async def get_order_by_id(db: Session, order_id: int) -> CheckoutSchema:
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    
    return order

async def delete_order_by_id(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    
    # Delete associated products first
    db.query(Product).filter(Product.order_id == order_id).delete()
    
    db.delete(order)
    db.commit()

async def create_order(db: Session, uuid: UUID, order: CheckoutCreateSchema) -> CheckoutSchema:
    # Check if the idempotency key already exists
    duplicated = db.query(Order).filter(Order.uuid == str(uuid)).first()
    if duplicated:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Duplicate request detected (UUID already exists)"
        )

    # Convert the Pydantic model to a dictionary
    order_data = order.model_dump()
    order_data['uuid'] = str(uuid)

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

    order_data['products'] = products

    credix_response = await call_credix_create_order(order_data)
    
    db_order.credixid = credix_response['id']
    db_order.fee = credix_response['buyerFeesCents']/100 #transform back to float
    db_order.status = credix_response['status']

    db.commit()
    db.refresh(db_order)

    return db_order

async def call_credix_create_order(order: CheckoutCreateSchema):
    #url = "https://api.credix.finance/v1/orders"
    url = "https://api.pre.credix.finance/v1/orders"

    estimated_deliver_date = datetime.now(timezone.utc) + timedelta(days=3)
    estimated_deliver_date = estimated_deliver_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    first_name, last_name = split_name(order['name'])
    products = create_items_list(order['products'])
    order['tax'] = int(round(order['total'] * 0.17, 2)*100) #simulates averange ICMS tax value and convert it to cents
    installments = create_installments(order)
    

    payload = {
        "externalId": order['uuid'],
        "subtotalAmountCents": order['total']*100, #transform to cents
        "buyerTaxId": order['taxid'], 
        "sellerTaxId": "37154724000108", # fixed value since we are the seller
        "taxAmountCents": order['tax'], 
        "shippingCostCents": int(order['freight']*100), #convert to cents
        "shippingLocation": {
            "address1": order['address'],
            "address2": order['address2'],
            "city": "São Paulo", # fixed value
            "region": "São Paulo", # fixed value
            "postalCode": order['postalcode'],
            "country": "Brazil" # fixed value
        },
        "estimatedDeliveryDateUTC": estimated_deliver_date,
        "installments": installments,
        "contactInformation": {
            "email": order['email'],
            "phone": "+"+order['phone'],
            "name": first_name,
            "lastName": last_name
        },
        "items": products
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-CREDIPAY-API-KEY": "OTAyNjUyNmUtMGNmZi00NjdmLTg2YzYtY2YxNDc5MjhlMTIyOml3V093ME52V2dUdVp6eUd5SWdqKysybXFGNHFRUXZCUWZOcnRIZnVtZHM9"
    }

    async with httpx.AsyncClient(timeout = httpx.Timeout(30.0)) as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_detail = e.response.json() 
            raise HTTPException(
                status_code=e.response.status_code,
                detail=error_detail 
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Request failed: {e}")

def create_items_list(products: List[ProductSchema]) -> List[dict]:
    credix_products = []
    for product in products:
        credix_product = {
            "productId": "7891910000197",  # Fixed value for now
            "productName": product['name'],
            "quantity": int(product['amount']),  # Ensure ints int
            "unitPriceCents": int(product['unitcost'] * 100)  # Convert to cents
        }
        credix_products.append(credix_product)
    return credix_products

def split_name(full_name: str) -> tuple[str, str]:
    name_parts = full_name.split()
    if len(name_parts) > 1:
        first_name = " ".join(name_parts[:-1])  # Everything except the last word
        last_name = name_parts[-1]  # Last word
    else:
        first_name = full_name  # The entire name
        last_name = ""  # No last name
    return first_name, last_name

def create_installments(order:CheckoutCreateSchema) -> List[dict]:
    # Extract relevant fields from the order
    paymentterm_days = int(order['paymentterm'])  
    num_installments = max(1, order['installments'])  
    total_amount_cents = int((order['total'] * 100) + (order['tax']) + (order['freight'] * 100))  # Convert to cents
    face_value_cents = total_amount_cents // num_installments  # Divide equally among installments

    # Calculate the first installment's maturity date
    first_maturity_date = datetime.now(timezone.utc) + timedelta(days=paymentterm_days)

    installments = []
    for i in range(num_installments):
        # Calculate the maturity date for the current installment
        if i == 0:
            maturity_date = first_maturity_date  # First installment is due after paymentterm_days
        else:
            maturity_date = first_maturity_date + timedelta(days=30 * i)  # Subsequent installments are due every 30 days

        maturity_date_str = maturity_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        installments.append({
            "maturityDate": maturity_date_str,
            "faceValueCents": face_value_cents
        })

    return installments