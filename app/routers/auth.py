from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, database, utils, models, oauth2
from sqlalchemy.orm import Session



router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", response_model=schemas.Token)
async def login(user_logins:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    # OAuth2PasswordrequestForm stores email/username input in "username"

    user = db.query(models.User).filter(models.User.email == user_logins.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect username or password. Please try again!")
    
    if not utils.verify_password(user_logins.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect username or password. Please try again!")
    
    access_token = oauth2.create_access_token(data = {'user_id':user.id})
    
    return {
        "access_token":f"{access_token}",
        "token_type":"Bearer"    
            }