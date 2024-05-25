from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# what we expect from the user
# title str, content str
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class ResponseUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes= True
class ResponsePost(Post):
    id: int
    created_at: datetime
    user_id: int
    user: ResponseUser
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None