from typing import Union, Callable
from pydantic import BaseSettings, BaseModel
from fastapi import Depends, HTTPException, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED


class BasicAuthConfig(BaseSettings):
    username: str = "admin"
    password: Union[str, bytes] = "secret"

    class Config:
        env_prefix = "BASIC_AUTH"
        case_insensitive = True


security = HTTPBasic()
basic_auth_config = BasicAuthConfig()


class User(BaseModel):
    username: str


def set_basic_auth(app: FastAPI) -> Callable:
    """
    Set basic authentication to application and return function
    to get current user
    """

    def get_current_active_user(credentials: HTTPBasicCredentials = Depends(security)):
        if (
            credentials.username != basic_auth_config.username
            or credentials.password != basic_auth_config.password
        ):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        return User(username=credentials.username)

    @app.get("/users/me")
    def read_current_user(current_user: User = Depends(get_current_active_user)):
        return current_user

    return get_current_active_user
