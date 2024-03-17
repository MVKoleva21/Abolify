from fastapi import APIRouter, HTTPException, Depends
from db.db import curr, conn
from models.UserIM import UserIM
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

@router.post("/register", tags=["authentication"])
async def register(user_im: UserIM):
    curr.execute("""SELECT * FROM users WHERE username = %s""", (user_im.username, ))

    user_db = curr.fetchone()

    for char in user_im.username:
        if not char.isalnum() and char != '_':
            raise HTTPException(status_code=400, detail="Username may only contain letters, numbers and underscores")

    if user_db:
        raise HTTPException(status_code=403, detail=f"User with username {user_im.username} already exists")

    salt = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(64))

    password = hashlib.sha512((salt + user_im.password).encode('utf-8')).hexdigest()

    curr.execute("""
    INSERT INTO users(id, username, password)
    VALUES
        (DEFAULT, %s, %s);
    """, (user_im.username, password))

    with open("db/salt.json", 'r') as f:
        salts = json.load(f)

    salts[user_im.username] = salt

    with open("db/salt.json", 'w') as f:
        json.dump(salts, f)

    conn.commit()

@router.post("/login", tags=["authentication"])
async def login(user_im: UserIM):
    print(user_im.username)
    curr.execute("""SELECT * FROM users WHERE username = %s""", (user_im.username, ))

    user_db = curr.fetchone()

    if not user_db:
        raise HTTPException(status_code=400, detail=f"User with username {user_im.username} not found")
    
    with open("db/salt.json", 'r') as f:
        salt = json.load(f)[user_im.username]

    password = hashlib.sha512((salt + user_im.password).encode('utf-8')).hexdigest()

    if password != user_db[2]:
        raise HTTPException(status_code=400, detail="Incorrect password")

    key = ''
    for i in os.getenv("RSA_PRIVATE").split(","):
        key += i + "\n"
    private_key = key

    token = jwt.encode({"iss": user_db[0], "exp": datetime.datetime.now(tz=pytz.utc) + datetime.timedelta(hours=3)}, private_key, algorithm="RS256")

    return {"access_token": token}

@router.post("/token", tags=["authentication"])
async def token(user_im: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    print(user_im.username)
    curr.execute("""SELECT * FROM users WHERE username = %s""", (user_im.username, ))

    user_db = curr.fetchone()

    if not user_db:
        raise HTTPException(status_code=401, detail=f"User with username {user_im.username} not found", headers={"WWW-Authenticate": "Bearer"})
    
    with open("db/salt.json", 'r') as f:
        salt = json.load(f)[user_im.username]

    password = hashlib.sha512((salt + user_im.password).encode('utf-8')).hexdigest()

    if password != user_db[2]:
        raise HTTPException(status_code=401, detail="Incorrect password", headers={"WWW-Authenticate": "Bearer"})

    key = ''
    for i in os.getenv("RSA_PRIVATE").split(","):
        key += i + "\n"
    private_key = key

    token = jwt.encode({"iss": user_db[0], "exp": datetime.datetime.now(tz=pytz.utc) + datetime.timedelta(hours=3)}, private_key, algorithm="RS256")

    return Token(access_token=token, token_type="bearer")

@router.get("/user", tags=["users"])
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
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

    curr.execute("""SELECT * FROM users WHERE id = %s""", (payload["iss"], ))

    user = curr.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user[1]

@router.get("/user/chats", tags=["users", "chats"])
async def get_user_chats(token: Annotated[str, Depends(oauth2_scheme)]):
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

    curr.execute("SELECT * FROM chats WHERE user_id = %s", (payload["iss"], ))

    return curr.fetchall()