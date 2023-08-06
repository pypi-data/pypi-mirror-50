from starlette.requests import Request
from fastapi import Depends


def __get_context__(request: Request):
    if not hasattr(request.state, "mongodb"):
        request.state.mongodb = None
    if not hasattr(request.state, "async_sql"):
        request.state.async_sql = None
    if not hasattr(request.state, "sql"):
        request.state.sql = None
    return request.state


get_context = Depends(__get_context__)
