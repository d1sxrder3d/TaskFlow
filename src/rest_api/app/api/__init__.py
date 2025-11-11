from src.rest_api.app.api.v1 import *

main_api_router = APIRouter(
    prefix="/api",
    tags=["api"],
)


main_api_router.include_router(api_v1_router, tags=["v1"])



