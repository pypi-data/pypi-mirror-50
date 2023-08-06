try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    SQL_ALCHEMY_INSTALLED = 1
except ImportError:
    SQL_ALCHEMY_INSTALLED = 0
from pydantic import BaseSettings
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from ..exceptions import MissingDependencyError


class SQLDatabaseConfig(BaseSettings):
    uri: str = "sqlite:///example.db"

    class Config:
        env_prefix = "APP_SQL_"
        case_insensitive = True


database_config = SQLDatabaseConfig()


def set_sql(app: FastAPI) -> None:
    """
    Set up a database connection to a FastAPI application.
    It also defines a middleware that injects database connection into requests
    """
    if SQL_ALCHEMY_INSTALLED == 0:
        raise MissingDependencyError(
            missing_package="sqlachemy", extra="sql|mysql|postgres"
        )

    db_engine = create_engine(database_config.uri)
    Session = sessionmaker(bind=db_engine)

    @app.middleware("http")
    async def sql_session_middleware(request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        request.state.sql = Session()

        response = await call_next(request)
        return response
