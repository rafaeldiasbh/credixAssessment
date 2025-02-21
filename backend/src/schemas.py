from pydantic import BaseModel, EmailStr, constr, Field
from typing import List

class HelloMessage(BaseModel):
    message: str

class Product(BaseModel):
    name: str
    amount: int
    unitcost: float

class Checkout(BaseModel):
    id: str
    name: str
    address: str
    zipcode: constr(min_length=8, max_length=8)  # Constrain zipcode length to brazilian standart
    phone: constr(min_length=10, max_length=20)  # note sure of international phones sizes.
    email: EmailStr  
    productsvalue: float
    discount: float
    freight: float
    producttotal: float
    paymentterm: int
    installments: int
    products: List[Product] 