from fastapi.testclient import  TestClient
from app.main import app
from app import schemas

client = TestClient(app)

def test_root():
    resp = client.get("/")
    print(resp.json().get("message"))
    assert resp.json().get("message") == 'Hello World'


def test_create_user():
    user = {"email": "test123@gmail.com", "password": "password123"}
    res = client.post("/users", json=user)
    
    new_user =  schemas.ResponseUser(**res.json())
    print(new_user.email)
    assert new_user.email == "test123@gmail.com"
    assert res.status_code == 201