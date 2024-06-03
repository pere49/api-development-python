import pytest
from fastapi.testclient import  TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import schemas, models
from app.main import app
from app.database import get_db, Base
from app.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)

# Dependency
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

def test_root(client):
    resp = client.get("/")
    print(resp.json().get("message"))
    assert resp.json().get("message") == 'Hello World'


def test_create_user(client):
    user = {"email": "test123@gmail.com", "password": "password123"}
    res = client.post("/users", json=user)
    
    new_user =  schemas.ResponseUser(**res.json())
    print(new_user.email)
    assert new_user.email == "test123@gmail.com"
    assert res.status_code == 201