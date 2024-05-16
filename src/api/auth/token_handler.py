from datetime import datetime, timedelta
from decouple import config
from jwt import encode, decode, ExpiredSignatureError, DecodeError

from .utils.token_generator import create_token

class TokenHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is not None:
            return cls._instance
        cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.secret = config('SECRET')
        self.algorithm = config('ALGORITHM')
    
    def __repr__(self) -> str:
        return f'Token handler instance: {id(self)}'

    def token_encoder(self) -> str:
        payload = {
            "exp" : datetime.now() + timedelta(seconds=3600),
            "session_token" : create_token()
        }
        return encode(payload, self.secret, algorithm=self.algorithm)
    
    def token_decoder(self, token: str) -> dict:
        try:
            return decode(token, self.secret, algorithms=[self.algorithm])
        except ExpiredSignatureError:
            return ValueError('Token expired')
        except DecodeError:
            return ValueError('Error on token decoding')
