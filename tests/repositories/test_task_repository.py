import pytest
from unittest.mock import AsyncMock, MagicMock
from src.rest_api.app.repositories.task import TaskRepository

@pytest.mark.asyncio
async def test_get_by_user():
    db = AsyncMock()
    repo = TaskRepository(db)
    scalars_mock = MagicMock()
    scalars_mock.all.return_value = ["task1", "task2"]
    execute_result = MagicMock()
    execute_result.scalars.return_value = scalars_mock
    db.execute.return_value = execute_result
    result = await repo.get_by_user(1)
    assert result == ["task1", "task2"]
    db.execute.assert_awaited()

@pytest.mark.asyncio
async def test_get_by_tag():
    db = AsyncMock()
    repo = TaskRepository(db)
    scalars_mock = MagicMock()
    scalars_mock.all.return_value = ["task3"]
    execute_result = MagicMock()
    execute_result.scalars.return_value = scalars_mock
    db.execute.return_value = execute_result
    result = await repo.get_by_tag(2)
    assert result == ["task3"]
    db.execute.assert_awaited()
