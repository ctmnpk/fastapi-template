from datetime import datetime, timedelta
from decouple import config
from jwt import encode, ExpiredSignatureError, decode, DecodeError

from utils import Logger

_logger = Logger(__name__)
class TokenHandler:
    def __init__(self):
        self.secret = config("SECRET")
        self.algorithm = config("ALGORITHM")

    def __repr__(self) -> str:
        return f"Token handler instance: {id(self)}"

    def token_encoder(self, _user_id: int) -> str:
        payload = {"exp": datetime.now() 
                    + timedelta(seconds=3600), "sub": _user_id}
        return encode(payload, self.secret, self.algorithm)

    def token_decoder(self, token: str) -> dict:
        try:
            return decode(token, self.secret, algorithms=[self.algorithm])
        except ExpiredSignatureError as e:
            _logger.error(f'Expired token try with token: {token} | Error: {str(e)}')
        except DecodeError as e:
            _logger.error(f'Error while trying to decode token: {token} | Error: {str(e)}')
