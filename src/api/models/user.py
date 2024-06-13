from datetime import datetime
import enum

from pydantic import BaseModel, EmailStr, SecretStr, PrivateAttr, Field
from typing import Annotated, Optional

class Role(enum.Enum):
    COMMONER = 1
    IT = 2
    ADMIN = 3

class UserRequest(BaseModel):
    username: Optional[Annotated[str, "Username"]] = None
    password: str
    email: EmailStr

class UserResponse(BaseModel):
    _id: int = PrivateAttr() # -> private field
    username: Optional[Annotated[str, "Username"]] = None
    password: SecretStr
    email: EmailStr
    created_at: datetime = datetime.now()
    role: Role = Field(default=Role.COMMONER)

    def __init__(self, **data):
        super().__init__(**data)
        self._id = data.get('_id')
