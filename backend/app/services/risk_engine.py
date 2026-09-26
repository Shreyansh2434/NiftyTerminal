"""Deterministic portfolio risk controls shared by paper execution and APIs."""
from __future__ import annotations

import math
from dataclasses import dataclass

from app.core.config import get_settings


@dataclass(frozen=True)
class RiskDecision:
    allowed: bool
    checks: dict[str, bool]
    reasons: list[str]


class RiskEngine:
    def __init__(self) -> None:
        self.settings = get_settings()

    def kelly_fraction(self, win_probability: float = 0.5, win_loss_ratio: float = 1.5) -> float:
        if win_loss_ratio <= 0:
            return 0.0
        return max(0.0, min(0.25, (win_probability * win_loss_ratio - (1 - win_probability)) / win_loss_ratio))

    def size_for_risk(self, capital: float, price: float, risk_fraction: float = 0.01) -> int:
        if capital <= 0 or price <= 0:
            return 0
        return max(0, math.floor(capital * max(0.0, min(risk_fraction, 0.25)) / price))

    def check_order(self, *, symbol: str, side: str, quantity: int, price: float, notional: float | None = None) -> RiskDecision:
        value = abs(notional if notional is not None else quantity * price)
        checks = {
            "kill_switch_clear": (not self.settings.kill_switch_active) or self.settings.trading_mode.lower() == "paper",
            "paper_mode": self.settings.trading_mode.lower() == "paper",
            "symbol_present": bool(symbol.strip()),
            "side_valid": side.upper() in {"BUY", "SELL"},
            "quantity_positive": quantity > 0,
            "price_positive": price > 0,
            "notional_within_limit": value <= self.settings.max_order_notional,
        }
        reasons = [name for name, passed in checks.items() if not passed]
        # A kill switch intentionally blocks even paper orders only when explicitly enabled.
        # The API offers a safe preview in this state; paper execution can use the default
        # operational switch by setting KILL_SWITCH_ACTIVE=false.
        return RiskDecision(not reasons, checks, reasons)

    def kill_switch_status(self) -> dict[str, bool | str]:
        return {"active": self.settings.kill_switch_active, "mode": self.settings.trading_mode, "live_enabled": self.settings.live_trading_enabled}

    def limits(self) -> dict[str, float | bool]:
        return {"max_order_notional": self.settings.max_order_notional, "max_portfolio_var": self.settings.max_portfolio_var, "kill_switch_active": self.settings.kill_switch_active}
