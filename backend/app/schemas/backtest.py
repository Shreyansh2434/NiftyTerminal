"""Backtest API contracts.

The result payload deliberately contains JSON-friendly values so it can be
returned from the in-memory fallback as well as PostgreSQL JSON columns.
"""

from datetime import date, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class BacktestConfigurationRequest(BaseModel):
    name: str | None = None
    symbol: str = "NIFTY"
    start_date: date | None = None
    end_date: date | None = None
    initial_capital: float = Field(default=100000, gt=0)
    lot_size: int = Field(default=50, gt=0)
    entry_days: int = Field(default=5, gt=0)
    holding_days: int = Field(default=5, gt=0)
    short_delta: float = Field(default=0.16, gt=0, lt=0.5)
    wing_width: float = Field(default=150, gt=0)
    stop_loss_pct: float = Field(default=0.35, ge=0)
    target_profit_pct: float = Field(default=0.50, ge=0)
    commission_per_contract: float = Field(default=20, ge=0)
    slippage_bps: float = Field(default=4, ge=0)
    spread_bps: float = Field(default=10, ge=0)
    train_days: int = Field(default=126, gt=0)
    test_days: int = Field(default=63, gt=0)
    data: list[dict[str, Any]] | None = None


class BacktestRunRequest(BacktestConfigurationRequest):
    configuration_id: int | None = None


class BacktestTradeResponse(BaseModel):
    id: int | None = None
    trade_number: int
    symbol: str = "NIFTY"
    regime: str = "unknown"
    strategy_type: str = "IRON_CONDOR"
    entry_date: date | str
    exit_date: date | str | None = None
    entry_spot: float | None = None
    exit_spot: float | None = None
    legs: list[dict[str, Any]] = Field(default_factory=list)
    gross_pnl: float = 0
    commission: float = 0
    slippage: float = 0
    net_pnl: float = 0
    return_pct: float = 0
    exit_reason: str | None = None


class BacktestRunResponse(BaseModel):
    run_id: UUID | str
    status: str = "completed"
    symbol: str = "NIFTY"
    started_at: datetime | None = None
    completed_at: datetime | None = None
    configuration: dict[str, Any] = Field(default_factory=dict)
    metrics: dict[str, Any] = Field(default_factory=dict)
    equity_curve: list[dict[str, Any]] = Field(default_factory=list)
    walk_forward: list[dict[str, Any]] = Field(default_factory=list)
    regime_stats: dict[str, Any] = Field(default_factory=dict)
    trades_count: int = 0
    warning: str | None = None
    error: str | None = None


class BacktestCompareResponse(BaseModel):
    runs: list[BacktestRunResponse] = Field(default_factory=list)
    warning: str | None = None
