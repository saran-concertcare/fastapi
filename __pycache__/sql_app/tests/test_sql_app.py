from http import client
import json
from fastapi.testclient import TestClient
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

router = APIRouter(
    prefix="/details",
    tags=["Details"]
)

Base = declarative_base()

def get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()



SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost/test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base.metadata.create_all(bind = engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

router.dependency_overrides[get_db] = override_get_db

client = TestClient(router)

def test_create_user():
    response = client.post("/users/",json={"email": "saran@gmail.com","password": "123456789"})
    assert response.status_code == 200,response.text
    data = response.json()
    assert data["email"] == "saran@gmail.com"
    assert id in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200,response.text
    data = response.json()
    assert data["email"] == "saran@gmail.com"
    assert data["id"] == user_id