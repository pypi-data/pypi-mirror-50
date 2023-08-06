try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
except ImportError:
    raise ImportError(
        "Package 'sqlalchemy' is not installed."
        "You can install it using the following command:"
        "  'pip install faastapi[sql]'"
    )
from pydantic import BaseSettings
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response


class SQLDatabaseConfig(BaseSettings):
    uri: str = "sqlite:///example.db"

    class Config:
        env_prefix = "SQL_"
        case_insensitive = True


database_config = SQLDatabaseConfig()
db_engine = create_engine(database_config.uri)
Session = sessionmaker(bind=db_engine)


def set_sql(app: FastAPI) -> None:
    """
    Set up a database connection to a FastAPI application.
    It also defines a middleware that injects database connection into requests
    """

    @app.middleware("http")
    async def sql_session_middleware(request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        request.state.sql = Session()

        response = await call_next(request)
        return response
