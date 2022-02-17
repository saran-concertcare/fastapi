from http import client
from urllib import response
from fastapi import FastAPI

app= FastAPI()

@app.get('/')
async def read_root():
    return {"message": "Hello World"}



