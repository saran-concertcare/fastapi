from sqlite3 import Timestamp
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from database import Base
from sqlalchemy.orm import relationship




class Post(Base):
    __tablename__ = "posts"


    student_id = Column(Integer,primary_key=True,nullable=False)
    student_name = Column(String,nullable=False)
    academic_year = Column(String,nullable=False)
    total_fees = Column(Integer,nullable=False)
    fees_paid = Column(Integer,nullable=False)
    balance_fees = Column(Integer,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False) 


    owner = relationship("User")
class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))