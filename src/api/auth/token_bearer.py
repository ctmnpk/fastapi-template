from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .token_handler import TokenHandler

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(TokenBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
                                                        TokenBearer, 
                                                        self
                                                    ).__call__(request)
        
        if not credentials:
            return HTTPException(status_code=403, 
                                detail='Credentials missing')
        
        if credentials.scheme != 'Bearer':
            return HTTPException(status_code=403, 
                                detail='Invalid credential scheme')
        return credentials.credentials
        
    def token_verifier(self, token: str) -> bool:
        is_token_valid = TokenHandler().token_decoder(token) 
        return True if is_token_valid else False
