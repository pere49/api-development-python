import pytest
from fastapi.testclient import  TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base
from app.config import settings
from app.oauth import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "test123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    user = res.json()
    user['password'] = "password123"
    yield user

@pytest.fixture
def token(test_user):
    return create_access_token(({"user_id": test_user['id']}))

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {"title": "Amazing Clouds", "content": "Wispy formations danced across the cerulean canvas.",
        "user_id": test_user["id"]},
        {"title": "Cat Wisdom", "content": "The purrfect nap spot is always a sunbeam.",
        "user_id": test_user["id"]},
        {"title": "Baking Bonanza", "content": "The aroma of freshly baked cookies filled the air with delight.",
        "user_id": test_user["id"]},
        {"title": "Underwater Adventure", "content": "Schools of colorful fish darted through the coral reef.",
        "user_id": test_user["id"]}]
    
    def create_post_model(post):
        return models.Posts(**post)
    
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)    
    session.add_all(posts)
    session.commit()
    post_query = session.query(models.Posts).all()
    return post_query
