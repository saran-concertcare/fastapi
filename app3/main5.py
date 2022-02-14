from ast import Str
import email
from fastapi import FastAPI,Depends,HTTPException,status
from pydantic import BaseModel
from typing import List
from fastapi_jwt_auth import AuthJWT
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from enum import auto
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange 
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app.main import post
#from .. import models,schemas
#from . import oauth2
#from ..database import get_db
from typing import List
from sqlite3 import Cursor
from sqlalchemy.orm import Session

app = FastAPI()

class Settings(BaseModel):
    authjwt_secret_key:str = 'e683b5d1992e4ba549478ff317e3ed71a6afea0ef5babe9eed5cd253874d2371'


@AuthJWT.load_config
def get_config():
    return Settings()

class User(BaseModel):
    id: str
    email: str
    password: str

    class Config():
        schema_extra={
            "example":{
                "username": "saran",
                "email": "saran@gmail.com",
                "password": "password"
            }
        }

while True:
    try:
        conn=psycopg2.connect(host="localhost",database="fastapi3",user="postgres",password="password123",
        cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error: ",error)
        time.sleep(2)

class Post(BaseModel):
    student_id: str
    student_name: str
    academic_year: str
    total_fees: str
    fees_paid: str
    balance_fees: str

@app.get("/get")
def get_details():
    cursor.execute("SELECT * FROM student_details")
    details= cursor.fetchall()
    return {"data": details}


@app.post("/signup",status_code=201)
def create_user(user: User):
    cursor.execute("""INSERT INTO USERS (id,email,password) VALUES(%s,%s,%s) RETURNING * """,
    (user.id,user.email,user.password))
    new_details=cursor.fetchall()
    conn.commit()
    return {"data" : new_details}

@app.post("/login")
def login(user:User,Authorize:AuthJWT=Depends()):
    for u in user:
        if (u.id==user.id) and (u.password==user.password):
            access_token = Authorize.create_access_token(subject=user.id)
            refresh_token = Authorize.create_refresh_token(subject=user.id)

            return {"access_token": access_token,"refresh_token": refresh_token}

        raise HTTPException(status_code=401,detail="Invalid credentials")

@app.get("/protected")
def get_logged_in_user(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")


    current_user = Authorize.get_jwt_subject()

    return {"Current_user": current_user}


@app.get("/new_token")
def create_new_token(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    current_user = Authorize.get_jwt_subject()

    access_token = Authorize.create_access_token(subject=current_user)

    return {"new_access_token": access_token}

@app.post("/fresh_login")
def fresh_login(user:User,Authorize:AuthJWT=Depends()):
    for u in ("""SELECT * FROM USERS """):
        if (u.id==user.id) and (u.password==user.password):
            fresh_token = Authorize.create_access_token(subject=user.id,fresh=True)

            return {"fresh_token": fresh_token}

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")
    

@app.get("/fresh_url")
def get_user(Authorize:AuthJWT=Depends()):
    try:
        Authorize.fresh_jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid details")
    
    current_user = Authorize.get_jwt_subject()
    return {"Current_user": current_user}