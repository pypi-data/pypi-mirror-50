from typing import Callable
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .models import CORSConfig


cors_config = CORSConfig()


def set_cors(app: FastAPI) -> Callable:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_config.allow_origins,
        allow_credentials=cors_config.allow_credentials,
        allow_methods=cors_config.allow_methods,
        allow_headers=cors_config.allow_headers,
    )
