import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/55")
    assert res.status_code == 404

def test_authorized_user_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Posts.id == test_posts[0].id
    assert post.Posts.content == test_posts[0].content
    assert res.status_code == 200

@pytest.mark.parametrize("title, content, published", [
    ("Amazing Clouds","Wispy formations danced across the cerulean canvas.", True),
    ("Cat Wisdom","The purrfect nap spot is always a sunbeam.", False),
    ("Baking Bonanza","The aroma of freshly baked cookies filled the air with delight.", False)
    ])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published, "user_id": test_user["id"]})
    # print(res.json())
    created_post = schemas.ResponsePost(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user["id"]

def test_create_post_default_pubished_true(authorized_client, test_user):
    res = authorized_client.post("/posts/", json={"title": "Something", "content": "Some content", "user_id": test_user["id"]})
    created_post = schemas.ResponsePost(**res.json())
    assert res.status_code == 201
    assert created_post.title == "Something"
    assert created_post.content == "Some content"
    assert created_post.published == True
    assert created_post.user_id == test_user["id"]

def test_unauthorised_user_create_post(client, test_user):
    res = client.post("/posts/", json={"title": "Something", "content": "Some content", "user_id": test_user["id"]})
    assert res.status_code == 401

def test_unauthorised_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/255")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_user2, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated titile", 
        "content": "updated content",
        "id": test_posts[0].id}
    
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json = data)
    updated_post = schemas.Post(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated titile", 
        "content": "updated content",
        "id": test_posts[3].id}
    
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json = data)
    assert res.status_code == 403

def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated titile", 
        "content": "updated content",
        "id": test_posts[0].id}
    
    res = authorized_client.put(f"/posts/100", json = data)
    assert res.status_code == 404

def test_unauthorised_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401