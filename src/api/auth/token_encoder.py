from datetime import datetime, timedelta

from jwt import encode

from .configuration_handler import ConfigurationHandler
from models.enums import Role


class TokenEncoder(ConfigurationHandler):
    """
    TokenEncoder is a class that extends ConfigurationHandler to provide functionality for encoding JWT tokens.
    
    Methods:
    --------
    __init__():
        Initializes the TokenEncoder instance.
        
    __repr__() -> str:
        Returns a string representation of the TokenEncoder instance.
    
    __call__(_user_id: int, role: Role) -> str:
        Encodes a payload into a JWT token.
    """
    def __init__(self):
        super().__init__()

    def __call__(self, _user_id: int, role: Role) -> str:
        """
        Encodes a payload into a JWT token.
        
        Args:
        -----
        `_user_id` : int
            The user ID to include in the token payload.
        `role` : Role
            The user's role, an instance of the Role enum.
        
        Returns:
        --------
        `str`
            The encoded JWT token as a string.
        """
        payload = {
            "exp": datetime.now() + timedelta(seconds=3600),
            "sub": _user_id,
            "role": role.value
        }
        return encode(payload, self.secret, self.algorithm)