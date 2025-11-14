import os
os.environ["APP_ENV"] = "test"
from dotenv import load_dotenv
import pytest
import subprocess

@pytest.fixture(scope="session", autouse=True)
def set_test_env():

    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env.test'), override=True)

    alembic_ini = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/rest_api/alembic.ini'))
    subprocess.run([
        "alembic",
        "-c",
        alembic_ini,
        "upgrade",
        "head"
    ], check=True)


# TODO: Тесты миграций на Postgres!! Остальные на SQLite