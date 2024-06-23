from fastapi import Depends
from fastapi.exceptions import HTTPException, FastAPIError
from fastapi.routing import APIRouter
from sqlalchemy import delete, insert, select, update, and_
from sqlalchemy.exc import SQLAlchemyError

from typing import Annotated

from auth import CredentialsBearer
from database import connection, Todos
from models.schemas import TodoCreateRequest, TodoResponse, TodoUpdateRequest
from utils import Logger

_logger = Logger(logger_name=__name__)._get_logger()


todo_router = APIRouter(prefix="/api/v1/todo", tags=["To-Do"])


@todo_router.post("/")
async def create_todo(
    todo: TodoCreateRequest,
    credentials: Annotated[dict, "Credentials"] = Depends(CredentialsBearer()),
):
    _logger.info("Todo create route called")
    _user_id = credentials.get("sub")
    try:
        query = (
            insert(Todos)
            .values(
                title=todo.title,
                description=todo.description,
                dead_line=todo.dead_line,
                priority=todo.priority,
                user_id=_user_id,
            )
        )
        connection.execute(query)
        connection.commit()
        return "Todo created"
    except SQLAlchemyError as e:
        connection.rollback()
        _logger.error(
            "SQLAlchemy Error while to-do creation | Error: %s", str(e)
        )
        raise HTTPException(
            status_code=400, detail="Transaction couldn't be completed"
        )
    except FastAPIError as e:
        _logger.warning("Server error: %s", str(e))
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@todo_router.get("/{todo_id}", response_model=TodoResponse)
async def read_single_todo(
    todo_id: Annotated[int, "Todo Id query parameter"],
    credentials: Annotated[dict, "Credentials"] = Depends(CredentialsBearer()),
):
    _logger.info("Todo read single item call")
    _user_id = credentials.get("sub")
    try:
        query = (
            select(
                Todos.title, Todos.description, Todos.dead_line,
                Todos.priority, Todos.created_at, Todos.id
            )
            .where(
                and_(Todos.id == todo_id, Todos.user_id == _user_id)
            )
        )
        specific_todo = connection.execute(query).fetchone()
        if specific_todo is None:
            _logger.info("Specified to-do not found: %s", todo_id)
            raise HTTPException(
                status_code=404, detail="Requested todo not found"
            )
        return specific_todo
    except SQLAlchemyError as e:
        connection.rollback()
        _logger.error(
            "SQLAlchemy Error while searching to-do | Error: %s", str(e)
        )
        raise HTTPException(
            status_code=400, detail="Transaction couldn't be completed"
        )
    except FastAPIError as e:
        _logger.warning("Unexpected server error: %s", str(e))
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@todo_router.get("/", response_model=list[TodoResponse])
async def read_all_todos(
    credentials: Annotated[dict, "Credentials"] = Depends(CredentialsBearer()),
):
    _logger.info("Todo read all call")
    _user_id = credentials.get("sub")
    try:
        query = (
            select(Todos)
            .where(
                Todos.user_id == _user_id
            )
        )
        all_user_todos = connection.execute(query).fetchall()
        return all_user_todos
    except SQLAlchemyError as e:
        connection.rollback()
        _logger.error(
            "SQLAlchemy Error while retrieving all to-do's | Error: %s", str(e)
        )
        raise HTTPException(
            status_code=400, detail="Transaction couldn't be completed"
        )
    except FastAPIError as e:
        _logger.warning("Unexpected server error: %s", str(e))
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@todo_router.put("/{todo_id}")
async def update_todo(
    todo_id: Annotated[int, "Todo Id query parameter"],
    todo: Annotated[TodoUpdateRequest, "Todo body"],
    credentials: Annotated[dict, "Credentials"] = Depends(CredentialsBearer()),
):
    _logger.info("Todo update call")
    _user_id = credentials.get("sub")
    try:
        query = (
            update(Todos)
            .where(Todos.id == todo_id, Todos.user_id == _user_id)
            .values(
                title=todo.title,
                description=todo.description,
                dead_line=todo.dead_line,
                priority=todo.priority,
            )
        )
        connection.execute(query)
        connection.commit()
        _logger.info("Todo updated: %s", todo_id)
        return "Todo updated"
    except SQLAlchemyError as e:
        connection.rollback()
        _logger.error(
            "SQLAlchemy Error while updating to-do | Error: %s", str(e)
        )
        raise HTTPException(
            status_code=400, detail="Transaction couldn't be completed"
        )
    except FastAPIError as e:
        _logger.warning("Server error: %s", str(e))
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@todo_router.delete("/{todo_id}")
async def delete_todo(
    todo_id: Annotated[int, "Todo Id query parameter"],
    credentials: Annotated[dict, "Credentials"] = Depends(CredentialsBearer()),
):
    _logger.info("Todo delete call")
    _user_id = credentials.get("sub")
    try:
        query = (
            delete(Todos)
            .where(
                and_(Todos.id == todo_id, Todos.user_id == _user_id)
            )
        )
        connection.execute(query)
        connection.commit()
        _logger.info("Todo deleted: %s", todo_id)
        return "Todo deleted"
    except SQLAlchemyError as e:
        connection.rollback()
        _logger.error(
            "SQLAlchemy Error while deleting to-do | Error: %s", str(e)
        )
        raise HTTPException(
            status_code=400, detail="Transaction couldn't be completed"
        )
    except FastAPIError as e:
        _logger.warning("Unexpected server error: %s", str(e))
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
