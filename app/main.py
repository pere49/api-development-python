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


""" API Routes """
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Posts).all()
    return posts

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts", response_model=List[schemas.ResponsePost])
def get_posts(db: Session = Depends(database.get_db)):
    # Method 2: Using RAW SQL
    # cursor.execute(""" SELECT * FROM posts; """)
    # posts = cursor.fetchall()
    # print(posts)

    # Method 3: Using SQLAlchemy ORM
    posts = db.query(models.Posts).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
def create_posts(post: schemas.Post, db: Session = Depends(database.get_db)):
    # Method 1 using local data
    # post_dict = post.model_dump()
    # post_dict["id"] = randrange(0, 1000000)
    # my_posts.append(post_dict)

    # Method 2 using postgres database(raw sql)
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # Method 3: Using SQLAlchemy ORM
    new_post = models.Posts(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}", response_model=schemas.ResponsePost)
def get_post(id: int, response: Response, db: Session = Depends(database.get_db)):
    # Method 1: using local data
    # post = find_post(id)

    # Method 2: Using postgres ql
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()

    # Method 3: Using SQLAlchemy ORM
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        # method 1
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return  {'message': f"Post with id {id} was not found"}

        # method 2
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db)):
    # Method 1: Using local data
    # index = find_index_post(id)
    # # my_posts.pop(index)

    # Method 2: Using POSTGRES QL
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    
    # conn.commit()

    # Method 3: Using SQLAlchemy ORM
    post = db.query(models.Posts).filter(models.Posts.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.ResponsePost)
def update_post(id: int, updated_post:schemas.Post, db: Session = Depends(database.get_db)):
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
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING * """, 
    #                (post.title, post.content, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    # Method 3: Using SQLAlchemy ORM
    post_query = db.query(models.Posts).filter(models.Posts.id == id) 
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} does not exist")
    
    post_query.update(updated_post.model_dump())
    db.commit()
    return post_query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUser)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # hash the password from user.password
    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users/{id}", response_model=schemas.ResponseUser)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found")
    return user