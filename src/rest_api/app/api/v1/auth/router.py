from fastapi import APIRouter, Depends, HTTPException, status, Request, Response

from src.rest_api.app.api.v1.auth.service import AuthService
from src.rest_api.app.api.v1.auth.schema import (
    LoginRequest,
    AccessTokenResponse,
    MessageResponse, RegisterRequest,
)
from src.rest_api.app.core.dependencies import get_auth_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register", response_model=MessageResponse)
async def register(
    request_data: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
):
    success = await service.register(
        username=request_data.username,
        email=str(request_data.email),
        password=request_data.password,
        first_name=request_data.first_name,
        last_name=request_data.last_name,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User registration failed"
        )

    return MessageResponse(message="User registered successfully")


@router.post("/login", response_model=AccessTokenResponse)
async def login(
    login_data: LoginRequest,
    request: Request,
    response: Response,
    service: AuthService = Depends(get_auth_service)
):

    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    tokens = await service.login(
        username=login_data.username,
        password=login_data.password,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    response.set_cookie(key="refresh_token", value=tokens["refresh_token"], httponly=True)

    return AccessTokenResponse(access_token=tokens["access_token"])


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_token(
    request: Request,
    service: AuthService = Depends(get_auth_service),
):

    _refresh_token = request.cookies.get("refresh_token")

    if not _refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    result = await service.refresh_access_token(_refresh_token)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result


@router.post("/logout", response_model=MessageResponse)
async def logout(
    request: Request,
    response: Response,
    service: AuthService = Depends(get_auth_service)
):
    success = await service.revoke_refresh_token(request.cookies.get("refresh_token"))

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token not found"
        )

    response.delete_cookie(key="refresh_token")

    return MessageResponse(message="Successfully logged out")
