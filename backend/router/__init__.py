from .books import router as books
from .users import router as users
from .user_auth import router as user_auth
from .genre import router as genre

__all__ = [
    "books",
    "users",
    "user_auth",
    "genre"
]