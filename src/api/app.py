from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import connection
from routes import todo_router, user_router, auth_router
from utils import Logger

_logger = Logger(logger_name=__name__)._get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        connection
        yield
    except Exception as e:
        _logger.error(
            "Database connection cannot be stablised | Error: %s",
            str(e)
        )
        connection.rollback()
        raise f"Error caught on datbase connection: {e}"
    finally:
        connection.close()


app = FastAPI(title="FastAPI Template", version="1.0.0", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(todo_router)
app.include_router(user_router)


@app.get("/", status_code=200, tags=["Health Check"])
async def health_check():
    _logger.info(
        "Health check endpoint called"
    )
    return {"State": "Application running"}
