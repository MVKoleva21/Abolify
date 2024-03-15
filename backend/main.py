from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.db import curr

from routes import users, chats, messages

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
app.include_router(chats.router)
app.include_router(messages.router)