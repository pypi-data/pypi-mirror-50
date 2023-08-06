from typing import Dict
from fastapi import FastAPI, Depends
from pydantic import BaseSettings
from .security import set_cors, set_basic_auth, set_oauth2, set_no_auth
from .security.oauth2_password_bearer import USERS_DB as DEFAULT_USERS_DB
from .instrumentation import set_process_time_headers
from .databases import set_mongodb, set_sql, set_async_sql
from .logger import logger


class AppSettings(BaseSettings):
    cors_enabled: bool = True
    basic_auth_enabled: bool = True
    oauth2_auth_enabled: bool = False
    instrumentation_enabled: bool = False
    mongodb_enabled: bool = False
    sql_enabled: bool = False
    async_sql_enabled: bool = False
    enable_openfaas: bool = True

    class Config:
        case_insensitive = True
        env_prefix = "APP_"


class FaastAPI(FastAPI):

    settings = AppSettings

    def __init__(self, **kwargs):
        """
        Return a new instance of Q
        """
        self.configuration = self.settings()
        if self.configuration.enable_openfaas:
            openapi_prefix = "/function/demo-faastapi"
        else:
            openapi_prefix = ""
        super().__init__(openapi_prefix=openapi_prefix, **kwargs)
        self.get_user = None
        self.users_db = None

    def configure(self, users_db: Dict[str, dict] = DEFAULT_USERS_DB):
        """
        Configure application
        """
        if self.configuration.cors_enabled:
            logger.info("Enabling CORS policy")
            set_cors(self)
        if self.configuration.instrumentation_enabled:
            logger.info("Enabling instrumentation middleware")
            set_process_time_headers(self)
        if self.configuration.mongodb_enabled:
            logger.info("Enabling mongodb plugin")
            set_mongodb(self)
        if self.configuration.sql_enabled:
            logger.info("Enabling sql plugin")
            set_sql(self)
        if self.configuration.async_sql_enabled:
            logger.info("Enabling async sql plugin")
            set_async_sql(self)
        # OAUTH2 has priority over basic auth
        if (
            self.configuration.basic_auth_enabled
            and not self.configuration.oauth2_auth_enabled
        ):
            logger.info("Enabling basic authentication plugin")
            self.get_user = Depends(set_basic_auth(self))
        elif self.configuration.oauth2_auth_enabled:
            logger.info("Enabling oauth2 authentication plugin")
            self.get_user = Depends(set_oauth2(self, users_db=users_db))
        else:
            logger.info("Disabling authentication")
            self.get_user = Depends(set_no_auth(self))
        logger.info("Finished configuring application")
