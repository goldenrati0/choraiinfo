import os


class FlaskConfig:
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "DEV")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "s3cr3t_key")


class Database:
    _database: str = os.getenv("DB", "postgresql")
    _db_driver: str = os.getenv("DB_DRIVER", "psycopg2")
    _db_host: str = os.getenv("DB_HOST", "127.0.0.1")
    _db_port: int = os.getenv("DB_PORT", 5432)
    _db_username: str = os.getenv("DB_USER", "postgres")
    _db_password: str = os.getenv("DB_PASSWORD", "letsplay")
    _db_name: str = os.getenv("DB_NAME", "choraiinfo")


class SQLAlchemyConfig:
    track_modifications: bool = False
    database_uri: str = f"{Database._database}+{Database._db_driver}://{Database._db_username}:{Database._db_password}@{Database._db_host}:{Database._db_port}/{Database._db_name}"
    echo: bool = False
    native_unicode: str = "utf-8"
    commit_on_teardown: bool = False


class Configuration:
    ENV: str = FlaskConfig.ENVIRONMENT
    DEBUG: bool = FlaskConfig.ENVIRONMENT == "DEV"
    SECRET_KEY: str = FlaskConfig.SECRET_KEY
    SQLALCHEMY_DATABASE_URI: str = SQLAlchemyConfig.database_uri
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = SQLAlchemyConfig.track_modifications
    SQLALCHEMY_ECHO: bool = SQLAlchemyConfig.echo
    SQLALCHEMY_COMMIT_ON_TEARDOWN: bool = SQLAlchemyConfig.commit_on_teardown
    SQLALCHEMY_NATIVE_UNICODE: str = SQLAlchemyConfig.native_unicode
