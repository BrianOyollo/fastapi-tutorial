from fastapi import FastAPI
import os 
from . import models
from .database import engine
from .routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BlogAPI",
    version="1.0"
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)