"""Lightweight Phase 2 validation when a project test runner is unavailable."""

from datetime import date, timedelta

from app.services.backtest_engine import run_backtest
from app.services.metrics_calculator import calculate_metrics
from app.services.price_simulator import PriceSimulator


def main() -> None:
    start = date(2024, 1, 1)

    # A high-IV trend must not open a position even though its regime is
    # otherwise eligible for a directional spread.
    no_trade_history = [
        {
            "date": start + timedelta(days=i),
            "close": 22000 + i * 35,
            "iv_rank": 80,
        }
        for i in range(70)
    ]
    no_trade = run_backtest({"train_days": 20, "test_days": 10}, no_trade_history)
    assert no_trade["trades"] == []

    # Explicit historical IV ranks make this smoke check independent of a
    # vendor.  The engine still reads the rank from the prior bar only.
    history = []
    value = 22000.0
    for i in range(30):
        value += 35
        history.append({"date": start + timedelta(days=i), "close": value, "iv_rank": 20})
    for i in range(30, 60):
        value -= 35
        history.append({"date": start + timedelta(days=i), "close": value, "iv_rank": 20})
    for i in range(60, 100):
        value += 2 if i % 2 else -2
        history.append({"date": start + timedelta(days=i), "close": value, "iv_rank": 40})
    result = run_backtest({"train_days": 20, "test_days": 10, "entry_days": 5, "holding_days": 2}, history)
    assert result["status"] == "completed"
    assert result["metrics"]["total_trades"] == len(result["trades"])
    assert result["walk_forward"]
    strategy_types = {trade["strategy_type"] for trade in result["trades"]}
    assert {"PUT_SPREAD", "CALL_SPREAD", "IRON_CONDOR"} <= strategy_types
    assert all(trade["exit_reason"] in {"target", "stop", "time"} for trade in result["trades"])
    assert calculate_metrics([{"net_pnl": 10}, {"net_pnl": -5}])["total_pnl"] == 5
    fill = PriceSimulator(commission_per_contract=20).simulate_iron_condor(
        entry_spot=22000,
        exit_spot=22000,
        short_put=21800,
        long_put=21650,
        short_call=22200,
        long_call=22350,
    )
    assert fill["commission"] == 160
    assert fill["net_pnl"] <= fill["gross_pnl"]
    spread = PriceSimulator(commission_per_contract=20).simulate_put_spread(
        entry_spot=22000,
        exit_spot=22000,
        short_put=21800,
        long_put=21650,
        stop_loss_pct=0.35,
    )
    assert spread["max_risk"] > 0
    assert spread["exit_reason"] in {"target", "stop", "time"}
    print("Phase 2 backtest smoke validation passed")


if __name__ == "__main__":
    main()
