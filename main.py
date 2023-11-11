from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

def read_db():
    with open('db.json', 'r') as file:
        posts = json.load(file)
    return posts

def update_db(post):
    posts = read_db()
    posts.append(post)

    with open('db.json', 'w') as file:
        json.dump(posts, file, indent=3)

def find_post(post_id):
    posts = read_db()
    for post in posts:
        if post['id'] == post_id:
            return post
        

class Post(BaseModel):
    id:int
    title:str
    content:str
    published:bool = True
    rating:int|None=None

@app.get('/posts')
async def all_posts():
    posts = read_db()
    return posts

@app.post("/posts/new", status_code=status.HTTP_201_CREATED)
async def new_post(post:Post): 
    new_post = post.model_dump()
    update_db(new_post)

@app.get("/posts/{post_id}")
async def get_post(post_id:int, response:Response):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found!")
    return post
    