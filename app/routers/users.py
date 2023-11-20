from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags = ['Users']
)

@router.get("", response_model=List[schemas.UserResponse])
async def get_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    if users == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no users")
    return users


@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def register_user(user:schemas.User, db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"A user with email '{user.email}' already exists. Please use a different one!")


@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user(user_id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} does not exist!")
    return user


