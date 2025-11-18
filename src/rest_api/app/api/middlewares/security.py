from fastapi import Request, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from src.rest_api.app.core.security import decode_jwt


async def verify_token(request: Request):
    token = request.headers.get("Authorization")

    if not token or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )

    jwt_token = token.removeprefix("Bearer ").strip()
    try:
        decode_jwt(jwt_token)
    except Exception:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return True
