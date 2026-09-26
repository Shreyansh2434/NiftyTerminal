from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NIFTY Options Intelligence Terminal"
    environment: str = "development"
    log_level: str = "INFO"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/nifty_terminal"
    nse_timeout_seconds: float = 8.0
    market_cache_seconds: int = 30
    scheduler_enabled: bool = True
    refresh_interval_seconds: int = 60
    # Safety defaults: no connector can place live orders unless every gate is explicit.
    trading_mode: str = "paper"
    live_trading_enabled: bool = False
    live_trading_confirmation: str = ""
    kill_switch_active: bool = True
    max_order_notional: float = 100000.0
    max_portfolio_var: float = 0.05
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
