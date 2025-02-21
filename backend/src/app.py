from fastapi import FastAPI
from .schemas import HelloMessage
from http import HTTPStatus

app = FastAPI()

@app.get('/', status_code=HTTPStatus.OK, response_model=HelloMessage)
def read_root():
    return {"message": "Hello World"}

@app.post('/newOrder', status_code=HTTPStatus.CREATED)
def create_order(order: Checkout):
    return ''