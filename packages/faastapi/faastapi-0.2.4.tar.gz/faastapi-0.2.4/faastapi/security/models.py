from typing import List, Union, Optional
from pydantic import BaseSettings, BaseModel


DEFAULTS_CORS_ORIGIN = [
    "http://localhost.com",
    "https://localhost.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:5000",
]


class JWTConfig(BaseSettings):
    # to get a string like this run:
    # openssl rand -hex 32
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_prefix = "APP_JWT_"
        case_insensitive = True


class CORSConfig(BaseSettings):
    allow_origins: List[str] = DEFAULTS_CORS_ORIGIN
    allow_credentials: bool = True
    allow_methods: List[str] = ["*"]
    allow_headers: List[str] = ["*"]


class BasicAuthConfig(BaseSettings):
    username: str = "admin"
    password: Union[str, bytes] = "secret"

    class Config:
        env_prefix = "APP_BASIC_AUTH_"
        case_insensitive = True


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
