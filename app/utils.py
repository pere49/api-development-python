import json
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return  pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

""" Utility functions for .json file """
with open("./app/fake_db.json") as f:
    my_posts = json.load(f)

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i