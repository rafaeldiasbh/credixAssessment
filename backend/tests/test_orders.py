from fastapi.testclient import TestClient
from src.main import app
from http import HTTPStatus
import hashlib, uuid, json

root = '/api/v1'

def generate_idempotency_key(data: str) -> str:
    # Hash the data using SHA256
    hash_object = hashlib.sha256(data.encode())
    hash_hex = hash_object.hexdigest()
    
    # Generate a UUID5 using the hash as the name and a fixed namespace (URL)
    namespace = uuid.NAMESPACE_URL
    idempotency_key = str(uuid.uuid5(namespace, hash_hex))
    
    return idempotency_key

def test_order_flow():
    client = TestClient(app)
    
    # Create an order
    payload = {
        "name": "automated test",
        "taxid": "26900161000125",
        "address": "string",
        "address2": "string",
        "postalcode": "string",
        "phone": "98252859772441",
        "email": "user@example.com",
        "productstotal": 10.0,
        "discount": 0.0,
        "freight": 1.0,
        "total": 11.0,
        "paymentterm": 7,
        "installments": 2,
        "products": [
            {
                "name": "automatedTest1",
                "amount": 1,
                "unitcost": 10.0
            }
        ]
    }

    # Convert the payload to a JSON string
    payload_json = json.dumps(payload, sort_keys=True)  # Sort keys to ensure consistent hashing
    
    # Generate the idempotency key
    idempotency_key = generate_idempotency_key(payload_json)

    # Create the order
    create_response = client.post(root + '/orders', json=payload, headers={"Idempotency-Key": idempotency_key})
    
    assert create_response.status_code == HTTPStatus.CREATED, "Failed to create order"
    
    # Extract the order ID and status from the response
    create_response_data = create_response.json()
    order_id = create_response_data.pop("id")
    create_response_data.pop("status") # ll not be used and cant be present
    create_response_data.pop("credixid") 
    create_response_data.pop("fee") 

    # Verify the response data matches the payload
    assert create_response_data == payload, "Response data does not match payload"
    
    # Step 2: Retrieve the order and verify its existence
    get_response = client.get(f"{root}/orders/{order_id}")
    assert get_response.status_code == HTTPStatus.OK, "Failed to retrieve order"
    
    get_response_data = get_response.json()
    assert get_response_data["id"] == order_id, "Retrieved order ID does not match"
    
    # Step 3: Delete the order
    delete_response = client.delete(f"{root}/orders/{order_id}")
    assert delete_response.status_code == HTTPStatus.NO_CONTENT, "Failed to delete order"
    
    # Step 4: Verify the order no longer exists
    get_deleted_response = client.get(f"{root}/orders/{order_id}")
    assert get_deleted_response.status_code == HTTPStatus.NOT_FOUND, "Order still exists after deletion"

def test_get_all_orders():
    client = TestClient(app)
    
    # Create an order
    payload = {
        "name": "automated test",
        "taxid": "26900161000125",
        "address": "string",
        "address2": "string",
        "postalcode": "string",
        "phone": "98252859772441",
        "email": "user@example.com",
        "productstotal": 10.0,
        "discount": 0.0,
        "freight": 1.0,
        "total": 12.0,
        "paymentterm": 7,
        "installments": 2,
        "products": [
            {
                "name": "automatedTest1",
                "amount": 1,
                "unitcost": 11.0
            }
        ]
    }

    # Convert the payload to a JSON string
    payload_json = json.dumps(payload, sort_keys=True)  # Sort keys to ensure consistent hashing
    
    # Generate the idempotency key
    idempotency_key = generate_idempotency_key(payload_json)

    
    # Create the order
    create_response = client.post(root + '/orders', json=payload, headers={"Idempotency-Key": idempotency_key})
    assert create_response.status_code == HTTPStatus.CREATED, "Failed to create order"
    
    # Extract the order ID from the response
    order_id = create_response.json()["id"]
    
    # Step 2: Fetch all orders
    get_all_response = client.get(root + '/orders')
    assert get_all_response.status_code == HTTPStatus.OK, "Failed to fetch all orders"
    
    # Verify the created order is in the list
    orders = get_all_response.json()
    assert any(order["id"] == order_id for order in orders), "Created order not found in the list"