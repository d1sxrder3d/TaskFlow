from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from src.rest_api.app.core.config import settings
from src.rest_api.app.core.logging_config import setup_uvicorn_loggers, logger
from src.rest_api.app.db import init_db, DatabaseManager
from src.rest_api.app.api import main_api_router


# noinspection PyUnusedLocal
@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info(f"Starting {settings.project_name} v{settings.version}")
    logger.info(f"Environment: {settings.debug_mode}")

    if settings.debug_mode in ("dev", "debug"):
        await init_db()


    yield

    await DatabaseManager.close()


app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    debug=settings.is_debug,
    lifespan=lifespan,
    logger=logger,
)


app.include_router(main_api_router)

setup_uvicorn_loggers()

if __name__ == "__main__":
    uvicorn.run(app, log_config=None)