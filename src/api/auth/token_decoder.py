from jwt import decode
from jwt.exceptions import ExpiredSignatureError, DecodeError

from .configuration_handler import ConfigurationHandler
from utils import Logger


_logger = Logger(logger_name=__name__)._get_logger()


class TokenDecoder(ConfigurationHandler):
    """
    TokenDecoder is a class that extends ConfigurationHandler to provide functionality for decoding JWT tokens.
    
    Methods:
    --------
    __init__():
        Initializes the TokenDecoder instance.
        
    __repr__() -> str:
        Returns a string representation of the TokenDecoder instance.
    
    __call__(token: str) -> dict:
        Attempts to decode a JWT token and return its payload.
    """
    def __init__(self):
        """
        Initializes the TokenDecoder instance.
        
        Inherits the initialization from the ConfigurationHandler class,
        which sets up the necessary configuration values.
        """
        super().__init__()

    def __call__(self, token: str) -> dict:
        """
        Attempts to decode a JWT token.
        
        Args:
        -----
        `token` : str
            The JWT token to decode.
        
        Returns:
        --------
        `dict`
            The decoded token payload if successful, None if an error occurs.
        
        Raises:
        -------
        `Log`
            Errors are logged with specifics of the token and error.
        """
        try:
            return decode(token, self.secret, algorithms=[self.algorithm])
        except ExpiredSignatureError as e:
            _logger.warning(
                "Decoded expired token: %s | Error: %s",
                token,
                str(e)
            )
        except DecodeError as e:
            _logger.warning(
                "Error while trying to decode token: %s | Error: %s",
                token,
                str(e)
            )