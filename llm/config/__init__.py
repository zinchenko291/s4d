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

    yandex_agent_api_key: str
    yandex_agent_url: str
    yandex_base_assistant_url: str
    yandex_project_id: str
    mcp_server_url: str

    rabbit_user: str
    rabbit_pass: str
    rabbit_host: str
    rabbit_port: int


app_config = AppConfig()