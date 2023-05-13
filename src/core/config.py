import os
from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseSettings

__all__ = (
    "Settings",
    "yaml_settings",
    "get_settings",
)


class App(BaseSettings):
    domain: str
    project_name: str
    description: str
    version: str
    api_doc_prefix: str
    host: str
    port: int
    debug: bool
    jwt_secret: str
    jwt_lifetime: int


class Postgres(BaseSettings):
    host: str
    port: int
    dbname: str
    user: str
    password: str

    @property
    def async_dsn(self) -> str:
        host: str = self.host
        port: int = self.port
        dbname: str = self.dbname
        user: str = self.user
        password: str = self.password
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}"


class Minio(BaseSettings):
    host: str
    port: int
    access_key: str
    secret_key: str


class Settings(BaseSettings):
    app: App
    postgres: Postgres
    minio: Minio


config_file = os.getenv("CONFIG_FILE", "config.local.yaml")
settings_path = Path(__file__).parent / config_file  # type: ignore
with settings_path.open("r") as f:
    yaml_settings = yaml.load(f, Loader=yaml.Loader)


@lru_cache
async def get_settings() -> Settings:
    return Settings(**yaml_settings)
