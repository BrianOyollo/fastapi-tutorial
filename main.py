from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

posts= [
    {
        "id":1,
        "title":"Post 1",
        "content":"Proident aliqua consequat exercitation do ex amet sint eiusmod."
    },
    {
        "id":2,
        "title":"Post 2",
        "content":"Proident aliqua consequat exercitation do ex amet sint eiusmod."
    }
]

def find_post(post_id):
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
    return posts

@app.post("/posts/new")
async def new_post(post:Post): 
    new_post = post.model_dump()
    posts.append(new_post)

@app.get("/posts/{post_id}")
async def get_post(post_id:int):
    post = find_post(post_id)
    return post
    