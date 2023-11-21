from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from .. import models, schemas,oauth2
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.PostResponse1])
# @router.get('/')
async def all_posts(db:Session = Depends(get_db), q:Optional[str]=""):
    posts = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(models.Like, models.Like.post_id == models.Post.id).group_by(models.Post.id).all()
    
    return posts


@router.get("/{post_id}", response_model=schemas.PostResponse)
async def get_post(post_id:int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found!")
    return post


@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def new_post(post:schemas.Post, db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)): 
    new_post = models.Post(author=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{post_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id:int, db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post_to_delete_query = db.query(models.Post).filter(models.Post.id == post_id)
    post_to_delete = post_to_delete_query.first()

    if post_to_delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found!")
    
    if post_to_delete.author != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this request!")
    
    post_to_delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{post_id}/update", response_model=schemas.PostResponse)
async def update_post(post_id:int, post_update:schemas.updatePost, db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post_to_update_query = db.query(models.Post).filter(models.Post.id == post_id)
    post_to_update = post_to_update_query.first()

    if post_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with id {post_id} not found!')
     
    if post_to_update.author != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this request!")
    
    post_to_update_query.update(post_update.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()

    return post_to_update