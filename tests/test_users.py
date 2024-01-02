from fastapi.testclient import TestClient
from app import schemas
from .database import session, client

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get('message') == "Welcome to the blog!"


def test_create_user(client):
    test_user = {"email":"jsonhayes@gmail.com", "password":"Testpass123"}
    response = client.post('/users/new', json=test_user)

    new_test_user = schemas.UserResponse(**response.json())
    assert response.status_code == 201
    assert new_test_user.email == 'jsonhayes@gmail.com'
    