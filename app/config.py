from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AI Media Watch"
    app_env: str = "production"
    log_level: str = "INFO"

    database_url: str = "postgresql+psycopg://mediawatch:change-me@postgres:5432/mediawatch"
    redis_url: str = "redis://redis:6379/0"
    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/1"

    s3_endpoint_url: str = "http://minio:9000"
    s3_access_key_id: str = "minioadmin"
    s3_secret_access_key: str = "minioadmin-change-me"
    s3_bucket: str = "mediawatch-assets"
    s3_region: str = "us-east-1"
    s3_secure: bool = False

    playwright_headless: bool = True
    playwright_browser: str = "chromium"
    playwright_timeout_ms: int = 30000
    playwright_user_agents: str = ""
    proxy_urls: str = ""
    proxy_rotation_strategy: str = "round_robin"

    collect_keywords_interval_minutes: int = Field(default=30, ge=15, le=60)
    monitor_accounts_interval_minutes: int = Field(default=30, ge=15, le=60)

    tiktok_research_api_token: str = ""
    tiktok_research_api_base_url: str = "https://open.tiktokapis.com"
    tiktok_region_code: str = "KZ"
    tiktok_query_days: int = Field(default=7, ge=1, le=30)
    tiktok_max_count: int = Field(default=100, ge=1, le=100)
    instagram_graph_api_token: str = ""

    @property
    def proxy_url_list(self) -> list[str]:
        return [item.strip() for item in self.proxy_urls.split(",") if item.strip()]

    @property
    def user_agent_list(self) -> list[str]:
        return [item.strip() for item in self.playwright_user_agents.split("|") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
