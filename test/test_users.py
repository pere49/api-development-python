import pytest
from jose import jwt

from .database import client, session
from app import schemas
from app.config import settings

@pytest.fixture
def test_user(client):
    user_data = {"email": "test123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    user = res.json()
    user['password'] = "password123"
    yield user

def test_root(client):
    resp = client.get("/")
    print(resp.json().get("message"))
    assert resp.json().get("message") == 'Hello World'


def test_create_user(client):
    user = {"email": "test123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user)
    
    new_user =  schemas.ResponseUser(**res.json())
    print(new_user.email)
    assert new_user.email == "test123@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    user = {"username": test_user["email"], "password": test_user["password"]}
    res = client.post("/login", data=user)
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200