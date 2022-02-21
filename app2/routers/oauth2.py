from statistics import mode
from jose import JWTError,jwt
from datetime import datetime, timedelta
import schemas,database,models
from sqlalchemy.orm import Session
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List
from config import settings


#secret_key
#algorithm
#access_token expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 10

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'login')

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm = ALGORITHM)

    return encoded_jwt
def create_refresh_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt
def verify_access_token(token: str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms = [ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

def verify_refresh_token(refresh_token: str,credentials_exception):
    try:
        refresh_payload = jwt.decode(refresh_token,SECRET_KEY,algorithms = [ALGORITHM])

        id: str = refresh_payload.get("user_id")

        if id is None:
            raise credentials_exception
        refresh_token_data = schemas.TokenData(id=id)
        print(refresh_payload)
    except JWTError:
        raise credentials_exception 

    return refresh_token_data

def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token,credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
