import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.rest_api.app.api.v1.auth.service import AuthService

@pytest.mark.asyncio
async def test_authenticate_user_success():
    user = MagicMock(is_active=True, hashed_password=b"hash")
    repo = AsyncMock()

    repo.get_by_username.return_value = user
    repo.get_by_email.return_value = None

    with patch("src.rest_api.app.api.v1.auth.service.validate_password", return_value=True):
        service = AuthService(AsyncMock(), repo)
        result = await service.authenticate_user("test", "password")
        assert result is user

@pytest.mark.asyncio
async def test_authenticate_user_fail():
    repo = AsyncMock()
    repo.get_by_username.return_value = None
    repo.get_by_email.return_value = None

    service = AuthService(AsyncMock(), repo)

    result = await service.authenticate_user("notfound", "password")

    assert result is None
