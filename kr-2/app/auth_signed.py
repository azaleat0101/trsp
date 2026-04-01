import time
from typing import Optional

from fastapi import APIRouter, Response, Cookie, HTTPException
from itsdangerous import URLSafeSerializer, BadSignature
from uuid import uuid4

router = APIRouter()

SECRET_KEY = "super_secret_key_for_itsdangerous"
serializer = URLSafeSerializer(SECRET_KEY, salt="session")

SESSION_TTL = 300        # 5 минут
SESSION_RENEW_MIN = 180  # 3 минуты


def create_session_token(user_id: str, timestamp: int) -> str:
    data = {"user_id": user_id, "timestamp": timestamp}
    return serializer.dumps(data)


def parse_session_token(token: str) -> dict:
    try:
        return serializer.loads(token)
    except BadSignature:
        raise HTTPException(status_code=401, detail="Invalid session")


@router.post("/login_signed")
def login_signed(data: dict, response: Response):
    username = data.get("username")
    password = data.get("password")

    if username != "user123" or password != "password123":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id = str(uuid4())
    now = int(time.time())
    token = create_session_token(user_id=user_id, timestamp=now)

    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        secure=False, 
        max_age=SESSION_TTL,
    )

    return {"message": "Logged in", "user_id": user_id}


@router.get("/profile")
def profile(
    response: Response,
    session_token: Optional[str] = Cookie(default=None),
):
    if not session_token:
        raise HTTPException(status_code=401, detail="Session expired")

    data = parse_session_token(session_token)
    user_id = data["user_id"]
    ts = data["timestamp"]
    now = int(time.time())
    diff = now - ts

    if diff > SESSION_TTL:
        raise HTTPException(status_code=401, detail="Session expired")

    if SESSION_RENEW_MIN <= diff <= SESSION_TTL:
        new_token = create_session_token(user_id=user_id, timestamp=now)
        response.set_cookie(
            key="session_token",
            value=new_token,
            httponly=True,
            secure=False,
            max_age=SESSION_TTL,
        )

    return {"user_id": user_id, "message": "Profile data"}