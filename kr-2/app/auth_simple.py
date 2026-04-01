from typing import Optional, Dict
from uuid import uuid4

from fastapi import APIRouter, Response, Cookie, HTTPException

router = APIRouter()

FAKE_USER_DB: Dict[str, str] = {
    "user123": "password123",
}

SESSIONS: Dict[str, str] = {}


@router.post("/login")
def login_simple(data: dict, response: Response):
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")

    if FAKE_USER_DB.get(username) != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = str(uuid4())
    SESSIONS[token] = username

    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        max_age=300,
    )

    return {"message": "Logged in", "session_token": token}


@router.get("/user")
def get_user_simple(session_token: Optional[str] = Cookie(default=None)):
    if not session_token or session_token not in SESSIONS:
        raise HTTPException(status_code=401, detail="Unauthorized")

    username = SESSIONS[session_token]
    return {"username": username, "profile": "Simple profile info"}