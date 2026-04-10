from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Distributed AI Trading Engine"
    environment: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    jwt_secret: str = "change-this-secret"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    kafka_bootstrap_servers: str = "kafka:9092"
    kafka_market_topic: str = "market-ticks"
    kafka_order_topic: str = "trade-orders"
    database_url: str = "sqlite+aiosqlite:///./trading.db"
    model_path: str = "/models/lstm_model.keras"
    risk_max_notional: float = 1_000_000
    risk_max_daily_loss: float = 50_000
    prometheus_enabled: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
