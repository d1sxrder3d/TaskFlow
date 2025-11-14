from fastapi import Request, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED



async def verify_token(request: Request):
    token = request.headers.get("Authorization")

    if not token or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )


    return True
