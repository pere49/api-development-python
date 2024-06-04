import pytest
from jose import jwt

from app import schemas
from app.config import settings

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

@pytest.mark.parametrize("email, password, status_code, detail", [
        ("test123@gmail.com", "pasword1234", 403, 'Invalid credentials'), 
        ("user@example.com", "pasword1234", 403, "Email not found"), 
        ("user@example.com", "pasword123", 403, "Email not found"),
        (None, 'password123', 422, None),
        ("test123@gmail.com", None, 422, None)])

def test_incorrect_login(client, test_user, email, password, status_code, detail):
    user = {"username": email, "password": password}
    res = client.post("/login", data=user)
    print(res.json().get('detail'))

    assert res.status_code == status_code
    # assert res.json().get('detail') == detail
