from sqlite3 import Cursor
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange 
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class post(BaseModel):
    title: str
    content: str
    published: bool = True
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


my_posts = [{"title": "title of post 1","content":"content of post 1","id":1},
{"title":"favourite food","content":"I love biriyani","id":2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {'message' : 'welcome to my api!!!!!!'}

@app.get('/posts')
def get_posts():
    
    return {'data': "hi"}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post : post):
    
    return {"data" : "abcd"}


@app.get("/posts/{id}")
def get_post(id: int):
    
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post id with:{id} is not found")
    return {"post detail" : post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index=find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with id:{id} does not exist')    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    


@app.put("/posts/{id}")
def update_post(id: int,post: post):
     index=find_index_post(id)

     if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with id:{id} does not exist')
   
     post_dict=post.dict
     post_dict['id'] = id
     my_posts[index] = post_dict
     return {'data' : post_dict} 
