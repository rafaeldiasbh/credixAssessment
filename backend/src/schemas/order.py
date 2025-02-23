from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional

class ProductSchema(BaseModel):
    name: str
    amount: int
    unitcost: float

class BaseCheckoutSchema(BaseModel):
    name: str
    taxid: str
    address: str
    address2: Optional[str] = Field(None)
    postalcode: Optional[str] = Field(None, min_length=5, max_length=10)
    phone: Optional[str] = Field(None, pattern=r"^\d{10,15}$")
    email: Optional[EmailStr] = Field(None, description="Email address (optional)")
    productstotal: float
    discount: float
    freight: float
    total: float
    paymentterm: int
    installments: int

    # Custom validator to convert empty strings to None
    @validator("postalcode", "phone", "email", pre=True)
    def empty_str_to_none(cls, value):
        if value == "":
            return None
        return value

class CheckoutCreateSchema(BaseCheckoutSchema):
    products: List[ProductSchema]

class CheckoutSchema(BaseCheckoutSchema):
    id: int = Field(..., description="The ID of the order (required for PUT/PATCH/DELETE)")
    status: str
    credixid: Optional[str]
    fee: float
    products: Optional[List[ProductSchema]] = Field(
        None,
        description="List of products (optional for updates)"
    )