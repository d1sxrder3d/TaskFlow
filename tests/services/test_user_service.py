import pytest
from unittest.mock import AsyncMock, MagicMock
from src.rest_api.app.api.v1.users.service import UserService

@pytest.mark.asyncio
async def test_get_user_by_id():
    repo = AsyncMock()
    repo.get.return_value = MagicMock(id=1)
    service = UserService(repo)
    user = await service.get_user_by_id(1)
    assert user.id == 1
    repo.get.assert_awaited_with(1)

@pytest.mark.asyncio
async def test_get_user_by_username():
    repo = AsyncMock()
    repo.get_by_username.return_value = MagicMock(username="test")
    service = UserService(repo)
    user = await service.get_user_by_username("test")
    assert user.username == "test"
    repo.get_by_username.assert_awaited_with("test")

@pytest.mark.asyncio
async def test_get_user_by_email():
    repo = AsyncMock()
    repo.get_by_email.return_value = MagicMock(email="test@example.com")
    service = UserService(repo)
    user = await service.get_user_by_email("test@example.com")
    assert user.email == "test@example.com"
    repo.get_by_email.assert_awaited_with("test@example.com")
