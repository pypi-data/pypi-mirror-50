from typing import List, Dict


ALL_PLUGINS = {
    "basic-auth": {"extra": None, "env": "app_enable_basic_auth"},
    "oauth2-password": {"extra": "oauth", "env": "app_enable_password_oauth2"},
    "instrumentation": {"extra": None, "env": "app_enable_instrumentation"},
    "sqlite": {"extra": "sqlite", "env": "app_enable_sql"},
    "postgres": {"extra": "postgres", "env": "app_enable_sql"},
    "mysql": {"extra": "mysql", "env": "app_enable_sql"},
    "async-sqlite": {"extra": "async-sqlite", "env": "app_enable_async_sql"},
    "async-postgres": {"extra": "async-postgres", "env": "app_enable_async_sql"},
    "async-mysql": {"extra": "async-mysql", "env": "app_enable_async_sql"},
    "mongodb": {"extra": "mongodb", "env": "app_enable_mongodb"},
}


def get_plugin_info(plugin: str) -> Dict[str, str]:
    if plugin not in ALL_PLUGINS:
        raise ValueError(
            f"plugin {plugin} does not exist. Available plugins: {', '.join(ALL_PLUGINS)}"
        )
    else:
        return ALL_PLUGINS[plugin]


def get_plugins_env_and_extras(plugins: List[str]) -> List[str]:
    extras = []
    env = {}
    for plugin in plugins:
        plugin_info = get_plugin_info(plugin)
        if plugin_info["extra"]:
            extras.append(plugin_info["extra"])
        var = plugin_info["env"]
        env[var] = 1
    return extras, env
