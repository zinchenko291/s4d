import os

from pydantic_settings import BaseSettings, SettingsConfigDict

CONFIG_MODEL_CONFIG = SettingsConfigDict(
    alias_generator=lambda field_name: field_name.upper(),
    env_file='.env' if os.path.exists('.env') else None,
)


class AppConfig(BaseSettings):
    """
    Конфигурации проекта
    """

    model_config = CONFIG_MODEL_CONFIG

    rabbit_user: str
    rabbit_pass: str
    rabbit_host: str
    rabbit_port: int

    redis_host: str
    redis_port: int
    redis_pass: str
    redis_db: int


app_config = AppConfig()