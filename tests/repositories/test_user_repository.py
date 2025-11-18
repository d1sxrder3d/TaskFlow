import pytest
from unittest.mock import AsyncMock, MagicMock
from src.rest_api.app.repositories.user import UserRepository


@pytest.mark.asyncio
async def test_get_by_username():
    db = AsyncMock()
    repo = UserRepository(db)

    scalars_mock = MagicMock()
    scalars_mock.first.return_value = "user_obj"

    execute_result = MagicMock()
    execute_result.scalars.return_value = scalars_mock

    db.execute.return_value = execute_result
    result = await repo.get_by_username("test")

    assert result == "user_obj"

    db.execute.assert_awaited()


@pytest.mark.asyncio
async def test_get_by_email():
    db = AsyncMock()
    repo = UserRepository(db)

    scalars_mock = MagicMock()
    scalars_mock.first.return_value = "user_obj"

    execute_result = MagicMock()
    execute_result.scalars.return_value = scalars_mock

    db.execute.return_value = execute_result
    result = await repo.get_by_email("test@example.com")

    assert result == "user_obj"

    db.execute.assert_awaited()

@pytest.mark.asyncio
async def test_get_by_organization():
    db = AsyncMock()
    repo = UserRepository(db)

    scalars_mock = MagicMock()
    scalars_mock.all.return_value = ["user1", "user2"]

    execute_result = MagicMock()
    execute_result.scalars.return_value = scalars_mock

    db.execute.return_value = execute_result
    result = await repo.get_by_organization(42)

    assert result == ["user1", "user2"]

    db.execute.assert_awaited()

@pytest.mark.asyncio
async def test_get_by_project():
    db = AsyncMock()
    repo = UserRepository(db)

    scalars_mock = MagicMock()
    scalars_mock.all.return_value = ["user1"]

    execute_result = MagicMock()
    execute_result.scalars.return_value = scalars_mock

    db.execute.return_value = execute_result

    result = await repo.get_by_project(99)

    assert result == ["user1"]

    db.execute.assert_awaited()

@pytest.mark.asyncio
async def test_get_by_task():
    db = AsyncMock()
    repo = UserRepository(db)

    scalars_mock = MagicMock()
    scalars_mock.all.return_value = ["user3"]

    execute_result = MagicMock()
    execute_result.scalars.return_value = scalars_mock

    db.execute.return_value = execute_result

    result = await repo.get_by_task(7)

    assert result == ["user3"]

    db.execute.assert_awaited()
