"""Deterministic option fills used by the Phase 2 backtest.

The simulator is intentionally conservative: short legs are sold at the bid
and long legs are bought at the ask on entry; the reverse is used on exit.
Slippage is applied away from the trader on every fill and commissions are
charged per contract.  No market data is mutated by this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, pi, sqrt
from typing import Any


@dataclass(frozen=True)
class OptionLeg:
    option_type: str
    strike: float
    quantity: int
    side: str


class PriceSimulator:
    def __init__(
        self,
        *,
        spread_bps: float = 10.0,
        slippage_bps: float = 4.0,
        commission_per_contract: float = 20.0,
        lot_size: int = 50,
    ) -> None:
        self.spread_bps = max(0.0, float(spread_bps))
        self.slippage_bps = max(0.0, float(slippage_bps))
        self.commission_per_contract = max(0.0, float(commission_per_contract))
        self.lot_size = max(1, int(lot_size))

    @staticmethod
    def theoretical_price(
        spot: float,
        strike: float,
        days_to_expiry: int,
        volatility: float = 0.18,
        option_type: str = "put",
    ) -> float:
        """A transparent BSM-inspired price with an intrinsic floor."""
        spot, strike = max(0.0, float(spot)), max(0.0, float(strike))
        t = max(0.0, days_to_expiry) / 365.0
        intrinsic = max(0.0, strike - spot) if option_type.lower() == "put" else max(0.0, spot - strike)
        if t <= 0 or spot <= 0 or volatility <= 0:
            return intrinsic
        # ATM time value scaled by distance from spot.  It is stable without
        # scipy and is sufficient for execution/slippage modelling.
        time_value = spot * float(volatility) * sqrt(t / (2.0 * pi))
        distance = abs(strike - spot) / max(spot, 1.0)
        return intrinsic + time_value * exp(-2.0 * distance)

    def quote(self, theoretical: float) -> tuple[float, float]:
        theoretical = max(0.0, float(theoretical))
        half_spread = theoretical * self.spread_bps / 20_000.0
        bid = max(0.0, theoretical - half_spread)
        ask = theoretical + half_spread
        return bid, ask

    def fill_price(self, theoretical: float, side: str) -> tuple[float, float]:
        """Return (fill, execution slippage) for a buy/sell order."""
        bid, ask = self.quote(theoretical)
        side = side.lower()
        reference = ask if side == "buy" else bid
        slip = reference * self.slippage_bps / 10_000.0
        fill = reference + slip if side == "buy" else max(0.0, reference - slip)
        return fill, abs(fill - theoretical)

    def get_fill_price(self, theoretical: float, side: str) -> float:
        """Compatibility helper returning only the executable price."""
        return self.fill_price(theoretical, side)[0]

    def apply_spread_slippage(self, theoretical: float, side: str) -> float:
        return self.get_fill_price(theoretical, side)

    @staticmethod
    def calculate_pnl(entry_price: float, exit_price: float, quantity: int, side: str = "long") -> float:
        direction = 1.0 if side.lower() in {"long", "buy"} else -1.0
        return (float(exit_price) - float(entry_price)) * int(quantity) * direction

    def _leg_theoretical(
        self, spot: float, strike: float, days: int, volatility: float, option_type: str
    ) -> float:
        return self.theoretical_price(spot, strike, days, volatility, option_type)

    def simulate_iron_condor(
        self,
        *,
        entry_spot: float,
        exit_spot: float,
        short_put: float,
        long_put: float,
        short_call: float,
        long_call: float,
        days_held: int = 5,
        days_to_expiry: int = 30,
        volatility: float = 0.18,
        lot_size: int | None = None,
        target_profit_pct: float = 0.50,
        stop_loss_pct: float = 0.35,
        exit_reason: str | None = None,
    ) -> dict[str, Any]:
        """Simulate a four-leg iron-condor round trip.

        The returned ``net_pnl`` is in currency and includes all costs.  At
        expiry the option value is intrinsic; before expiry a conservative
        time-value mark is used for the exit.
        """
        quantity = self.lot_size if lot_size is None else max(1, int(lot_size))
        legs = [
            OptionLeg("put", float(short_put), -1, "sell"),
            OptionLeg("put", float(long_put), 1, "buy"),
            OptionLeg("call", float(short_call), -1, "sell"),
            OptionLeg("call", float(long_call), 1, "buy"),
        ]
        entry_credit = 0.0
        exit_debit = 0.0
        theoretical_result = 0.0
        leg_results: list[dict[str, Any]] = []
        remaining = max(0, int(days_to_expiry) - int(days_held))
        for leg in legs:
            entry_theoretical = self._leg_theoretical(
                entry_spot, leg.strike, days_to_expiry, volatility, leg.option_type
            )
            # Selling is a credit and buying is a debit.
            entry_side = "sell" if leg.side == "sell" else "buy"
            entry_fill, _ = self.fill_price(entry_theoretical, entry_side)
            exit_theoretical = self._leg_theoretical(
                exit_spot, leg.strike, remaining, volatility, leg.option_type
            )
            exit_side = "buy" if leg.side == "sell" else "sell"
            exit_fill, _ = self.fill_price(exit_theoretical, exit_side)
            signed_entry = entry_fill if leg.side == "sell" else -entry_fill
            signed_exit = -exit_fill if leg.side == "sell" else exit_fill
            entry_credit += signed_entry
            exit_debit += signed_exit
            theoretical_result += (
                (entry_theoretical if leg.side == "sell" else -entry_theoretical)
                + (-exit_theoretical if leg.side == "sell" else exit_theoretical)
            )
            leg_results.append(
                {
                    "option_type": leg.option_type,
                    "strike": leg.strike,
                    "side": leg.side,
                    "entry_price": round(entry_fill, 6),
                    "exit_price": round(exit_fill, 6),
                    "quantity": quantity,
                }
            )
        gross_pnl = theoretical_result * quantity
        execution_pnl = (entry_credit + exit_debit) * quantity
        # The difference captures both quoted spread and adverse slippage.
        slippage = max(0.0, gross_pnl - execution_pnl)
        # Brokerage is charged per executed lot/order (the convention used by
        # Indian index-option brokers), while P&L and slippage use lot size.
        commission = len(legs) * 2 * self.commission_per_contract
        net_pnl = gross_pnl - commission - slippage
        width = max(abs(float(short_put) - float(long_put)), abs(float(long_call) - float(short_call)))
        max_risk = max(0.0, width * quantity - max(0.0, entry_credit) * quantity / 2.0)
        target_pnl = max_risk * max(0.0, float(target_profit_pct))
        stop_pnl = max_risk * max(0.0, float(stop_loss_pct))
        if exit_reason is None:
            if gross_pnl >= target_pnl and target_pnl > 0:
                exit_reason = "target"
            elif gross_pnl <= -stop_pnl and stop_pnl > 0:
                exit_reason = "stop"
            else:
                exit_reason = "time"
        return {
            "legs": leg_results,
            "gross_pnl": round(gross_pnl, 6),
            "commission": round(commission, 6),
            "slippage": round(slippage, 6),
            "net_pnl": round(net_pnl, 6),
            "entry_credit": round(entry_credit * quantity, 6),
            "exit_debit": round(exit_debit * quantity, 6),
            "max_risk": round(max_risk, 6),
            "target_pnl": round(target_pnl, 6),
            "stop_pnl": round(stop_pnl, 6),
            "exit_reason": exit_reason,
        }

    def _simulate_vertical_spread(
        self,
        *,
        entry_spot: float,
        exit_spot: float,
        short_strike: float,
        long_strike: float,
        option_type: str,
        days_held: int = 5,
        days_to_expiry: int = 30,
        volatility: float = 0.18,
        lot_size: int | None = None,
        target_profit_pct: float = 0.50,
        stop_loss_pct: float = 0.35,
        exit_reason: str | None = None,
    ) -> dict[str, Any]:
        """Simulate a two-leg credit spread with executable bid/ask fills.

        ``max_risk`` is calculated from the configured NIFTY lot size and the
        distance between the strikes, less the entry credit.  The caller can
        pass an explicit exit reason when it has evaluated an intraday path;
        otherwise the deterministic mark is classified as target, stop, or
        time.
        """
        quantity = self.lot_size if lot_size is None else max(1, int(lot_size))
        option_type = option_type.lower()
        legs = [
            OptionLeg(option_type, float(short_strike), -1, "sell"),
            OptionLeg(option_type, float(long_strike), 1, "buy"),
        ]
        entry_credit_per_unit = 0.0
        exit_debit_per_unit = 0.0
        theoretical_pnl_per_unit = 0.0
        execution_pnl_per_unit = 0.0
        leg_results: list[dict[str, Any]] = []
        remaining = max(0, int(days_to_expiry) - int(days_held))

        for leg in legs:
            entry_theoretical = self._leg_theoretical(
                entry_spot, leg.strike, days_to_expiry, volatility, option_type
            )
            entry_fill, _ = self.fill_price(entry_theoretical, leg.side)
            exit_side = "buy" if leg.side == "sell" else "sell"
            exit_theoretical = self._leg_theoretical(
                exit_spot, leg.strike, remaining, volatility, option_type
            )
            exit_fill, _ = self.fill_price(exit_theoretical, exit_side)
            signed_entry_theoretical = entry_theoretical if leg.side == "sell" else -entry_theoretical
            signed_exit_theoretical = -exit_theoretical if leg.side == "sell" else exit_theoretical
            signed_entry_execution = entry_fill if leg.side == "sell" else -entry_fill
            signed_exit_execution = -exit_fill if leg.side == "sell" else exit_fill
            theoretical_pnl_per_unit += signed_entry_theoretical + signed_exit_theoretical
            execution_pnl_per_unit += signed_entry_execution + signed_exit_execution
            if leg.side == "sell":
                entry_credit_per_unit += entry_fill
                exit_debit_per_unit += exit_fill
            else:
                entry_credit_per_unit -= entry_fill
                exit_debit_per_unit -= exit_fill
            leg_results.append(
                {
                    "option_type": leg.option_type,
                    "strike": leg.strike,
                    "side": leg.side,
                    "entry_price": round(entry_fill, 6),
                    "exit_price": round(exit_fill, 6),
                    "quantity": quantity,
                }
            )

        entry_credit_per_unit = max(0.0, entry_credit_per_unit)
        width = abs(float(short_strike) - float(long_strike))
        max_risk = max(0.0, (width - entry_credit_per_unit) * quantity)
        gross_pnl = theoretical_pnl_per_unit * quantity
        execution_pnl = execution_pnl_per_unit * quantity
        slippage = max(0.0, gross_pnl - execution_pnl)
        commission = len(legs) * 2 * self.commission_per_contract
        net_pnl = execution_pnl - commission
        target_pnl = max_risk * max(0.0, float(target_profit_pct))
        stop_pnl = max_risk * max(0.0, float(stop_loss_pct))
        if exit_reason is None:
            if gross_pnl >= target_pnl and target_pnl > 0:
                exit_reason = "target"
            elif gross_pnl <= -stop_pnl and stop_pnl > 0:
                exit_reason = "stop"
            else:
                exit_reason = "time"

        return {
            "legs": leg_results,
            "gross_pnl": round(gross_pnl, 6),
            "commission": round(commission, 6),
            "slippage": round(slippage, 6),
            "net_pnl": round(net_pnl, 6),
            "entry_credit": round(entry_credit_per_unit * quantity, 6),
            "exit_debit": round(max(0.0, exit_debit_per_unit) * quantity, 6),
            "max_risk": round(max_risk, 6),
            "target_pnl": round(target_pnl, 6),
            "stop_pnl": round(stop_pnl, 6),
            "return_pct": round(net_pnl / max(max_risk, 1.0) * 100, 6),
            "days_held": max(0, int(days_held)),
            "exit_reason": exit_reason,
        }

    def simulate_put_spread(
        self,
        *,
        entry_spot: float,
        exit_spot: float,
        short_put: float | None = None,
        long_put: float | None = None,
        short_strike: float | None = None,
        long_strike: float | None = None,
        wing_width: float | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Simulate a short put / long put credit spread."""
        short = short_put if short_put is not None else short_strike
        long = long_put if long_put is not None else long_strike
        if short is None and long is None and wing_width is not None:
            short = float(entry_spot) - abs(float(wing_width))
            long = short - abs(float(wing_width))
        if short is None or long is None:
            raise ValueError("short_put/long_put or wing_width are required")
        return self._simulate_vertical_spread(
            entry_spot=entry_spot,
            exit_spot=exit_spot,
            short_strike=short,
            long_strike=long,
            option_type="put",
            **kwargs,
        )

    def simulate_call_spread(
        self,
        *,
        entry_spot: float,
        exit_spot: float,
        short_call: float | None = None,
        long_call: float | None = None,
        short_strike: float | None = None,
        long_strike: float | None = None,
        wing_width: float | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Simulate a short call / long call credit spread."""
        short = short_call if short_call is not None else short_strike
        long = long_call if long_call is not None else long_strike
        if short is None and long is None and wing_width is not None:
            short = float(entry_spot) + abs(float(wing_width))
            long = short + abs(float(wing_width))
        if short is None or long is None:
            raise ValueError("short_call/long_call or wing_width are required")
        return self._simulate_vertical_spread(
            entry_spot=entry_spot,
            exit_spot=exit_spot,
            short_strike=short,
            long_strike=long,
            option_type="call",
            **kwargs,
        )

    # Explicit aliases make the intended strategy names available to older
    # clients that called these methods "credit spreads".
    simulate_put_credit_spread = simulate_put_spread
    simulate_call_credit_spread = simulate_call_spread

    def simulate_condor(self, **kwargs: Any) -> dict[str, Any]:
        """Backward-compatible alias used by early Phase 2 clients."""
        return self.simulate_iron_condor(**kwargs)


def simulate_iron_condor(**kwargs: Any) -> dict[str, Any]:
    """Functional convenience wrapper for service and smoke-test callers."""
    simulator_options = {
        key: kwargs.pop(key)
        for key in ("spread_bps", "slippage_bps", "commission_per_contract", "lot_size")
        if key in kwargs
    }
    return PriceSimulator(**simulator_options).simulate_iron_condor(**kwargs)


def _simulate_strategy(strategy: str, **kwargs: Any) -> dict[str, Any]:
    simulator_options = {
        key: kwargs.pop(key)
        for key in ("spread_bps", "slippage_bps", "commission_per_contract", "lot_size")
        if key in kwargs
    }
    method = getattr(PriceSimulator(**simulator_options), strategy)
    return method(**kwargs)


def simulate_put_spread(**kwargs: Any) -> dict[str, Any]:
    return _simulate_strategy("simulate_put_spread", **kwargs)


def simulate_call_spread(**kwargs: Any) -> dict[str, Any]:
    return _simulate_strategy("simulate_call_spread", **kwargs)


__all__ = [
    "OptionLeg",
    "PriceSimulator",
    "simulate_iron_condor",
    "simulate_put_spread",
    "simulate_call_spread",
]
