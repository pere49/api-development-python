from .database import client, session
from app import schemas

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

def test_login_user(client):
    user = {"username": "test123@gmail.com", "password": "password123"}
    res = client.post("/login", data=user)
    assert res.status_code == 200