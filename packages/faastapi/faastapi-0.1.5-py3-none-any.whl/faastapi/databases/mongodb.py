try:
    from pymongo import MongoClient

    PYMONGO_INSTALLED = 1
except ImportError:
    PYMONGO_INSTALLED = 0
from pydantic import BaseSettings
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from ..exceptions import MissingDependencyError


class MongoDBConfig(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 27017
    database: str = "test"

    class Config:
        env_prefix = "MONGODB_"
        case_insensitive = True


mongodb_config = MongoDBConfig()


def set_mongodb(app: FastAPI) -> None:
    """
    Set up a middleware that injects a MongoDB database object
    into each request
    """
    if PYMONGO_INSTALLED == 0:
        raise MissingDependencyError("pymongo", "mongodb")

    client = MongoClient(host=mongodb_config.host, port=mongodb_config.port)
    db = client[mongodb_config.database]

    @app.middleware("http")
    async def mongodb_session_middleware(request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        request.state.mongodb = db
        response = await call_next(request)
        return response
