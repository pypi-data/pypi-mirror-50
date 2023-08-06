try:
    from databases import Database
except ImportError:
    raise ImportError(
        "Package 'databases' is not installed. "
        "You can install it one of the following command:\n"
        "  - pip install faastapi[postgres]\n"
        "  - pip install faastapi[sqlite]\n"
        "  - pip install faastapi[mysql]\n"
    )
from pydantic import BaseSettings
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response


class AsyncSQLDatabaseConfig(BaseSettings):
    uri: str = "sqlite:///example.db"

    class Config:
        env_prefix = "ASYNC_SQL_"
        case_insensitive = True


database_config = AsyncSQLDatabaseConfig()
database = Database(database_config.uri)


def set_async_sql(app: FastAPI) -> None:
    """
    Set up a database connection to a FastAPI application.
    It also defines a middleware that injects database connection into requests
    """

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
