from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException, FastAPIError
from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError

from typing import Annotated

from auth import CredentialsBearer
from database import connection, Users
from models.schemas import UserResponse, UserUpdateRequest
from utils import Logger

user_router = APIRouter(prefix="/api/v1/user", tags=["User"])

_logger = Logger(logger_name=__name__)._get_logger()


@user_router.get("/", response_model=UserResponse)
async def profile(
    credentials: Annotated[dict, "Credentials"] = Depends(CredentialsBearer())
):
    _logger.info("User profile route call")
    _user_id = credentials.get("sub")
    try:
        query = (
            select(Users)
            .where(
                Users.id == _user_id
            )
        )
        user_profile = connection.execute(query).fetchone()
        if not user_profile:
            _logger.info("User profile not found")
            raise HTTPException(
                status_code=404, detail="Requested user not found"
            )
        return user_profile
    except SQLAlchemyError as e:
        connection.rollback()
        _logger.error(
            "SQLAlchemy Error while searching for user: %s | Error: %s",
            _user_id,
            str(e)
        )
        raise HTTPException(
            status_code=400, detail="Transaction couldn't be completed"
        )
    except FastAPIError as e:
        _logger.warning("Server error: %s", str(e))
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")



@user_router.put("/")
async def update_user(
    user: UserUpdateRequest,
    credentials: Annotated[dict, "Credentials"] = Depends(CredentialsBearer())
):
    _logger.info("User update call")
    _user_id = credentials.get("sub")
    try: 
        query = (
            update(Users)
            .where(Users.id == _user_id)
            .values(
                username=user.username,
                email=user.email,
                password=user.password,
                name=user.name
            )
        )
        connection.execute(query)
        connection.commit()
        _logger.info("User updated successfully: %s", user.username)
        return "User updated"
    except SQLAlchemyError as e:
        connection.rollback()
        _logger.error(
            "SQLAlchemy Error while updating user: %s | Error: %s",
            _user_id,
            str(e)
        )
        raise HTTPException(
            status_code=400, detail="Transaction couldn't be completed"
        )
    except FastAPIError as e:
        _logger.warning("Server error: %s", str(e))
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@user_router.delete("/")
async def delete_user(
    credentials: Annotated[dict, "Credentials"] = Depends(CredentialsBearer())
):
    _logger.info("User delete call")
    _user_id = credentials.get("sub")
    try:
        query = (
            delete(Users)
            .where(Users.id == _user_id)
        )
        connection.execute(query)
        connection.commit()
        _logger.info("User deleted successfully: %s", _user_id)
        return "User deleted"
    except SQLAlchemyError as e:
        connection.rollback()
        _logger.error(
            "SQLAlchemy Error while deleting user: %s | Error: %s",
            _user_id,
            str(e)
        )
        raise HTTPException(
            status_code=400, detail="Transaction couldn't be completed"
        )
    except FastAPIError as e:
        _logger.warning("Server error: %s", str(e))
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
