from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from routes import auth_router
from migrations import connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        connection
        yield
    except Exception as e:
        connection.rollback()
        raise f'Error caught on datbase connection: {e}'
    finally:
        connection.close()

app = FastAPI(
    title="FastAPI Template",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth_router)

@app.get('/', tags=['Health Check'])
async def state():
    return {"State": "Application running", "Status" : status.HTTP_200_OK}
