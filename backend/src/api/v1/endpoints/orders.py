from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ....schemas.order import CheckoutCreateSchema, CheckoutSchema
from ....services.order_service import create_order, get_all_orders
from ....core.db import SessionLocal
from http import HTTPStatus
from uuid import UUID

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/orders", response_model=list[CheckoutSchema])
async def get_orders(db: Session = Depends(get_db)):
    return await get_all_orders(db)

@router.post("/orders", status_code=HTTPStatus.CREATED, response_model=CheckoutSchema)
async def create_new_order(order: CheckoutCreateSchema, idempotency_key: UUID = Header(...), db: Session = Depends(get_db)):
    return await create_order(db, idempotency_key, order)