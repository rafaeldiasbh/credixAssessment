from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class ProductSchema(BaseModel):
    name: str
    amount: int
    unitcost: float

class CheckoutCreateSchema(BaseModel):
    name: str
    address: str
    zipcode: str = Field(..., min_length=5, max_length=10)
    phone: str = Field(..., pattern=r"^\d{10,15}$")
    email: EmailStr
    productsvalue: float
    discount: float
    freight: float
    producttotal: float
    paymentterm: int
    installments: int
    products: List[ProductSchema]

class CheckoutSchema(BaseModel):
    id: str = Field(..., description="The ID of the order (required for PUT/PATCH/DELETE)")
    name: str
    address: str
    zipcode: str = Field(..., min_length=5, max_length=10)
    phone: str = Field(..., pattern=r"^\d{10,15}$")
    email: EmailStr
    productsvalue: float
    discount: float
    freight: float
    producttotal: float
    paymentterm: int
    installments: int
    products: List[ProductSchema]  # List of ProductSchema