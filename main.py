from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

# fastapi instance
app = FastAPI()

# what we expect from the user
# title str, content str
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
  {
    "title": "Amazing Clouds",
    "content": "Wispy formations danced across the cerulean canvas.",
    "id": 1
  },
  {
    "title": "Cat Wisdom",
    "content": "The purrfect nap spot is always a sunbeam.",
    "id": 2
  },
  {
    "title": "Baking Bonanza",
    "content": "The aroma of freshly baked cookies filled the air with delight.",
    "id": 3
  },
  {
    "title": "Underwater Adventure",
    "content": "Schools of colorful fish darted through the coral reef.",
    "id": 4
  },
  {
    "title": "Power of Music",
    "content": "Melodies that could soothe the soul and ignite the spirit.",
    "id": 5
  },
  {
    "title": "Starry Night",
    "content": "A blanket of twinkling diamonds adorned the inky expanse.",
    "id": 6
  },
  {
    "title": "City Lights",
    "content": "A symphony of neon signs illuminated the bustling metropolis.",
    "id": 7
  },
  {
    "title": "Forest Symphony",
    "content": "The rustle of leaves and the chirping of birds created a harmonious chorus.",
    "id": 8
  },
  {
    "title": "Bookworm Bliss",
    "content": "Getting lost in a captivating story, transported to another world.",
    "id": 9
  },
  {
    "title": "Rainy Day Dreams",    
    "content": "The rhythmic pitter-patter on the windowpane, a soothing lullaby.",
    "id": 10
  }
]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    print(id)
    return {"post-detail": find_post(id)}
