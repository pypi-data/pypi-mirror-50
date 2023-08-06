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

    class Config:
        case_insensitive = True
        env_prefix = "APP_"


class QuickFastAPI(FastAPI):

    settings = AppSettings

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.configuration = self.settings()
        self.get_user = None
        self.users_db = None

    def configure(self, users_db: Dict[str, dict] = DEFAULT_USERS_DB):
        """
        Configure application
        """
        if self.configuration.cors_enabled:
            set_cors(self)
            logger.info("Enabled CORS policy")
        if self.configuration.instrumentation_enabled:
            set_process_time_headers(self)
            logger.info("Enabled instrumentation middleware")
        if self.configuration.mongodb_enabled:
            set_mongodb(self)
            logger.info("Enabled mongodb plugin")
        if self.configuration.sql_enabled:
            set_sql(self)
            logger.info("Enabled sql plugin")
        if self.configuration.async_sql_enabled:
            set_async_sql(self)
            logger.info("Enabled async sql plugin")
        # OAUTH2 has priority over basic auth
        if (
            self.configuration.basic_auth_enabled
            and not self.configuration.oauth2_auth_enabled
        ):
            self.get_user = Depends(set_basic_auth(self))
            logger.info("Enabled basic authentication plugin")
        elif self.configuration.oauth2_auth_enabled:
            self.get_user = Depends(set_oauth2(self, users_db=users_db))
            logger.info("Enabled oauth2 authentication plugin")
        else:
            logger.info("Disabled authentication")
            self.get_user = Depends(set_no_auth(self))
        logger.info("Finished configuring application")
