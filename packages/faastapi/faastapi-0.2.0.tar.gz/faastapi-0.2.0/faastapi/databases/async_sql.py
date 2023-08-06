try:
    from databases import Database

    DATABASES_INSTALLED = 1
except ImportError:
    DATABASES_INSTALLED = 0
from pydantic import BaseModel
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from ..exceptions import MissingDependencyError


class AsyncSQLDatabaseConfig(BaseModel):
    uri: str = "sqlite:///example.db"

    class Config:
        env_prefix = "APP_ASYNC_SQL_"
        case_insensitive = True


database_config = AsyncSQLDatabaseConfig()


def set_async_sql(app: FastAPI) -> None:
    """
    Set up a database connection to a FastAPI application.
    It also defines a middleware that injects database connection into requests
    """
    if DATABASES_INSTALLED == 0:
        raise MissingDependencyError(
            "databases", "async-sqlite|async-mysql|async-postgres"
        )

    database = Database(database_config.uri)

    @app.on_event("startup")
    async def connect():
        await database.connect()

    @app.on_event("shutdown")
    async def disconnect():
        await database.disconnect()

    @app.middleware("http")
    async def async_sql_session_middleware(request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        request.state.async_sql = database
        response = await call_next(request)
        return response
