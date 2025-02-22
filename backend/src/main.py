from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.endpoints import orders, hello
from .core.db import Base, engine

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any origin for the assessment
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods 
    allow_headers=["*"],  # Allow all headers
)

#  routes
app.include_router(hello.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")