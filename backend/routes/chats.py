from fastapi import APIRouter, HTTPException, Depends
from db.db import curr, conn
from models.ChatIM import ChatIM
from models.Token import Token
from dotenv import load_dotenv
from typing import Annotated, Union
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import hashlib
import random
import string
import json
import jwt
import os
import datetime
import pytz

router = APIRouter()

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/chat/{chat_id}", tags=["chats"])
def get_chat_messages(chat_id:int, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        key = ''
        for i in os.getenv("RSA_PUBLIC").split(","):
            key += i + "\n"
        public_key = key

        payload = jwt.decode(token, public_key, algorithms=["RS256"])

    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Invalid token signature")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Token couldn't be decoded")

    curr.execute("SELECT * FROM chats WHERE id = %s", (chat_id, ))

    chat_db = curr.fetchone()

    if not chat_db:
        raise HTTPException(status_code=400, detail="Chat doesn't exist")

    if chat_db[1] != payload["iss"]:
        raise HTTPException(status_code=401, detail=f"User doesn't own chat with id {chat_db[0]}")

    curr.execute("SELECT * FROM messages WHERE chat_id = %s", (chat_id, ))

    messages_db = curr.fetchall()

    return {
        "alias": chat_db[2],
        "messages": messages_db
    }

@router.post("/chat", tags=["chats"])
def add_chat(chat: ChatIM, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        key = ''
        for i in os.getenv("RSA_PUBLIC").split(","):
            key += i + "\n"
        public_key = key

        payload = jwt.decode(token, public_key, algorithms=["RS256"])

    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Invalid token signature")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Token couldn't be decoded")
    
    curr.execute("""
    INSERT INTO chats(id, user_id, alias)
    VALUES
        (DEFAULT, %s, %s)
    RETURNING *
    """, (payload["iss"], chat.alias))

    conn.commit()

    return curr.fetchone()

@router.put("/chat/{chat_id}", tags=["chats"])
def rename_chat(chat: ChatIM, chat_id: int, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        key = ''
        for i in os.getenv("RSA_PUBLIC").split(","):
            key += i + "\n"
        public_key = key

        payload = jwt.decode(token, public_key, algorithms=["RS256"])

    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Invalid token signature")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Token couldn't be decoded")
    
    curr.execute("SELECT * FROM chats WHERE id = %s", (chat_id, ))

    chat_db = curr.fetchone()

    if not chat_db:
        raise HTTPException(status_code=400, detail="Chat doesn't exist")

    if chat_db[1] != payload["iss"]:
        raise HTTPException(status_code=401, detail=f"User doesn't own chat with id {chat_db[0]}")

    curr.execute("UPDATE chats SET alias=%s WHERE id=%s RETURNING *", (chat.alias, chat_db[0]))

    conn.commit()

    return curr.fetchone()
