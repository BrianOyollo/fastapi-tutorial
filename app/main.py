from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import json
import psycopg
import os 
import time


username = os.environ['POSTGRESQL_USER']
password = os.environ['POSTGRESQL_PASSWORD']
dbname = 'fastapidb'

while True:
    try:
        print(f"Connecting to {dbname} database ...", end='', flush=True)
        conn = psycopg.connect(
            host = 'localhost',
            user = username,
            password = password,
            dbname = dbname
        )
        cursor = conn.cursor()
        print(f"\rConnecting to {dbname} database ...success!")
        break
    
    except Exception as error:
        print(f"\rConnecting to {dbname} database ...failed!")
        print(error)
        time.sleep(2)

app = FastAPI(
    title="BlogAPI",
    version="1.0"
)

def read_db():
    with open('db.json', 'r') as file:
        posts = json.load(file)
    return posts

def write_db(posts):
    with open('db.json', 'w') as file:
        json.dump(posts, file, indent=3)

def find_post(post_id):
    posts = read_db()
    for index, post in enumerate(posts):
        if post['id'] == post_id:
            return index, post

def create_item(post):
    posts = read_db()
    posts.append(post)
    write_db(posts)


def del_item(post_id):
    posts = read_db()
    for index, post in enumerate(posts):
        if post['id'] == post_id:
            posts.pop(index)
    write_db(posts)


        

class Post(BaseModel):
    id:int
    title:str
    content:str
    published:bool = True
    rating:int|None=None

class updatePost(BaseModel):
    title:str|None=None
    content:str|None=None
    rating:int|None=None

@app.get('/posts')
async def all_posts():
    posts = read_db()
    return posts

@app.post("/posts/new", status_code=status.HTTP_201_CREATED)
async def new_post(post:Post): 
    new_post = post.model_dump()
    create_item(new_post)

@app.get("/posts/{post_id}")
async def get_post(post_id:int, response:Response):
    index, post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found!")
    return post
    

@app.delete("/posts/{post_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id:int):
    del_item(post_id)
    return {"Message": f"Post with id {post_id} has been deleted!"}

@app.put("/posts/{post_id}/update")
async def update_post(post_id:int, post_update:updatePost):
    index, post_to_update = find_post(post_id)

    if post_update.title:
        post_to_update['title'] = post_update.title
    if post_update.content:
        post_to_update['content'] = post_update.content
    if post_update.rating:
        post_to_update['rating'] = post_update.rating
    
    posts = read_db()
    posts[index] = post_to_update
    write_db(posts)

    return post_to_update


    
