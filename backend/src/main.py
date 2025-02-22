from fastapi import FastAPI
from .api.v1.endpoints import orders, hello
from .core.db import Base, engine

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

#  routes
app.include_router(hello.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")