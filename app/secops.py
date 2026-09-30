from fastapi import Request, HTTPException
import jwt
from .auth import getkey
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

def verify_token(request: Request) -> str:
    authtoken = request.cookies.get("jwt")
    if authtoken is None:
        raise HTTPException(status_code=401, detail="Not authenticated.")
    try:
        payload = jwt.decode(authtoken, getkey(), algorithms=["HS256"])
    except (ExpiredSignatureError):
        raise HTTPException(status_code=401, detail="Session expired, please log in again.")
    except (InvalidTokenError):
        raise HTTPException(status_code=401, detail="The token is invalid or expired.")

    return payload["user_id"]