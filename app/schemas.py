from pydantic import BaseModel

# what we expect from the user
# title str, content str
class Post(BaseModel):
    title: str
    content: str
    published: bool = True