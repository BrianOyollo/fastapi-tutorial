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


@app.get('/posts')
async def all_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'posts':posts}

@app.get("/posts/{post_id}")
async def get_post(post_id:int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    # query = "SELECT * FROM fastapi WHERE id = %s"
    # post = cursor.execute(query,(post_id,)).fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found!")
    return post


@app.post("/posts/new", status_code=status.HTTP_201_CREATED)
async def new_post(post:Post, db:Session = Depends(get_db)): 
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # query = "INSERT INTO fastapi (title, content,published) VALUES(%s,%s,%s) RETURNING *"
    # new_post = cursor.execute(query, (title, content, published)).fetchone()
    # conn.commit()
    return {'post':new_post}

    

@app.delete("/posts/{post_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id:int, db:Session = Depends(get_db)):
    # query = "DELETE FROM fastapi WHERE id = %s RETURNING *"
    deleted_post = db.query(models.Post).filter(models.Post.id == post_id)
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found!")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{post_id}/update")
async def update_post(post_id:int, post_update:updatePost, db:Session = Depends(get_db)):

    # query = "UPDATE fastapi SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *"
    updated_post = db.query(models.Post).filter(models.Post.id == post_id)

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with id {post_id} not found!')
    
    updated_post.update(post_update.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()

    return updated_post.first()


    
