from pydantic import BaseModel, EmailStr
from datetime import datetime

# what we expect from the user
# title str, content str
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class ResponsePost(Post):
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class ResponseUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes= True