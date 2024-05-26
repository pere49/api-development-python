from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional, List
from sqlalchemy.orm import Session

from . import models, database
from .routers import post, user, auth


# creating database tables
models.Base.metadata.create_all(bind=database.engine)

# fastapi instance
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

""" API Routes """
@app.get("/")
async def root():
    return {"message": "Hello World"}

