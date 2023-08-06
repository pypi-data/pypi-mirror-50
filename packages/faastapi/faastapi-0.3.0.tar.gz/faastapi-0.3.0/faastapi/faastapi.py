from typing import Dict, Optional
from fastapi import FastAPI, Depends
from pydantic import BaseSettings
from .security import set_cors, set_basic_auth, set_oauth2, set_no_auth
from .instrumentation import set_process_time_headers
from .databases import set_mongodb, set_sql, set_async_sql, set_redis
from .logger import logger


class AppSettings(BaseSettings):
    enable_cors: bool = False
    enable_basic_auth: bool = False
    enable_password_oauth2: bool = False
    enable_instrumentation: bool = False
    enable_mongodb: bool = False
    enable_sql: bool = False
    enable_async_sql: bool = False
    enable_redis: bool = False
    enable_openfaas: bool = True
    openfaas_function: Optional[str] = None

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
            openapi_prefix = f"/function/{self.configuration.openfaas_function}"
            super().__init__(openapi_prefix=openapi_prefix, **kwargs)
        else:
            super().__init__(**kwargs)
        self.get_user = None

    def configure(self, users_db: Optional[Dict[str, dict]] = None):
        """
        Configure application
        """
        if self.configuration.enable_cors:
            logger.info("Enabling CORS policy")
            set_cors(self)
        if self.configuration.enable_instrumentation:
            logger.info("Enabling instrumentation plugin")
            set_process_time_headers(self)
        if self.configuration.enable_mongodb:
            logger.info("Enabling mongodb plugin")
            set_mongodb(self)
        if self.configuration.enable_sql:
            logger.info("Enabling sql plugin")
            set_sql(self)
        if self.configuration.enable_async_sql:
            logger.info("Enabling async sql plugin")
            set_async_sql(self)
        if self.configuration.enable_redis:
            logger.info("Enabling redis plugin")
            set_redis(self)
        # OAUTH2 has priority over basic auth
        if (
            self.configuration.enable_basic_auth
            and not self.configuration.enable_password_oauth2
        ):
            logger.info("Enabling basic authentication plugin")
            self.get_user = Depends(set_basic_auth(self))
        elif self.configuration.enable_password_oauth2:
            logger.info("Enabling oauth2 authentication plugin")
            self.get_user = Depends(
                set_oauth2(
                    self,
                    openfaas_enable=self.configuration.enable_openfaas,
                    openfaas_function=self.configuration.openfaas_function,
                )
            )
        else:
            logger.info("Disabling authentication")
            self.get_user = Depends(set_no_auth(self))
        logger.info("Finished configuring application")
