from fastapi import APIRouter, HTTPException
from sqlalchemy import and_, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from auth import TokenHandler
from models import UserRequest
from utils import Logger
from migrations import connection, Users

_logger = Logger(logger_name=__name__)

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@auth_router.post("/signin")
async def signin(user: UserRequest):
    _logger.info("SignIn service called")
    try:
        query = select(Users).where(
            and_(
                or_(Users.email == user.email, Users.username == user.username),
                Users.password == user.password,
            )
        )
        result = connection.execute(query).first()
        if not result:
            raise HTTPException(status_code=400, detail="User not found")
        _logger.info(f"User authenticated {user.username}")
        return TokenHandler().token_encoder(result.id)
    except SQLAlchemyError as e:
        _logger.error(
            f"SQLAlchemy Error during user signin for: {user.username} | error: {str(e)}"
        )
        raise HTTPException(
            status_code=500, detail="Database error during signin"
        )
    except Exception as e:
        _logger.warning(
            f"Unable to complete user signin for: {user.username} | erro: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail="Unable to complete user signin"
        )


@auth_router.post("/signup")
async def signup(user: UserRequest):
    _logger.info("SignUp service called")
    existing_user_criteria = select(Users).where(
        or_(Users.username == user.username, Users.email == user.email)
    )
    try:
        user_exists = connection.execute(existing_user_criteria).fetchone()
        if user_exists:
            raise HTTPException(
                status_code=400,
                detail="User with the same username or email already exists",
            )
        query = insert(Users).values(
            username=user.username, password=user.password, email=user.email
        )
        connection.execute(query)
        connection.commit()
        _logger.info(f"User created: {user.username}")
        return "User created"
    except SQLAlchemyError as e:
        _logger.error(
            f"SQLAlchemy Error during user signin for: {user.username} | Error: {str(e)}"
        )
        connection.rollback()
        raise HTTPException(
            status_code=500, detail="Database error during signup"
        )
    except Exception as e:
        _logger.warning(
            f"Unable to complete user signup for: {user.username} | Error: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail="Unable to complete user signup"
        )
