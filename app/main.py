from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from dotenv import load_dotenv
import os

load_dotenv()
# fastapi instance
app = FastAPI()

# what we expect from the user
# title str, content str
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

""" Connecting to PostGres DB """
HOST=os.getenv('HOST')
DATABASE_NAME=os.getenv('DATABASE_NAME')
USER=os.getenv('USER')
PASSWORD=os.getenv('PASSWORD')
while True:
  try:
      conn = psycopg2.connect(host=HOST, database=DATABASE_NAME, user=USER, password=PASSWORD, cursor_factory=RealDictCursor)
      cursor = conn.cursor()
      print("Database connection was successful")
      break
  except Exception as error:
      print("Connection to database failed")
      print(f"error : {error}")
      time.sleep(2)


my_posts = [
  {"title": "Amazing Clouds","content": "Wispy formations danced across the cerulean canvas.","id": 1},
  {"title": "Cat Wisdom","content": "The purrfect nap spot is always a sunbeam.","id": 2  },
  {"title": "Baking Bonanza","content": "The aroma of freshly baked cookies filled the air with delight.","id": 3  },
  {"title": "Underwater Adventure","content": "Schools of colorful fish darted through the coral reef.","id": 4  },
  {"title": "Power of Music","content": "Melodies that could soothe the soul and ignite the spirit.","id": 5  },
  {"title": "Starry Night","content": "A blanket of twinkling diamonds adorned the inky expanse.","id": 6  },
  {"title": "City Lights","content": "A symphony of neon signs illuminated the bustling metropolis.","id": 7  },
  {"title": "Forest Symphony","content": "The rustle of leaves and the chirping of birds created a harmonious chorus.","id": 8  },
  {"title": "Bookworm Bliss","content": "Getting lost in a captivating story, transported to another world.","id": 9  },
  {"title": "Rainy Day Dreams",    "content": "The rhythmic pitter-patter on the windowpane, a soothing lullaby.","id": 10  }
]

""" Utility functions """
def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


""" API Routes """
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts; """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # Method 1 using local data
    # post_dict = post.model_dump()
    # post_dict["id"] = randrange(0, 1000000)
    # my_posts.append(post_dict)

    # Method 2 using postgres database
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # Method 1: using local data
    # post = find_post(id)

    # Method 2: Using postgres ql
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        # method 1
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return  {'message': f"Post with id {id} was not found"}

        # method 2
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    return {"post-detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # Method 1: Using local data
    index = find_index_post(id)

    # Method 2: Using POSTGRES QL
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} does not exist")
    
    # my_posts.pop(index)
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    # Method 1: using local data
    # index = find_index_post(id)
    # convert user input from front end to a dict
    # assign request id to user indut
    # update dict at current index with the new data
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    # print(post)

    # Method 2: Using PostGres ql
    cursor.execute(""" UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING * """, 
                   (post.title, post.content, str(id)))
    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} does not exist")
    
    conn.commit()
    
    return {'data': updated_post}