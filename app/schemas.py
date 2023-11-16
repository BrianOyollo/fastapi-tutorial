from pydantic import BaseModel, EmailStr
from datetime import datetime

# ----------- Posts ---------------------------

class Post(BaseModel):
    title:str
    content:str
    published:bool = True

class updatePost(BaseModel):
    title:str|None=None
    content:str|None=None
    published:bool|None=None


class User(BaseModel):
    id:int
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    email:EmailStr
    created_at:datetime

    class Config:
        form_attributes = True


class PostResponse(BaseModel):
    title:str
    content:str
    created_at:datetime
    author_info:UserResponse

    class Config:
        form_attributes = True


# ------------------- authentication ----------------------

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:int|None=None