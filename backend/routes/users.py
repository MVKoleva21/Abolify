from fastapi import APIRouter, HTTPException
from db.db import curr, conn
from modules.UserIM import UserIM
from dotenv import load_dotenv
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

@router.post("/register", tags=["users"])
def register(user_im: UserIM):
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

@router.post("/login", tags=["users"])
def login(user_im: UserIM):
    curr.execute("""SELECT * FROM users WHERE username = %s""", (user_im.username, ))

    user_db = curr.fetchone()

    if not user_db:
        raise HTTPException(status_code=400, detail=f"User with username {user_im.username} not found")
    
    with open("db/salt.json", 'r') as f:
        salt = json.load(f)[user_im.username]

    password = hashlib.sha512((salt + user_im.password).encode('utf-8')).hexdigest()

    if password != user_db[2]:
        raise HTTPException(status_code=400, detail="Incorrect password")

    private_key = os.getenv("RSA_PRIVATE")

    token = jwt.encode({"iss": user_db[0], "exp": datetime.datetime.now(tz=pytz.utc) + datetime.timedelta(hours=3)}, private_key, algorithm="RS256")

    return {"token": token}