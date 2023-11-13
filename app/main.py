from fastapi import FastAPI, Response, status, HTTPException,Depends
from pydantic import BaseModel
import json
import psycopg
from psycopg.rows import dict_row
import os 
import time
from . import models
from .database import get_db, engine
from sqlalchemy.orm import Session


username = os.environ['POSTGRESQL_USER']
password = os.environ['POSTGRESQL_PASSWORD']
dbname = 'fastapidb'

models.Base.metadata.create_all(bind=engine)



# while True:
#     try:
#         print(f"Connecting to {dbname} database ...", end='', flush=True)
#         conn = psycopg.connect(
#             host = 'localhost',
#             user = username,
#             password = password,
#             dbname = dbname,
#             row_factory=dict_row
#         )
#         cursor = conn.cursor()
#         print(f"\rConnecting to {dbname} database ...success!")
#         break
    
#     except Exception as error:
#         print(f"\rConnecting to {dbname} database ...failed!")
#         print(error)
#         time.sleep(2)

app = FastAPI(
    title="BlogAPI",
    version="1.0"
)

class Post(BaseModel):
    title:str
    content:str
    published:bool = True

class updatePost(BaseModel):
    title:str|None=None
    content:str|None=None
    published:bool|None=None


# @app.get("/posts")
# async def get_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {'posts':posts}


@app.get('/posts')
async def all_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'posts':posts}

@app.get("/posts/{post_id}")
async def get_post(post_id:int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter_by(id=post_id).all()
    return {'post':post}
    # query = "SELECT * FROM fastapi WHERE id = %s"
    # post = cursor.execute(query,(post_id,)).fetchone()

    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found!")
    # return post

@app.post("/posts/new", status_code=status.HTTP_201_CREATED)
async def new_post(post:Post, db:Session = Depends(get_db)): 
    title = post.title
    content = post.content
    published = post.published

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # query = "INSERT INTO fastapi (title, content,published) VALUES(%s,%s,%s) RETURNING *"
    # new_post = cursor.execute(query, (title, content, published)).fetchone()
    # conn.commit()
    return {'post':new_post}

    

# @app.delete("/posts/{post_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(post_id:int):
#     query = "DELETE FROM fastapi WHERE id = %s RETURNING *"
#     deleted_post = cursor.execute(query, (post_id,)).fetchone()

#     if not deleted_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found!")
    
#     conn.commit()
#     return deleted_post

# @app.put("/posts/{post_id}/update")
# async def update_post(post_id:int, post_update:updatePost):

#     query = "UPDATE fastapi SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *"
#     updated_post = cursor.execute(query, (post_update.title, post_update.content,post_update.published, post_id)).fetchone()

#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with id {post_id} not found!')

#     conn.commit()
#     return updated_post


    
