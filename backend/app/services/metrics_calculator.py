"""Pure performance and regime metrics for backtest results."""

from __future__ import annotations

from math import sqrt
from statistics import mean, stdev
from typing import Any, Iterable


def _number(trade: Any, name: str, default: float = 0.0) -> float:
    if isinstance(trade, dict):
        value = trade.get(name, default)
    else:
        value = getattr(trade, name, default)
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return default


def calculate_drawdown(equity: Iterable[float]) -> tuple[float, float]:
    peak = 0.0
    max_drawdown = 0.0
    max_drawdown_pct = 0.0
    for value in equity:
        value = float(value)
        peak = max(peak, value)
        drawdown = peak - value
        max_drawdown = max(max_drawdown, drawdown)
        if peak:
            max_drawdown_pct = max(max_drawdown_pct, drawdown / peak * 100)
    return max_drawdown, max_drawdown_pct


def calculate_metrics(
    trades: Iterable[Any],
    *,
    initial_capital: float = 100_000.0,
    periods_per_year: int = 252,
) -> dict[str, float | int | None]:
    items = list(trades)
    values = [_number(trade, "net_pnl") for trade in items]
    wins = [value for value in values if value > 0]
    losses = [value for value in values if value < 0]
    ending_capital = float(initial_capital) + sum(values)
    equity = [float(initial_capital)]
    for value in values:
        equity.append(equity[-1] + value)
    max_dd, max_dd_pct = calculate_drawdown(equity)
    returns = [value / max(float(initial_capital), 1.0) for value in values]
    volatility = stdev(returns) if len(returns) > 1 else 0.0
    sharpe = (mean(returns) / volatility * sqrt(periods_per_year)) if volatility else None
    gross_profit = sum(wins)
    gross_loss = abs(sum(losses))
    total_commission = sum(_number(trade, "commission") for trade in items)
    total_slippage = sum(_number(trade, "slippage") for trade in items)
    annualized_return = (
        ((ending_capital / max(float(initial_capital), 1.0)) ** (periods_per_year / max(len(values), 1)) - 1) * 100
        if values and ending_capital > 0
        else None
    )
    return {
        "total_trades": len(values),
        "winning_trades": len(wins),
        "losing_trades": len(losses),
        "win_rate": (len(wins) / len(values) * 100) if values else 0.0,
        "total_pnl": sum(values),
        "ending_capital": ending_capital,
        "total_return_pct": (sum(values) / max(float(initial_capital), 1.0) * 100),
        "return_pct": (sum(values) / max(float(initial_capital), 1.0) * 100),
        "annualized_return_pct": annualized_return,
        "average_trade": mean(values) if values else 0.0,
        "average_win": mean(wins) if wins else 0.0,
        "average_loss": mean(losses) if losses else 0.0,
        "best_trade": max(values) if values else 0.0,
        "worst_trade": min(values) if values else 0.0,
        "median_trade": sorted(values)[len(values) // 2] if values else 0.0,
        "profit_factor": (gross_profit / gross_loss) if gross_loss else None,
        "expectancy": mean(values) if values else 0.0,
        "total_commission": total_commission,
        "total_slippage": total_slippage,
        "max_drawdown": max_dd,
        "max_drawdown_pct": max_dd_pct,
        "sharpe_ratio": sharpe,
    }


def calculate_regime_stats(
    trades: Iterable[Any], *, initial_capital: float = 100_000.0
) -> dict[str, dict[str, float | int | None]]:
    grouped: dict[str, list[Any]] = {}
    for trade in trades:
        regime = (
            str(trade.get("regime", "unknown"))
            if isinstance(trade, dict)
            else str(getattr(trade, "regime", "unknown") or "unknown")
        )
        grouped.setdefault(regime, []).append(trade)
    return {
        regime: calculate_metrics(items, initial_capital=initial_capital)
        for regime, items in sorted(grouped.items())
    }


def calculate_performance_metrics(
    trades: Iterable[Any], *, initial_capital: float = 100_000.0
) -> dict[str, float | int | None]:
    """Compatibility name used by the original Phase 2 service draft."""
    return calculate_metrics(trades, initial_capital=initial_capital)


class MetricsCalculator:
    """Object-oriented compatibility API for callers that inject settings."""

    def __init__(self, initial_capital: float = 100_000.0) -> None:
        self.initial_capital = initial_capital

    def calculate(self, trades: Iterable[Any]) -> dict[str, Any]:
        return calculate_metrics(trades, initial_capital=self.initial_capital)

    def per_regime(self, trades: Iterable[Any]) -> dict[str, dict[str, Any]]:
        return calculate_regime_stats(trades, initial_capital=self.initial_capital)

    def calculate_regime_stats(self, trades: Iterable[Any]) -> dict[str, dict[str, Any]]:
        return self.per_regime(trades)


__all__ = [
    "MetricsCalculator",
    "calculate_drawdown",
    "calculate_metrics",
    "calculate_performance_metrics",
    "calculate_regime_stats",
]
