from fastapi import APIRouter, Depends, HTTPException, status, Request, Response

from src.rest_api.app.api.v1.auth.service import AuthService
from src.rest_api.app.api.v1.auth.schema import (
    LoginRequest,
    AccessTokenResponse,
    MessageResponse, RegisterRequest,
)
from src.rest_api.app.core.dependencies import get_auth_service
from src.rest_api.app.core.logging_config import logger

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register", response_model=MessageResponse)
async def register(
        request_data: RegisterRequest,
        service: AuthService = Depends(get_auth_service),
):
    try:
        success = await service.register(
            username=request_data.username,
            email=str(request_data.email),
            password=request_data.password,
            first_name=request_data.first_name,
            last_name=request_data.last_name,
        )

        if not success:
            logger.warning(f"Registration failed for username: {request_data.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User registration failed"
            )

        logger.info(f"User registered successfully: {request_data.username}")
        return MessageResponse(message="User registered successfully")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/login", response_model=AccessTokenResponse)
async def login(
        login_data: LoginRequest,
        request: Request,
        response: Response,
        service: AuthService = Depends(get_auth_service)
):
    try:
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")

        tokens = await service.login(
            username=login_data.username,
            password=login_data.password,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        if not tokens:
            logger.warning(f"Failed login attempt for username: {login_data.username}, IP: {ip_address}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh_token"],
            httponly=True,
            secure=True,
            samesite="lax"
        )

        logger.info(f"User logged in successfully: {login_data.username}, IP: {ip_address}")
        return AccessTokenResponse(access_token=tokens["access_token"])

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_token(
        request: Request,
        service: AuthService = Depends(get_auth_service),
):
    try:
        _refresh_token = request.cookies.get("refresh_token")

        if not _refresh_token:
            logger.warning("Refresh token missing in request")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token missing",
                headers={"WWW-Authenticate": "Bearer"},
            )

        result = await service.refresh_access_token(_refresh_token)

        if not result:
            logger.warning("Invalid or expired refresh token attempt")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info("Access token refreshed successfully")
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during token refresh: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/logout", response_model=MessageResponse)
async def logout(
        request: Request,
        response: Response,
        service: AuthService = Depends(get_auth_service)
):
    _refresh_token = request.cookies.get("refresh_token")

    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=True,
        samesite="lax"
    )

    if refresh_token:
        try:
            success = await service.revoke_refresh_token(_refresh_token)
            if success:
                logger.info("Refresh token revoked successfully")
            else:
                logger.warning("Refresh token not found in database, but logout proceeded")
        except Exception as e:
            logger.error(f"Error revoking refresh token during logout: {str(e)}", exc_info=True)
    else:
        logger.info("Logout called without refresh token (already logged out or cookie expired)")

    return MessageResponse(message="Successfully logged out")