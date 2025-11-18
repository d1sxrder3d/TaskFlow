from fastapi import APIRouter, Depends

from src.rest_api.app.api.middlewares.security import verify_token
from .users.router import router as users_router
from .auth.router import router as auth_router
from .organizations.router import router as organizations_router
from .projects.router import router as projects_router
from .tasks.router import router as tasks_router
from .files.router import router as files_router
from .tags.router import router as tags_router


api_v1_router = APIRouter(
    prefix="/v1",
    tags=["v1"],
)


api_v1_router.include_router(auth_router, tags=["auth"])


api_v1_router.include_router(
    users_router,
    tags=["users"],
    dependencies=[Depends(verify_token)])

api_v1_router.include_router(
    organizations_router,
    tags=["organizations"],
    dependencies=[Depends(verify_token)]
)

api_v1_router.include_router(
    projects_router,
    tags=["projects"],
    dependencies=[Depends(verify_token)]
)

api_v1_router.include_router(
    tasks_router,
    tags=["tasks"],
    dependencies=[Depends(verify_token)]
)

api_v1_router.include_router(
    files_router,
    tags=["files"],
    dependencies=[Depends(verify_token)]
)

api_v1_router.include_router(
    tags_router,
    tags=["tags"],
    dependencies=[Depends(verify_token)]
)
