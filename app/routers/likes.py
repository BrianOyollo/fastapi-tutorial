from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/likes",
    tags = ['likes']
)


@router.post("/{post_id}/like", status_code=status.HTTP_201_CREATED)
async def like_post(post_id:int, db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # check if posts exists
    post_query = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist!")

    like_query = db.query(models.Like).filter(models.Like.user_id == current_user.id, models.Like.post_id == post_id)
    found_like = like_query.first()

    if found_like:
        # if unlike if it had been liked (a like exists)
        like_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        # like the post
        new_like = models.Like(user_id = current_user.id, post_id = post_id)
        db.add(new_like)
        db.commit()
        return {"Message":f"Post with id {post_id} liked"}
        

