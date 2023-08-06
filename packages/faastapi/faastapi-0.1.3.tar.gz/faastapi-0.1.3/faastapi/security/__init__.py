from fastapi import FastAPI, Depends
from .basic_auth import set_basic_auth, User
from .cors import set_cors
from .oauth2_password_bearer import set_oauth2


def set_no_auth(app: FastAPI) -> FastAPI:
    """
    Set no authentication to application. I.E, /users/me will always return "guest".
    """

    def default_get_user():
        return User(username="guest")

    @app.get("/users/me")
    def read_current_user(current_user: User = Depends(default_get_user)):
        return current_user

    return app, default_get_user
