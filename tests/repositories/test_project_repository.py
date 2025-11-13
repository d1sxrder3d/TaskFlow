import pytest
from unittest.mock import AsyncMock, MagicMock
from src.rest_api.app.repositories.project import ProjectRepository

@pytest.mark.asyncio
async def test_get_by_organization():
    db = AsyncMock()
    repo = ProjectRepository(db)
    scalars_mock = MagicMock()
    scalars_mock.all.return_value = ["project1", "project2"]
    execute_result = MagicMock()
    execute_result.scalars.return_value = scalars_mock
    db.execute.return_value = execute_result
    result = await repo.get_by_organization(1)
    assert result == ["project1", "project2"]
    db.execute.assert_awaited()
