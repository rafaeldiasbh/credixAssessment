from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ....schemas.order import CheckoutCreateSchema, CheckoutSchema
from ....services.order_service import create_order
from ....core.db import SessionLocal
from http import HTTPStatus

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/newOrder", status_code=HTTPStatus.CREATED, response_model=CheckoutSchema)
def create_new_order(order: CheckoutCreateSchema, db: Session = Depends(get_db)):
    return create_order(db, order)