from fastapi import Header, HTTPException, status
from typing import Annotated
from core.config import settings


async def validate_auth_headers(
    x_parse_rest_api_key: Annotated[str, Header()] = None,
    x_jwt_kwy: Annotated[str, Header()] = None,
):
    if not x_parse_rest_api_key or not x_jwt_kwy:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authentication Headers",
        )

    if x_parse_rest_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
        )

    return True
