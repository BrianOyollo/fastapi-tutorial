from pydantic import BaseModel, EmailStr, ConfigDict
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
    model_config = ConfigDict(form_attributes=True)

    id:int
    email:EmailStr
    created_at:datetime

    # class ConfigDict:
    #     form_attributes = True


class PostResponse(BaseModel):
    id:int
    title:str
    content:str
    published:bool
    created_at:datetime
    author_info:UserResponse


    class ConfigDic:
        form_attributes = True

class PostLikesResponse(BaseModel):
    model_config = ConfigDict(form_attributes=True)

    Post:PostResponse
    likes:int

    # class Config:
    #     form_attributes = True


class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:int|None=None

