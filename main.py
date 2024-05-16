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

my_posts = [
  {
    "title": "Amazing Clouds",
    "content": "Wispy formations danced across the cerulean canvas.",
    "id": 12345
  },
  {
    "title": "Cat Wisdom",
    "content": "The purrfect nap spot is always a sunbeam.",
    "id": 54321
  },
  {
    "title": "Baking Bonanza",
    "content": "The aroma of freshly baked cookies filled the air with delight.",
    "id": 98765
  },
  {
    "title": "Underwater Adventure",
    "content": "Schools of colorful fish darted through the coral reef.",
    "id": 36987
  },
  {
    "title": "Power of Music",
    "content": "Melodies that could soothe the soul and ignite the spirit.",
    "id": 25874
  },
  {
    "title": "Starry Night",
    "content": "A blanket of twinkling diamonds adorned the inky expanse.",
    "id": 74123
  },
  {
    "title": "City Lights",
    "content": "A symphony of neon signs illuminated the bustling metropolis.",
    "id": 65432
  },
  {
    "title": "Forest Symphony",
    "content": "The rustle of leaves and the chirping of birds created a harmonious chorus.",
    "id": 89012
  },
  {
    "title": "Bookworm Bliss",
    "content": "Getting lost in a captivating story, transported to another world.",
    "id": 43210
  },
  {
    "title": "Rainy Day Dreams",    
    "content": "The rhythmic pitter-patter on the windowpane, a soothing lullaby.",
    "id": 10987
  }
]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(new_post: Post):
    print(new_post.rating)
    print(new_post.model_dump())
    return {"data": f"new post"}

# what we expect from the user
# title str, content str