import pytest
from unittest.mock import AsyncMock, MagicMock
from src.rest_api.app.repositories.organization import OrganizationRepository

@pytest.mark.asyncio
async def test_get_by_owner_id():
    db = AsyncMock()
    repo = OrganizationRepository(db)
    scalars_mock = MagicMock()
    scalars_mock.all.return_value = ["org1", "org2"]
    execute_result = MagicMock()
    execute_result.scalars.return_value = scalars_mock
    db.execute.return_value = execute_result
    result = await repo.get_by_owner_id(1)
    assert result == ["org1", "org2"]
    db.execute.assert_awaited()
