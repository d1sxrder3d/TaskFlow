from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv


try:
    load_dotenv()
except FileNotFoundError:
    from src.rest_api.app.core.logging_config import logger
    logger.error(".env file not found. Make sure it exists in the project root.")
except Exception as e:
    from src.rest_api.app.core.logging_config import logger
    logger.error(e)

BASE_DIR: Path = Path(__file__).resolve().parent.parent

DB_PATH: Path = BASE_DIR / "db.sqlite3"
LOGS_DIR: Path = BASE_DIR / "logs"
CERTS_DIR: Path = BASE_DIR / "certs"


class DBSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

    type: Literal["sqlite", "postgres"] = "sqlite"

    sqlite_path: Path = DB_PATH

    host: str = "localhost"
    port: int = 5432
    name: str = "app_db"
    user: str = "root"
    password: str = "root"

    echo: bool = False
    pool_pre_ping: bool = False

    @property
    def url(self) -> str:
        if self.type == "postgres":
            return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        return f"sqlite+aiosqlite:///{self.sqlite_path}"

    @property
    def engine_options(self) -> dict:
        options = {"echo": self.echo}

        if self.type == "postgres":
            options.update({
                "pool_size": 5,
                "max_overflow": 10,
                "pool_pre_ping": True,
            })

        return options

class AuthSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_prefix="AUTH_",
        env_file=".env",
        case_sensitive=False
    )

    private_key_path: Path = CERTS_DIR / "private.pem"
    public_key_path: Path = CERTS_DIR / "public.pem"
    algorithm: str = "RS256"

    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )


    project_name: str = "FastAPI Project"
    version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"

    debug_mode: Literal["dev", "debug", "prod"] = "dev"


    auth: AuthSettings = AuthSettings()
    db: DBSettings = DBSettings()

    @property
    def is_debug(self) -> bool:
        return self.debug_mode in ("dev", "debug")


settings = Settings()

if __name__ == "__main__" and settings.is_debug:
    from src.rest_api.app.core.logging_config import logger

    logger.info(f"Mode: {settings.debug_mode}")
    logger.info(f"Database URL: {settings.db.url}")
    logger.info(f"Echo SQL: {settings.db.echo}")
