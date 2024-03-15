from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.UserIM import UserIM
from db.db import curr

from routes import users

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)