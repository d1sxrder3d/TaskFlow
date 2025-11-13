from fastapi import APIRouter, Depends, HTTPException, status, Request

from src.rest_api.app.api.v1.auth.service import AuthService
from src.rest_api.app.api.v1.auth.schema import (
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse,
    AccessTokenResponse,
    MessageResponse,
)
from src.rest_api.app.core.dependencies import get_auth_service


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    request: Request,
    service: AuthService = Depends(get_auth_service),
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

    return tokens


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    service: AuthService = Depends(get_auth_service),
):
    result = await service.refresh_access_token(refresh_data.refresh_token)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result


@router.post("/logout", response_model=MessageResponse)
async def logout(
    refresh_data: RefreshTokenRequest,
    service: AuthService = Depends(get_auth_service),
):
    success = await service.revoke_refresh_token(refresh_data.refresh_token)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token not found"
        )

    return MessageResponse(message="Successfully logged out")

