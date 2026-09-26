"""Consistent display formatting for metrics and trade values."""

from __future__ import annotations

from typing import Any


def _number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def format_currency(value: Any, currency: str = "₹") -> str:
    return f"{currency}{_number(value):,.2f}"


def format_percent(value: Any, decimals: int = 2) -> str:
    return f"{_number(value):,.{decimals}f}%"


def format_number(value: Any, decimals: int = 2) -> str:
    return f"{_number(value):,.{decimals}f}"
