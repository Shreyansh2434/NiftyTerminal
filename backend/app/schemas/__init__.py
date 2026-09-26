"""Pydantic API schemas.

This package is the package-form compatibility API for older integrations that
imported the original ``app.schemas`` module.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.backtest import (
    BacktestCompareResponse,
    BacktestConfigurationRequest,
    BacktestRunRequest,
    BacktestRunResponse,
    BacktestTradeResponse,
)


class ApiMeta(BaseModel):
    source: str = "empty"
    cached: bool = False
    generated_at: datetime
    warning: str | None = None


class SpotQuote(BaseModel):
    symbol: str = "NIFTY"
    value: float | None = None
    change: float | None = None
    change_percent: float | None = None
    timestamp: datetime
    meta: ApiMeta


class OptionRow(BaseModel):
    strike: float
    call_oi: int = 0
    call_oi_change: int = 0
    call_volume: int = 0
    call_iv: float | None = None
    call_ltp: float | None = None
    put_oi: int = 0
    put_oi_change: int = 0
    put_volume: int = 0
    put_iv: float | None = None
    put_ltp: float | None = None


class OptionChainResponse(BaseModel):
    symbol: str = "NIFTY"
    expiry: str | None = None
    spot: float | None = None
    rows: list[OptionRow] = Field(default_factory=list)
    expiries: list[str] = Field(default_factory=list)
    meta: ApiMeta


class AnalyticsSummary(BaseModel):
    symbol: str = "NIFTY"
    spot: float | None = None
    pcr: float | None = None
    max_pain: float | None = None
    call_wall: float | None = None
    put_wall: float | None = None
    support: float | None = None
    resistance: float | None = None
    bias: str = "NEUTRAL"
    meta: ApiMeta


class HeatmapCell(BaseModel):
    strike: float
    call_oi: int = 0
    put_oi: int = 0
    call_oi_change: int = 0
    put_oi_change: int = 0


class HeatmapResponse(BaseModel):
    symbol: str = "NIFTY"
    rows: list[HeatmapCell] = Field(default_factory=list)
    meta: ApiMeta


class MaxPainResponse(BaseModel):
    symbol: str = "NIFTY"
    strike: float | None = None
    payouts: dict[str, float] = Field(default_factory=dict)
    meta: ApiMeta


class OIChange(BaseModel):
    strike: float
    call_change: int = 0
    put_change: int = 0


class OIChangesResponse(BaseModel):
    symbol: str = "NIFTY"
    changes: list[OIChange] = Field(default_factory=list)
    meta: ApiMeta


class Signal(BaseModel):
    name: str
    value: str
    confidence: float = 0
    rationale: str


class SignalsResponse(BaseModel):
    symbol: str = "NIFTY"
    signals: list[Signal] = Field(default_factory=list)
    meta: ApiMeta


class StatusResponse(BaseModel):
    status: str
    database: bool
    market_data: str
    generated_at: datetime
    details: dict[str, Any] = Field(default_factory=dict)


__all__ = [
    "ApiMeta",
    "SpotQuote",
    "OptionRow",
    "OptionChainResponse",
    "AnalyticsSummary",
    "HeatmapCell",
    "HeatmapResponse",
    "MaxPainResponse",
    "OIChange",
    "OIChangesResponse",
    "Signal",
    "SignalsResponse",
    "StatusResponse",
    "BacktestCompareResponse",
    "BacktestConfigurationRequest",
    "BacktestRunRequest",
    "BacktestRunResponse",
    "BacktestTradeResponse",
]
