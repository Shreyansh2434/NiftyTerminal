from uuid import uuid4

from fastapi import APIRouter

from app.services.market_data_aggregator import market_data_aggregator
from app.services.multi_asset_backtest_engine import multi_asset_backtest_engine

router = APIRouter(tags=["phase3-backtests"])
_runs: dict[str, dict] = {}


@router.post("/run")
async def run_backtest(payload: dict | None = None) -> dict:
    payload = payload or {}
    symbols = payload.get("symbols")
    history = await market_data_aggregator.history(symbols, int(payload.get("days", 180)))
    assets = await market_data_aggregator.list_assets()
    sector_map = {asset["symbol"]: asset["sector"] for asset in assets}
    parameters = {**payload, "sector_map": sector_map}
    result = multi_asset_backtest_engine.run(
        history, float(payload.get("initial_capital", 100000)),
        str(payload.get("strategy", "equal_weight_momentum")), parameters,
    )
    run_id = str(uuid4())
    result["run_id"] = run_id
    _runs[run_id] = result
    return result


@router.get("/run/{run_id}")
async def get_backtest(run_id: str) -> dict:
    return _runs.get(run_id, {"run_id": run_id, "status": "not_found"})


@router.get("/runs")
async def list_backtests() -> dict:
    return {"runs": list(_runs.values())}
