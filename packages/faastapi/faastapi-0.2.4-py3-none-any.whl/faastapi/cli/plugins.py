from typing import List, Dict, Callable
from pydantic import BaseModel
from ..databases.models import (
    SQLDatabaseConfig,
    AsyncSQLDatabaseConfig,
    MongoDBConfig,
    RedisConfig,
)
from ..security.models import JWTConfig, CORSConfig, BasicAuthConfig


class Plugin(BaseModel):
    env: str
    config: Callable = None
    extra: str = None


ALL_PLUGINS = {
    "basic-auth": Plugin(config=BasicAuthConfig, env="app_enable_basic_auth"),
    "oauth2-password": Plugin(
        config=JWTConfig, env="app_enable_password_oauth2", extra="oauth"
    ),
    "instrumentation": Plugin(env="app_enable_instrumentation"),
    "sqlite": Plugin(config=SQLDatabaseConfig, env="app_enable_sql", extra="sqlite"),
    "postgres": Plugin(
        config=SQLDatabaseConfig, env="app_enable_sql", extra="postgres"
    ),
    "mysql": Plugin(config=SQLDatabaseConfig, env="app_enable_sql", extra="mysql"),
    "async-sqlite": Plugin(
        config=AsyncSQLDatabaseConfig, env="app_enable_async_sql", extra="async-sqlite"
    ),
    "async-postgres": Plugin(
        config=AsyncSQLDatabaseConfig,
        env="app_enable_async_sql",
        extra="async-postgres",
    ),
    "async-mysql": Plugin(
        config=AsyncSQLDatabaseConfig, env="app_enable_async_sql", extra="async-mysql"
    ),
    "mongodb": Plugin(config=MongoDBConfig, env="app_enable_mongodb", extra="mongodb"),
    "cors": Plugin(config=CORSConfig, env="app_enable_cors"),
    "redis": Plugin(config=RedisConfig, env="app_enable_redis", extra="redis"),
}


def get_plugin(plugin: str) -> Plugin:
    if plugin not in ALL_PLUGINS:
        raise ValueError(
            f"plugin {plugin} does not exist. Available plugins: {', '.join(ALL_PLUGINS)}"
        )
    else:
        return ALL_PLUGINS[plugin]


def get_plugins_env_and_extras(plugins: Dict[str, dict]) -> List[str]:
    extras = []
    env = {}
    for plugin_name, dict_config in plugins.items():
        plugin = get_plugin(plugin_name)
        if plugin.extra:
            extras.append(plugin.extra)
        var = plugin.env
        env[var] = 1
        if dict_config:
            config = plugin.config(**dict_config)
            try:
                prefix = plugin.config.Config.env_prefix
            except AttributeError:
                continue
            else:
                for field, value in config:
                    env[prefix.lower() + field] = value
    return extras, env
