from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException, FastAPIError
from sqlalchemy import and_, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from auth import TokenEncoder
from models.schemas import UserSignInRequest, UserSignUpRequest
from utils import Logger
from database import connection, Users

_logger = Logger(logger_name=__name__)._get_logger()

_encoder = TokenEncoder()

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@auth_router.post("/signin")
async def signin(user: UserSignInRequest):
    _logger.info("SignIn route called")
    identifier = check_for_username_or_email(user=user)
    try:
        query = select(Users).where(
            or_(
                and_(
                    Users.username == user.username,
                    Users.password == user.password,
                ),
                and_(
                    Users.email == user.email,
                    Users.password == user.password
                ),
            )
        )
        user_info = connection.execute(query).first()
        if not user_info:
            _logger.info("User not found or not exists: %s", identifier())
            raise HTTPException(status_code=404, detail="User not found")
        _logger.info("User authenticated: %s", identifier())
        return _encoder(user_info.id, user_info.role)
    except SQLAlchemyError as e:
        _logger.error(
            "SQLAlchemy Error during user signin for: %s | Error: %s",
            identifier(),
            str(e)
        )
        raise HTTPException(
            status_code=400, detail="Transaction couldn't be completed"
        )
    except FastAPIError as e:
        _logger.info(
            "Unable to complete user signin for: %s | Erro: %s",
            identifier(),
            str(e)
        )
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@auth_router.post("/signup")
async def signup(user: UserSignUpRequest):
    _logger.info("SignUp route called")
    existing_user_criteria = select(Users).where(
        and_(Users.username == user.username, Users.email == user.email)
    )
    try:
        user_exists = connection.execute(existing_user_criteria).fetchone()
        if user_exists:
            raise HTTPException(
                status_code=400,
                detail="User with the same username or email already exists",
            )
        query = insert(Users).values(
            username=user.username,
            password=user.password,
            email=user.email,
            name=user.name,
            age=user.age,
            gender=user.gender,
        )
        connection.execute(query)
        connection.commit()
        _logger.info("User created: %s", user.username)
        return "User created"
    except SQLAlchemyError as e:
        _logger.error(
            "SQLAlchemy Error during user signin for: %s | Error: %s",
            user.username,
            str(e)
        )
        connection.rollback()
        raise HTTPException(
            status_code=400, detail="Transaction couldn't be completed"
        )
    except FastAPIError as e:
        _logger.info(
            "Unable to complete user signup for: %s | Error: %s",
            user.username,
            str(e)
        )
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


def check_for_username_or_email(user: UserSignInRequest):
    return lambda: user.username if user.username is not None else user.email
