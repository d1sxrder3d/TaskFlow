from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError

from src.rest_api.app.api.v1.users.service import UserService
from src.rest_api.app.api.v1.users.schema import (
    UserCreateRequest,
    UserUpdateRequest,
    UserResponse,
    UserListResponse,
)
from src.rest_api.app.core.dependencies import get_user_service
from src.rest_api.app.core.security import decode_jwt
from src.rest_api.app.repositories.user import UserRepository
from src.rest_api.app.db import User
from src.rest_api.app.core.dependencies import get_user_repository


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@router.get("", response_model=UserListResponse)
async def get_users(
    service: UserService = Depends(get_user_service),
):
    users = await service.get_all_users()
    return UserListResponse(users=users, total=len(users))


@router.get("/me", response_model=UserResponse)
async def get_me(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repository),
):
    try:
        payload = decode_jwt(token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = await user_repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    user = await service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    return user


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateRequest,
    service: UserService = Depends(get_user_service),
):
    try:
        user = await service.create_user(
            username=user_data.username,
            email=str(user_data.email),
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            is_active=user_data.is_active,
            is_superuser=user_data.is_superuser,
        )
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username or email already exists"
        )


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdateRequest,
    service: UserService = Depends(get_user_service),
):
    update_data = user_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )

    try:
        user = await service.update_user(user_id, **update_data)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )

        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    user = await service.delete_user(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )


@router.get("/organization/{organization_id}", response_model=List[UserResponse])
async def get_users_by_organization(
    organization_id: int,
    service: UserService = Depends(get_user_service),
):
    users = await service.get_users_by_organization(organization_id)
    return users


@router.get("/project/{project_id}", response_model=List[UserResponse])
async def get_users_by_project(
    project_id: int,
    service: UserService = Depends(get_user_service),
):
    users = await service.get_users_by_project(project_id)
    return users


@router.get("/task/{task_id}", response_model=List[UserResponse])
async def get_users_by_task(
    task_id: int,
    service: UserService = Depends(get_user_service),
):
    users = await service.get_users_by_task(task_id)
    return users

