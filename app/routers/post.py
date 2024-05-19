from typing import List

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, database, schemas

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/sqlalchemy")
def test_posts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Posts).all()
    return posts

@router.get("/", response_model=List[schemas.ResponsePost])
def get_posts(db: Session = Depends(database.get_db)):
    # Method 2: Using RAW SQL
    # cursor.execute(""" SELECT * FROM posts; """)
    # posts = cursor.fetchall()
    # print(posts)

    # Method 3: Using SQLAlchemy ORM
    posts = db.query(models.Posts).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
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

@router.get("/{id}", response_model=schemas.ResponsePost)
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

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@router.put("/{id}", response_model=schemas.ResponsePost)
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
