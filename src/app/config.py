from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    port: int = 4000
    cors_origins: str = "http://localhost:3005,http://127.0.0.1:3005"
    mes_base_url: str = "http://127.0.0.1:4100"
    cmms_base_url: str = "http://127.0.0.1:4100"
    llm_base_url: str = ""

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
