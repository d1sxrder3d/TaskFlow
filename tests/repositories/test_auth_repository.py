import pytest
from unittest.mock import AsyncMock, MagicMock
from src.rest_api.app.repositories.auth import AuthRepository


@pytest.mark.asyncio
async def test_get_refresh_token():
    db = AsyncMock()
    repo = AuthRepository(db)

    scalars_mock = MagicMock()
    scalars_mock.first.return_value = "auth_obj"

    execute_result = MagicMock()
    execute_result.scalars.return_value = scalars_mock

    db.execute.return_value = execute_result
    result = await repo.get_refresh_token("token")

    assert result == "auth_obj"

    db.execute.assert_awaited()
