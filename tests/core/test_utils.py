import pytest
from src.rest_api.app.core.utils import dev_only
from src.rest_api.app.core.config import settings

def test_dev_only_decorator_dev(monkeypatch):
    monkeypatch.setattr(settings, "debug_mode", "dev")
    @dev_only
    def foo():
        return 42
    assert foo() == 42

def test_dev_only_decorator_prod(monkeypatch):
    monkeypatch.setattr(settings, "debug_mode", "prod")
    @dev_only
    def foo():
        return 42
    with pytest.raises(RuntimeError):
        foo()

