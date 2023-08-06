from typing import Optional
from sqlalchemy.orm.session import Session
from starlette.requests import Request
from pymongo.database import Database as MongoDatabase
from databases import Database as AsyncSQLDatabase
from pydantic import BaseModel
from fastapi import Depends


class Context(BaseModel):
    mongodb: Optional[MongoDatabase] = None
    sql: Optional[Session] = None
    async_sql: Optional[AsyncSQLDatabase] = None

    class Config:
        arbitrary_types_allowed = True


def __get_context__(request: Request):
    mongodb = None
    try:
        mongodb = request.state.mongodb
    except AttributeError:
        pass
    async_sql = None
    try:
        async_sql = request.state.async_sql
    except AttributeError:
        pass
    sql = None
    try:
        sql = request.state.sql
    except AttributeError:
        pass
    return Context(mongodb=mongodb, sql=sql, async_sql=async_sql)


get_context = Depends(__get_context__)
