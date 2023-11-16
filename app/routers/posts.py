from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas,oauth2
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.PostResponse])
async def all_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.get("/{post_id}", response_model=schemas.PostResponse)
async def get_post(post_id:int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    # query = "SELECT * FROM fastapi WHERE id = %s"
    # post = cursor.execute(query,(post_id,)).fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found!")
    return post


@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def new_post(post:schemas.Post, db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)): 
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # query = "INSERT INTO fastapi (title, content,published) VALUES(%s,%s,%s) RETURNING *"
    # new_post = cursor.execute(query, (title, content, published)).fetchone()
    # conn.commit()
    return new_post


@router.delete("/{post_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id:int, db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # query = "DELETE FROM fastapi WHERE id = %s RETURNING *"
    deleted_post = db.query(models.Post).filter(models.Post.id == post_id)
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found!")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{post_id}/update", response_model=schemas.PostResponse)
async def update_post(post_id:int, post_update:schemas.updatePost, db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    # query = "UPDATE fastapi SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *"
    updated_post = db.query(models.Post).filter(models.Post.id == post_id)

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with id {post_id} not found!')
    
    updated_post.update(post_update.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()

    return updated_post.first()