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
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    email:EmailStr
    created_at:datetime

    class Config:
        form_attributes = True

class LikeResponse(BaseModel):
    user_id:int

    class Config:
        form_attributes = True

class PostResponse(BaseModel):
    title:str
    content:str
    created_at:datetime
    author_info:UserResponse
    # likes:LikeResponse

    class Config:
        form_attributes = True


class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:int|None=None

