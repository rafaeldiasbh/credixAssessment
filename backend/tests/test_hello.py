from fastapi.testclient import TestClient
from src.main import app
from http import HTTPStatus

root = '/api/v1'

def test_hello():
    client = TestClient(app)
    response = client.get(root)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello World"}

