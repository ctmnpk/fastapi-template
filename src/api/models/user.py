from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, SecretStr

class Role(Enum):
    COMMONER = 1
    IT = 2
    ADMIN = 3

class User(BaseModel):
    _id: UUID # -> private field
    username: str
    password: SecretStr
    email: EmailStr
    _authenticator: str = None # -> private field
    created_at: datetime = datetime.now()
    role: Role = Role.COMMONER
