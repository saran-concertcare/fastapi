from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from database import engine, get_db,Base
from sqlite3 import Timestamp
from sqlalchemy.sql.expression import text
import models
from routers import auth,details,users

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







