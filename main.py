from fastapi import FastAPI
from db import models
from db.database import engine
from routers import user, post, comment
from auth import authentication

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



@app.get('/')
def root():
    return "Hello World"

app.include_router(user.router)
app.include_router(post.router)
app.include_router(authentication.router)
app.include_router(comment.router)


# Database Configuration
models.Base.metadata.create_all(engine)


# Image Configuration
app.mount('/images', StaticFiles(directory='images'), name='images')


# CORE Configuration
origins = [
    'http://localhost:3000',
    'http://10.0.2.2:8000', # Andriod Emulator
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specify your trusted domains
    allow_credentials=True,
    allow_methods=["*"],  # Restrict methods
    allow_headers=["*"],  # Restrict headers
)











