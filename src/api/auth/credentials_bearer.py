from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .token_decoder import TokenDecoder

_decoder = TokenDecoder()


class CredentialsBearer(HTTPBearer):
    """
    CredentialsBearer is a subclass of HTTPBearer used to handle Bearer token authentication.
    
    Attributes:
    -----------
    `auto_error` : bool
        Indicates whether to automatically raise an error on authentication failure.
    
    Methods:
    --------
    __init__(auto_error=True):
        Initializes the CredentialsBearer with the option to automatically raise errors.
    
    __call__(request: Request) -> dict:
        Asynchronously processes an HTTP request to validate Bearer token credentials.
    """
    def __init__(self, auto_error=True):
        """
        Initializes the CredentialsBearer instance.
        
        Parameters:
        -----------
        `auto_error` : bool, optional
            If True, automatically raises an HTTPException on authentication failure (default is False).
        """
        super(CredentialsBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        """
        Asynchronously processes an HTTP request to validate Bearer token credentials.
        
        Parameters:
        -----------
        `request` : Request
            The incoming HTTP request to be authenticated.
        
        Returns:
        --------
        `dict`
            The decoded credentials if authentication is successful.
        
        Raises:
        -------
        HTTPException
            If the request is missing credentials, the scheme is incorrect, or the credentials are invalid.
        """
        credentials: HTTPAuthorizationCredentials = await super(
                                                            CredentialsBearer, 
                                                            self).__call__(
                                                                    request)
        if not credentials:
            raise HTTPException(status_code=403, 
                                detail="Request missing credentials")
        if credentials.scheme != "Bearer":
            raise HTTPException(status_code=403, 
                                detail="Request scheme missing or incorrect")
        decoded_credentials = _decoder(token=credentials.credentials)
        if not decoded_credentials:
            raise HTTPException(status_code=401,
                                detail="Request with unacknowledged credentials")
        return decoded_credentials
