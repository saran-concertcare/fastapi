from fastapi import FastAPI
from database import engine
import models
from routers import auth,details,users
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

origins = ["https://www.google.co.in","https://www.youtube.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


    

app.include_router(details.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/')
def root():
    return {"message": "Hello World"}




