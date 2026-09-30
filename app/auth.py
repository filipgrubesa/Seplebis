import secrets
import string
import bcrypt
import os
from dotenv import load_dotenv
load_dotenv()

def genuser(length: int):
    chars: str = string.ascii_letters
    username: str = "".join(secrets.choice(chars) for _ in range(length))
    return username

def genpass(length: int):
    chars: str = string.ascii_letters + string.digits + string.punctuation
    password: str = "".join(secrets.choice(chars) for _ in range (length))
    return password

def hashpass(password:str, rounds=12) -> bytes:
    pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
    return pw

def checkpass(password:str, hashed_password:bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)

def getkey():
    return os.getenv("JWT_SECRET")