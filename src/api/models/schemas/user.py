from pydantic import BaseModel, EmailStr
from typing import Annotated, Optional

from models.enums import Gender


class UserBase(BaseModel):
    username: Optional[Annotated[str, "Username"]] = None
    email: Optional[Annotated[EmailStr, "Email"]] = None
    password: Annotated[str, "Password"]


class UserSignInRequest(UserBase):
    pass


class UserSignUpRequest(UserBase):
    name: Annotated[str, "Name"]
    age: Annotated[int, "Age"]
    gender: Annotated[Gender, "Gender"]


class UserUpdateRequest(UserBase):
    pass


class UserResponse(UserBase):
    name: Annotated[str, "Name"]
    age: Annotated[int, "Age"]
    gender: Annotated[Gender, "Gender"]
