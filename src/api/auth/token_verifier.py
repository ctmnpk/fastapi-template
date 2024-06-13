from fastapi import Header, HTTPException
from typing import Annotated

from auth import TokenHandler
from utils import Logger

_logger = Logger(__name__)


class TokenVerifier:
    def token_verifier(token: Annotated[str, Header(...)]) -> None:
        signed_token = TokenHandler().token_decoder(token=token)
        if not type(signed_token) == dict:
            _logger.warning(
                f"Header token unsigned or unknown encoding: {token}"
            )
            raise HTTPException(status_code=401, detail="Unauthorized token")

    def key_verifier(key: Annotated[str, Header(...)]) -> None:
        if key != "access_token":
            _logger.warning(f"Unprocessable header key: {key}")
            raise HTTPException(
                status_code=400, detail="Missing or unexpected key passed"
            )
