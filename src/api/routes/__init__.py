# Package metadata
__version__ = "1.0.0"
__author__ = "ctmnpk"


# Packge modules, submodules and functions importing
from .auth_routes import auth_router
from .todo_routes import todo_router
from .user_routes import user_router


# Defined importing for '*' wildcard
__all__ = ["auth_router", "todo_router", "user_router"]
