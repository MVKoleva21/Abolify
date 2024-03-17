from fastapi import APIRouter, HTTPException, Depends
from db.db import curr, conn
from models.MessageIM import MessageIM
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
import json
from collections import Counter
import re
from openai import OpenAI
from heapq import nlargest

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/message", tags=["messages"])
async def post_message(message: MessageIM, token: Annotated[str, Depends(oauth2_scheme)]):
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
    
    curr.execute("SELECT * FROM chats WHERE id = %s", (message.chat_id, ))

    chat_db = curr.fetchone()

    if chat_db[1] != payload["iss"]:
        raise HTTPException(status_code=401, detail=f"User doesn't own chat with id {chat_db[0]}")
    
    curr.execute("""
    INSERT INTO messages(id, chat_id, content, created_at)
    VALUES
        (DEFAULT, %s, %s, DEFAULT)
    RETURNING *
    """, (message.chat_id, message.content))

    conn.commit()

    response = generate_response(message.content)

    curr.execute("""
    INSERT INTO messages(id, chat_id, content, created_at)
    VALUES
        (DEFAULT, %s, %s, DEFAULT)
    RETURNING *
    """, (message.chat_id, response))

    conn.commit()

    return curr.fetchone()

def generate_response(message: str):
    with open("data/context.txt", "r") as f:
        gpt_assistant_prompt = f.read()
    message=[{"role": "assistant", "content": gpt_assistant_prompt}, {"role": "user", "content": message}]
    temperature=0.2
    max_tokens=256
    frequency_penalty=0.0

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages = message,
        temperature=temperature,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty
    )

    return response.choices[0].message.content