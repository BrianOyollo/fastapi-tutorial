from fastapi.testclient import TestClient
from jose import jwt, JWTError
from app import schemas
from .database import session, client
import pytest
import os
from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

@pytest.fixture
def test_user(client):
    test_user_data = {"email":"jsonhayes@gmail.com", "password":"Testpass123"}
    response = client.post("/users/new", json=test_user_data)
    test_user = response.json()
    test_user['password'] = test_user_data['password']
    print(test_user)
    return test_user

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


def test_login_user(client, test_user):
    response = client.post("/login", data={'username':test_user['email'], 'password':test_user['password']})
    login_response = schemas.Token(**response.json())
    
    # verify token
    payload = jwt.decode(login_response.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    
    assert response.status_code == 200
    assert login_response.token_type == 'bearer'
    assert payload.get('user_id') == test_user['id']