from logging import exception
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


class bio(BaseModel):
    student_id: str 
    student_name: str
    father_name: str
    mother_name: str
    academic_year: str
    address: str

while True:
    try:
        conn=psycopg2.connect(host="localhost",database="fastapi3",user="postgres",password="password123",
        cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection was successful")
        break
    except exception as error:
        print("Database connection failed")
        print("Error: ",error)
        time.sleep(2)

@app.get("/personal_details")
def get_personal_info():
    cursor.execute("SELECT * FROM personal_info")
    perosonal_details=cursor.fetchall()
    return {"data": perosonal_details}

@app.post("/personal_details")
def create_personal_info(info :bio ):
    cursor.execute("""INSERT INTO personal_info(student_id,student_name,father_name,mother_name,academic_year,address) 
    VALUES (%s,%s,%s,%s,%s,%s) RETURNING * """,(info.student_id,info.student_name,info.father_name,info.mother_name,
    info.academic_year,info.address))
    bio_data=cursor.fetchall()
    conn.commit()
    return {"data": bio_data}


@app.get("/personal_details/{id}")
def get_details(id: int):
    cursor.execute("""SELECT *FROM personal_info WHERE student_id = %s """,(str(id)))
    single_data=cursor.fetchone()
    if not single_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,deetail=f"data with id:{id} was not found")
    return {"data": single_data}


@app.delete("/personal_details/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM personal_info WHERE student_id = %s returning *""",(str(id)))
    delete_post = cursor.fetchone()
    conn.commit()

    if not delete_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/personal_details/{id}")
def update_post(id: int, post: bio):
    cursor.execute("""UPDATE personal_info SET student_id=%s,student_name=%s,father_name=%s,mother_name=%s,
    academic_year=%s,address=%s WHERE student_id = %s RETURNING *""",(post.student_id,post.student_name,post.father_name,
    post.mother_name,post.academic_year, post.address,(str(id))))
    updated_post=cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    return {"data" : updated_post}