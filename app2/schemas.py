from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime

class PostBase(BaseModel):
    student_id: str
    student_name: str
    academic_year: str
    total_fees: str
    fees_paid: str
    balance_fees: str

class PostCreate(PostBase):
    pass
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Post(PostBase):
    created_at: datetime
    owner_id: int
    owner :UserOut
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Refresh_Token(BaseModel):
    refresh_token : str
    token_type: str

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)