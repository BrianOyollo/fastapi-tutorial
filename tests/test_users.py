from fastapi.testclient import TestClient
from jose import jwt, JWTError
from app import schemas


import pytest
import os
from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')



def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get('message') == "Welcome to the blog!"


def test_create_user(client):
    test_user = {"email":"jasonhayes@gmail.com", "password":"Testpass123"}
    response = client.post('/users/new', json=test_user)

    new_test_user = schemas.UserResponse(**response.json())
    assert response.status_code == 201
    assert new_test_user.email == 'jasonhayes@gmail.com'


def test_login_user(client, test_user):
    response = client.post("/login", data={'username':test_user['email'], 'password':test_user['password']})
    login_response = schemas.Token(**response.json())
    
    # verify token
    payload = jwt.decode(login_response.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    
    assert response.status_code == 200
    assert login_response.token_type == 'bearer'
    assert payload.get('user_id') == test_user['id']


@pytest.mark.parametrize("username, password, status_code", [
    ('wrongemail@gmail.com', 'Testpass123', 403),
    ('jasonhayes@gmail.com', 'Testpass1233', 403),
    ('wrongemail@gmail.com', 'Testpass1223', 403),
    (None, 'Testpass123', 422),
    ('wrongemail@gmail.com', None, 422),
    (None, None, 422),
])
def test_incorrect_login(client, test_user, username, password, status_code):
    response = client.post("/login", data={'username': username, 'password':password})
    assert response.status_code == status_code
    