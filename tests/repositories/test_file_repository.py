import pytest
from unittest.mock import AsyncMock, MagicMock
from src.rest_api.app.repositories.file import FileRepository

@pytest.mark.asyncio
async def test_get_by_mime_type():
    db = AsyncMock()
    repo = FileRepository(db)
    scalars_mock = MagicMock()
    scalars_mock.all.return_value = ["file1"]
    execute_result = MagicMock()
    execute_result.scalars.return_value = scalars_mock
    db.execute.return_value = execute_result
    result = await repo.get_by_mime_type("image/png")
    assert result == ["file1"]
    db.execute.assert_awaited()

@pytest.mark.asyncio
async def test_get_by_project():
    db = AsyncMock()
    repo = FileRepository(db)
    scalars_mock = MagicMock()
    scalars_mock.all.return_value = ["file2"]
    execute_result = MagicMock()
    execute_result.scalars.return_value = scalars_mock
    db.execute.return_value = execute_result
    result = await repo.get_by_project(1)
    assert result == ["file2"]
    db.execute.assert_awaited()
