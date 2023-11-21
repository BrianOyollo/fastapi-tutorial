from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from datetime import datetime, timedelta
from . import schemas, database, models
from sqlalchemy.orm import Session
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data:dict):
    data_to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(data_to_encode,  SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str, credentials_exception):
    try:
        # decode the access_token and get id(user_id)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id:str = payload.get('user_id')
        
        # raise exception if id doesn't exist
        if user_id is None:
            raise credentials_exception
        
        # else validate the id
        token_data = schemas.TokenData(id=user_id)

    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", 
                                          headers={' WWW-Authenticate':'Bearer'})
    
    current_token = verify_access_token(token, credentials_exception)
    current_user = db.query(models.User).filter(models.User.id == current_token.id).first()
    return current_user