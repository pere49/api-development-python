import os
from dotenv import load_dotenv

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session


from . import models, database, schemas, utils
from .routers import post, user, auth

load_dotenv()


# creating database tables
models.Base.metadata.create_all(bind=database.engine)

# fastapi instance
app = FastAPI()

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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

""" API Routes """
@app.get("/")
async def root():
    return {"message": "Hello World"}

