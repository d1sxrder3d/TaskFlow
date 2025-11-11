from fastapi import APIRouter

from src.rest_api.app.api.v1.users import users_router

api_v1_router = APIRouter(
    prefix="/v1",
    tags=["v1"],
)

api_v1_router.include_router(users_router, tags=["users"])
