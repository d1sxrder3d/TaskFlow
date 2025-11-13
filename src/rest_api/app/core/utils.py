from functools import wraps

from src.rest_api.app.core.config import settings

def dev_only(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if settings.debug_mode not in ("dev", "debug"):
            raise RuntimeError(f"{func.__name__} is blocked in production mode.")
        return func(*args, **kwargs)

    return wrapper