from typing import List, Callable
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseSettings


DEFAULTS_ORIGIN = [
    "http://localhost.com",
    "https://localhost.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:5000",
]


class CORSConfig(BaseSettings):
    allow_origins: List[str] = DEFAULTS_ORIGIN
    allow_credentials: bool = True
    allow_methods: List[str] = ["*"]
    allow_headers: List[str] = ["*"]


cors_config = CORSConfig()


def set_cors(app: FastAPI) -> Callable:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_config.allow_origins,
        allow_credentials=cors_config.allow_credentials,
        allow_methods=cors_config.allow_methods,
        allow_headers=cors_config.allow_headers,
    )
