from fastapi import FastAPI, Response, status, HTTPException, Depends
#from fastapi.params import Body
#from pydantic import BaseModel
#from random import randrange
#from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import False_
from fastapi.middleware.cors import CORSMiddleware
from app.routers.vote import vote
from . import models,schemas, utils
from .database import Base, engine, get_db
from .routers import post, user, auth, vote
from .config import settings
models.Base.metadata.create_all(bind=engine)
app=FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#savedposts= [{"title":"niggers","content":"niggers", "id": 2},{"title":"niggers","content":"niggers", "id": 3}]
#def find_post(id):
    #for p in savedposts:
        #if p["id"]==id:
            #return p
#def find_post_index(id):
    #for i,p in enumerate(savedposts):
        #if p['id'] == id:
            #return i
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
#@app.get("/")
#async def root():
    #return {"message": "Nigga on a horse"}
