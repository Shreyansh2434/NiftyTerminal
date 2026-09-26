"""Walk-forward, signal-driven NIFTY options backtest engine.

The engine accepts normalized OHLCV dictionaries, pandas-like records, or
objects with ``date``/``timestamp`` and ``close`` attributes.  A decision at
index *i* only reads ``bars[:i]``; bars after the entry are used solely to
mark the already-open position.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from math import log, sqrt
from statistics import mean, stdev
from typing import Any, Iterable, Mapping

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import OHLCV
from app.services.metrics_calculator import calculate_metrics, calculate_regime_stats
from app.services.price_simulator import PriceSimulator


@dataclass
class BacktestConfig:
    symbol: str = "NIFTY"
    initial_capital: float = 100_000.0
    lot_size: int = 50
    entry_days: int = 5
    holding_days: int = 5
    short_delta: float = 0.16
    wing_width: float = 150.0
    stop_loss_pct: float = 0.35
    target_profit_pct: float = 0.50
    commission_per_contract: float = 20.0
    slippage_bps: float = 4.0
    spread_bps: float = 10.0
    train_days: int = 126
    test_days: int = 63
    start_date: date | None = None
    end_date: date | None = None
    data: list[dict[str, Any]] | None = None

    @classmethod
    def from_mapping(cls, values: Mapping[str, Any] | None) -> "BacktestConfig":
        values = values or {}
        allowed = {field_name for field_name in cls.__dataclass_fields__}
        clean = {key: value for key, value in values.items() if key in allowed}
        for key in ("start_date", "end_date"):
            if isinstance(clean.get(key), str):
                clean[key] = date.fromisoformat(clean[key])
        return cls(**clean)

    def as_dict(self) -> dict[str, Any]:
        result = {key: value for key, value in self.__dict__.items() if key != "data"}
        for key in ("start_date", "end_date"):
            if isinstance(result.get(key), (date, datetime)):
                result[key] = result[key].isoformat()
        return result


def _date(value: Any, fallback: date) -> date:
    if value is None:
        return fallback
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.fromisoformat(str(value).replace("Z", "+00:00")).date()


def normalize_bars(data: Iterable[Any]) -> list[dict[str, Any]]:
    bars: list[dict[str, Any]] = []
    fallback = date(2000, 1, 1)
    for item in data:
        if isinstance(item, Mapping):
            get = item.get
        else:
            get = lambda key, default=None: getattr(item, key, default)
        close = get("close", get("adj_close", None))
        if close is None:
            continue
        timestamp = get("date", get("timestamp", get("datetime", None)))
        day = _date(timestamp, fallback)
        fallback = day + timedelta(days=1)
        value = float(close)
        bars.append(
            {
                "date": day,
                "open": float(get("open", value) or value),
                "high": float(get("high", value) or value),
                "low": float(get("low", value) or value),
                "close": value,
                "volume": int(get("volume", 0) or 0),
                "regime": get("regime"),
                "iv_rank": get(
                    "iv_rank",
                    get("ivRank", get("implied_volatility_rank", get("iv_rank_percentile", None))),
                ),
            }
        )
    unique: dict[date, dict[str, Any]] = {}
    for bar in bars:
        unique[bar["date"]] = bar
    return [unique[key] for key in sorted(unique)]


def synthetic_history(days: int = 520, seed_price: float = 22_000.0) -> list[dict[str, Any]]:
    """Deterministic fallback data keeps the API useful without a data vendor."""
    value = float(seed_price)
    result = []
    for index in range(days):
        drift = 0.00025 if (index // 70) % 2 == 0 else -0.00012
        cycle = ((index % 31) - 15) / 120_000
        previous = value
        value = max(100.0, value * (1.0 + drift + cycle))
        result.append(
            {
                "date": date(2022, 1, 3) + timedelta(days=index),
                "open": previous,
                "high": max(previous, value) * 1.004,
                "low": min(previous, value) * 0.996,
                "close": value,
                "volume": 1_000_000,
            }
        )
    return result


async def load_historical_data(
    session: AsyncSession | None,
    *,
    symbol: str = "NIFTY",
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[dict[str, Any]]:
    """Read only completed OHLCV rows; return an empty list on DB failure."""
    if session is None:
        return []
    try:
        query = select(OHLCV).where(OHLCV.symbol == symbol).order_by(OHLCV.timestamp)
        if start_date:
            query = query.where(OHLCV.timestamp >= datetime.combine(start_date, datetime.min.time()))
        if end_date:
            query = query.where(OHLCV.timestamp <= datetime.combine(end_date, datetime.max.time()))
        rows = (await session.execute(query)).scalars().all()
        return [
            {
                "date": row.timestamp,
                "open": float(row.open or row.close or 0),
                "high": float(row.high or row.close or 0),
                "low": float(row.low or row.close or 0),
                "close": float(row.close),
                "volume": row.volume or 0,
            }
            for row in rows
            if row.close is not None
        ]
    except Exception:
        return []


@dataclass
class BacktestEngine:
    config: BacktestConfig | Mapping[str, Any] = field(default_factory=BacktestConfig)
    simulator: PriceSimulator | None = None

    def __post_init__(self) -> None:
        if isinstance(self.config, Mapping):
            self.config = BacktestConfig.from_mapping(self.config)
        if self.simulator is None:
            self.simulator = PriceSimulator(
                spread_bps=self.config.spread_bps,
                slippage_bps=self.config.slippage_bps,
                commission_per_contract=self.config.commission_per_contract,
                lot_size=self.config.lot_size,
            )

    def _volatility(self, history: list[dict[str, Any]]) -> float:
        closes = [bar["close"] for bar in history[-30:]]
        if len(closes) < 3:
            return 0.18
        returns = [log(closes[i] / closes[i - 1]) for i in range(1, len(closes)) if closes[i - 1] > 0]
        return max(0.08, min(0.80, (stdev(returns) if len(returns) > 1 else 0.01) * sqrt(252)))

    def _regime(self, history: list[dict[str, Any]], volatility: float) -> str:
        """Return ``trend × volatility`` using only completed bars."""
        if len(history) < 20:
            return "unknown"
        closes = [float(bar["close"]) for bar in history[-20:]]
        short = mean(closes[-5:])
        long = mean(closes)
        slope = (closes[-1] / max(closes[0], 1.0)) - 1.0
        if slope > 0.004 or short > long * 1.002:
            trend = "trending_up"
        elif slope < -0.004 or short < long * 0.998:
            trend = "trending_down"
        else:
            trend = "ranging"
        volatility_bucket = "high_vol" if volatility >= 0.25 else "low_vol"
        return f"{trend}_{volatility_bucket}"

    def _iv_rank(self, history: list[dict[str, Any]]) -> float:
        """Calculate a deterministic IV-rank proxy without future observations.

        A supplied rank on the most recently completed bar wins.  Otherwise
        the percentile of rolling realized volatility is used.  The tie
        fallback intentionally treats stable low realized volatility as a
        low-IV environment, keeping synthetic data useful while remaining
        deterministic.
        """
        if not history:
            return 50.0
        supplied = history[-1].get("iv_rank")
        if supplied is not None:
            try:
                return max(0.0, min(100.0, float(supplied)))
            except (TypeError, ValueError):
                pass
        window = min(20, len(history))
        if len(history) < 3:
            return 50.0
        rolling: list[float] = []
        for end in range(window, len(history) + 1):
            value = self._volatility(history[:end])
            if value > 0:
                rolling.append(value)
        if not rolling:
            return 50.0
        current = rolling[-1]
        low, high = min(rolling), max(rolling)
        if high - low < 1e-9:
            return 20.0 if current < 0.25 else 80.0
        rank = sum(value <= current for value in rolling) / len(rolling) * 100.0
        return max(0.0, min(100.0, rank))

    def generate_signal(self, history: list[dict[str, Any]]) -> dict[str, Any]:
        """Generate one daily signal from bars ending on the prior day."""
        volatility = self._volatility(history)
        regime = self._regime(history, volatility)
        iv_rank = self._iv_rank(history)
        trend = regime.rsplit("_", 2)[0] if regime != "unknown" else "unknown"
        strategy_type: str | None = None
        if trend == "trending_up" and iv_rank < 30:
            strategy_type = "PUT_SPREAD"
        elif trend == "trending_down" and iv_rank < 30:
            strategy_type = "CALL_SPREAD"
        elif trend == "ranging" and iv_rank < 50:
            strategy_type = "IRON_CONDOR"
        return {
            "signal": "GO" if strategy_type else "NO_TRADE",
            "strategy_type": strategy_type,
            "regime": regime,
            "iv_rank": round(iv_rank, 6),
            "volatility": volatility,
        }

    def _strikes(self, spot: float, volatility: float) -> tuple[float, float, float, float]:
        # Delta is represented by a volatility-scaled distance, not by using
        # an option chain that could contain future observations.
        distance = max(self.config.wing_width, spot * volatility * sqrt(30 / 365) * 0.85)
        step = max(50.0, round(distance / 50.0) * 50.0)
        short_put = spot - step
        short_call = spot + step
        return short_put - self.config.wing_width, short_put, short_call, short_call + self.config.wing_width

    def run(self, historical_data: Iterable[Any] | None = None) -> dict[str, Any]:
        source = self.config.data if historical_data is None else historical_data
        bars = normalize_bars(source) if source is not None else []
        used_fallback = not bars
        if used_fallback:
            bars = normalize_bars(synthetic_history())
        if self.config.start_date:
            bars = [bar for bar in bars if bar["date"] >= self.config.start_date]
        if self.config.end_date:
            bars = [bar for bar in bars if bar["date"] <= self.config.end_date]
        warmup = max(20, self.config.train_days)
        trades: list[dict[str, Any]] = []
        equity_curve = [{"date": bars[0]["date"].isoformat(), "equity": self.config.initial_capital}] if bars else []
        capital = float(self.config.initial_capital)
        index = warmup
        trade_number = 1
        while index < len(bars):
            # This is the only decision point.  Current data is excluded from
            # the signal and only supplies the executable entry spot.
            history = bars[:index]
            if (index - warmup) % max(1, self.config.entry_days) != 0:
                index += 1
                continue
            entry = bars[index]
            signal = self.generate_signal(history)
            if signal["signal"] != "GO":
                index += 1
                continue
            strategy_type = str(signal["strategy_type"])
            volatility = float(signal["volatility"])
            regime = str(signal["regime"])
            long_put, short_put, short_call, long_call = self._strikes(entry["close"], volatility)
            assert self.simulator is not None
            final_index = min(index + max(1, self.config.holding_days), len(bars) - 1)
            if final_index <= index:
                break
            result: dict[str, Any] = {}
            exit_index = final_index
            # Evaluate every completed bar after entry so a target/stop can
            # close the position before the scheduled time exit.
            for candidate_index in range(index + 1, final_index + 1):
                candidate = bars[candidate_index]
                common = {
                    "entry_spot": entry["close"],
                    "exit_spot": candidate["close"],
                    "days_held": candidate_index - index,
                    "days_to_expiry": 30,
                    "volatility": volatility,
                    "lot_size": self.config.lot_size,
                    "target_profit_pct": self.config.target_profit_pct,
                    "stop_loss_pct": self.config.stop_loss_pct,
                }
                if strategy_type == "PUT_SPREAD":
                    result = self.simulator.simulate_put_spread(
                        short_put=short_put, long_put=long_put, **common
                    )
                elif strategy_type == "CALL_SPREAD":
                    result = self.simulator.simulate_call_spread(
                        short_call=short_call, long_call=long_call, **common
                    )
                else:
                    result = self.simulator.simulate_iron_condor(
                        short_put=short_put,
                        long_put=long_put,
                        short_call=short_call,
                        long_call=long_call,
                        **common,
                    )
                exit_index = candidate_index
                if result.get("exit_reason") in {"target", "stop"} or candidate_index == final_index:
                    break
            exit_bar = bars[exit_index]
            trade = {
                "trade_number": trade_number,
                "symbol": self.config.symbol,
                "regime": regime,
                "strategy_type": strategy_type,
                "signal": signal["signal"],
                "iv_rank": signal["iv_rank"],
                "entry_date": entry["date"].isoformat(),
                "exit_date": exit_bar["date"].isoformat(),
                "entry_spot": entry["close"],
                "exit_spot": exit_bar["close"],
                "legs": result["legs"],
                "gross_pnl": result["gross_pnl"],
                "commission": result["commission"],
                "slippage": result["slippage"],
                "net_pnl": result["net_pnl"],
                "return_pct": result["net_pnl"] / max(capital, 1.0) * 100,
                "exit_reason": result.get("exit_reason", "time"),
            }
            for key in ("max_risk", "target_pnl", "stop_pnl"):
                if key in result:
                    trade[key] = result[key]
            capital += float(trade["net_pnl"])
            trades.append(trade)
            equity_curve.append({"date": exit_bar["date"].isoformat(), "equity": round(capital, 6)})
            trade_number += 1
            index = max(index + 1, exit_index + 1)
        metrics = calculate_metrics(trades, initial_capital=self.config.initial_capital)
        walk_forward = self._walk_forward(bars, trades)
        return {
            "status": "completed",
            "symbol": self.config.symbol,
            "configuration": self.config.as_dict(),
            "metrics": metrics,
            "equity_curve": equity_curve,
            "walk_forward": walk_forward,
            "regime_stats": calculate_regime_stats(trades, initial_capital=self.config.initial_capital),
            "trades": trades,
            "warning": (
                "Using deterministic synthetic fallback history; results are illustrative, not historical"
                if used_fallback
                else None
            ),
        }

    def _walk_forward(self, bars: list[dict[str, Any]], trades: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not bars:
            return []
        folds: list[dict[str, Any]] = []
        train, test = max(1, self.config.train_days), max(1, self.config.test_days)
        start = 0
        while start + train < len(bars):
            test_end = min(start + train + test, len(bars))
            test_start_date, test_end_date = bars[start + train]["date"], bars[test_end - 1]["date"]
            fold_trades = [
                trade
                for trade in trades
                if test_start_date.isoformat() <= trade["entry_date"] <= test_end_date.isoformat()
            ]
            folds.append(
                {
                    "fold": len(folds) + 1,
                    "train_start": bars[start]["date"].isoformat(),
                    "train_end": bars[start + train - 1]["date"].isoformat(),
                    "test_start": test_start_date.isoformat(),
                    "test_end": test_end_date.isoformat(),
                    "metrics": calculate_metrics(fold_trades, initial_capital=self.config.initial_capital),
                }
            )
            start += test
        return folds

    def run_walk_forward(self, historical_data: Iterable[Any] | None = None) -> dict[str, Any]:
        return self.run(historical_data)


def run_backtest(
    config: Mapping[str, Any] | BacktestConfig | None = None,
    historical_data: Iterable[Any] | None = None,
) -> dict[str, Any]:
    settings = config if isinstance(config, BacktestConfig) else BacktestConfig.from_mapping(config)
    return BacktestEngine(settings).run(historical_data)


__all__ = [
    "BacktestConfig",
    "BacktestEngine",
    "normalize_bars",
    "load_historical_data",
    "run_backtest",
    "synthetic_history",
]
