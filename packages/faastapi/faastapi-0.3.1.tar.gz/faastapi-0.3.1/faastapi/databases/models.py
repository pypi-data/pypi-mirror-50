from pydantic import BaseSettings


class SQLDatabaseConfig(BaseSettings):
    uri: str = "sqlite:///example.db"

    class Config:
        env_prefix = "APP_SQL_"
        case_insensitive = True


class AsyncSQLDatabaseConfig(SQLDatabaseConfig):
    class Config:
        env_prefix = "APP_SQL_"
        case_insensitive = True


class MongoDBConfig(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 27017
    database: str = "test"

    class Config:
        env_prefix = "APP_MONGODB_"
        case_insensitive = True


class RedisConfig(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 6379
    db: int = 0

    class Config:
        env_prefix = "APP_REDIS_"
        case_insensitive = True
