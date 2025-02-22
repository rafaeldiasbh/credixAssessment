from fastapi.testclient import TestClient
from src.main import app
from http import HTTPStatus

root = '/api/v1'

def test_create_order():
    client = TestClient(app)
    payload = {"name":"string","address":"string","zipcode":"string","phone":"2703651141972","email":"user@example.com","productsvalue":0.0,"discount":0.0,"freight":0.0,"producttotal":0.0,"paymentterm":0,"installments":0,"products":[{"name":"string","amount":0,"unitcost":0.0}]}
    response = client.post(root+'/newOrder', json=payload)
    response_data = response.json()
    pop = response_data.pop("id")
    status = response_data.pop("status")
    assert response.status_code == HTTPStatus.CREATED
    assert response_data == payload and pop and status == 'pending'
