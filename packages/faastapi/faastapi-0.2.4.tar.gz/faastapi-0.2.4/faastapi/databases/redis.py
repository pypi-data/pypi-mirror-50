try:
    from redis import Redis
except ImportError:
    REDIS_INSTALLED = 0
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from ..exceptions import MissingDependencyError
from .models import RedisConfig


redis_config = RedisConfig()


def set_redis(app: FastAPI) -> None:
    """
    Set up a middleware that injects a MongoDB database object
    into each request
    """
    if REDIS_INSTALLED == 0:
        raise MissingDependencyError("redis", "redis")

    redis = Redis(host=redis_config.host, port=redis_config.port, db=redis_config.db)

    @app.middleware("http")
    async def redis_session_middleware(request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        request.state.redis = redis
        response = await call_next(request)
        return response
