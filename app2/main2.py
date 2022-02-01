from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from enum import auto
from logging import exception
from turtle import mode
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange 
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import Boolean
from app.main import post
from . import models,schemas,utils
from .database import engine, get_db
from .routers import details,users,auth


models.Base.metadata.create_all(bind = engine)

app = FastAPI()


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
    

app.include_router(details.router)
app.include_router(users.router)
app.include_router(auth.router)







