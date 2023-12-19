from fastapi import FastAPI
import os 
from . import models
from .database import engine
from .routers import posts, users, auth, likes
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BlogAPI",
    version="1.0"
)
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"messgae":"Welcome to our blog!"}

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(likes.router)
app.include_router(auth.router)