from datetime import datetime

from fastapi import APIRouter, Header, HTTPException, Depends, Response
from typing import Optional

from .models import CommonHeaders

router = APIRouter()


@router.get("/headers")
def get_headers(
    user_agent: Optional[str] = Header(default=None, alias="User-Agent"),
    accept_language: Optional[str] = Header(default=None, alias="Accept-Language"),
):
    if not user_agent or not accept_language:
        raise HTTPException(status_code=400, detail="Required headers missing")

    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language,
    }


def get_common_headers(
    user_agent: str = Header(alias="User-Agent"),
    accept_language: str = Header(alias="Accept-Language"),
) -> CommonHeaders:
    if not user_agent or not accept_language:
        raise HTTPException(status_code=400, detail="Required headers missing")

    return CommonHeaders(
        **{
            "User-Agent": user_agent,
            "Accept-Language": accept_language,
        }
    )


@router.get("/headers_v2")
def headers_v2(common: CommonHeaders = Depends(get_common_headers)):
    return {
        "User-Agent": common.user_agent,
        "Accept-Language": common.accept_language,
    }


@router.get("/info")
def info(
    response: Response,
    common: CommonHeaders = Depends(get_common_headers),
):
    response.headers["X-Server-Time"] = datetime.utcnow().isoformat()

    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": common.user_agent,
            "Accept-Language": common.accept_language,
        },
    }