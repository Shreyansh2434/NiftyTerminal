from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ToolRequest(BaseModel):
    tool: Literal["quote", "options", "backtest", "monte_carlo"]
    arguments: dict[str, Any] = Field(default_factory=dict)


class AnalogueRequest(BaseModel):
    current: dict[str, Any]
    history: list[dict[str, Any]] = Field(default_factory=list)
    limit: int = Field(default=3, ge=1, le=50)


class CopilotQueryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2_000)
    symbol: str = Field(default="NIFTY", min_length=1, max_length=32)


class FinSQLRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2_000)
    execute: bool = False
