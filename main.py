from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

# fastapi instance
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}

@app.post("/posts")
def create_posts(new_post: Post):
    print(new_post.rating)
    print(new_post.model_dump())
    return {"data": f"new post"}

# what we expect from the user
# title str, content str