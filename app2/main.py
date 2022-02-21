from pydantic import BaseModel
from typing import Optional,List
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from database import get_db
import models,schemas
from . import oauth2
from database import get_db
from typing import List
from sqlite3 import Cursor

class PostBase(BaseModel):
    student_id: str
    student_name: str
    academic_year: str
    total_fees: str
    fees_paid: str
    balance_fees: str

router = APIRouter(
    prefix="/details",
    tags=["Details"]
)

'''
@app.get('/')
async def read_root():
    return {"message": "Hello World"}
'''

@router.get('/',response_model=List[schemas.Post])
async def test_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return  posts

