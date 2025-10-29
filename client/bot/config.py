from pydantic import SecretStr
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    bot_token: SecretStr
    redis_url: str
    api_url: str = "http://localhost:8080"
    domain: str

    ttl_choices = [("1 hour", 3600), ("1 day", 86400), ("1 week", 604800)]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="",
        case_sensitive=False,
    )


settings = Settings()
