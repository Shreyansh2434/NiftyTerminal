"""Resilient Phase 2 backtest API."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import BacktestConfiguration, BacktestRun, BacktestTrade
from app.schemas.backtest import (
    BacktestCompareResponse,
    BacktestRunRequest,
    BacktestRunResponse,
    BacktestTradeResponse,
)
from app.services.backtest_engine import load_historical_data, run_backtest

router = APIRouter(prefix="/backtest", tags=["backtest"])
_RUNS: dict[str, dict[str, Any]] = {}


def _dump(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        return value.model_dump()
    return value.dict()


def _response(run_id: str, result: dict[str, Any], started: datetime, warning: str | None = None) -> BacktestRunResponse:
    return BacktestRunResponse(
        run_id=run_id,
        status=result.get("status", "completed"),
        symbol=result.get("symbol", "NIFTY"),
        started_at=started,
        completed_at=datetime.now(timezone.utc),
        configuration=result.get("configuration", {}),
        metrics=result.get("metrics", {}),
        equity_curve=result.get("equity_curve", []),
        walk_forward=result.get("walk_forward", []),
        regime_stats=result.get("regime_stats", {}),
        trades_count=len(result.get("trades", [])),
        warning=warning or result.get("warning"),
        error=result.get("error"),
    )


async def _persist(
    session: AsyncSession | None,
    run_id: str,
    result: dict[str, Any],
    response: BacktestRunResponse,
    configuration_id: int | None,
) -> str | None:
    if session is None:
        return "Database unavailable; result retained in memory only"
    try:
        model = BacktestRun(
            id=run_id,
            configuration_id=configuration_id,
            symbol=response.symbol,
            status=response.status,
            started_at=response.started_at,
            completed_at=response.completed_at,
            initial_capital=response.configuration.get("initial_capital", 100000),
            parameters=response.configuration,
            metrics=response.metrics,
            equity_curve=response.equity_curve,
            walk_forward=response.walk_forward,
            regime_stats=response.regime_stats,
            warning=response.warning,
        )
        session.add(model)
        for trade in result.get("trades", []):
            trade_columns = {
                "trade_number",
                "symbol",
                "regime",
                "strategy_type",
                "entry_date",
                "exit_date",
                "entry_spot",
                "exit_spot",
                "legs",
                "gross_pnl",
                "commission",
                "slippage",
                "net_pnl",
                "return_pct",
                "exit_reason",
            }
            values = {key: value for key, value in trade.items() if key in trade_columns}
            for key in ("entry_date", "exit_date"):
                if isinstance(values.get(key), str):
                    from datetime import date

                    values[key] = date.fromisoformat(values[key])
            session.add(BacktestTrade(run_id=run_id, **values))
        await session.commit()
    except Exception:
        await session.rollback()
        return "Database write failed; result retained in memory only"
    return None


@router.post("/run", response_model=BacktestRunResponse)
async def create_backtest(
    payload: BacktestRunRequest | None = None,
    session: AsyncSession | None = Depends(get_db),
) -> BacktestRunResponse:
    payload = payload or BacktestRunRequest()
    values = _dump(payload)
    configuration_id = values.pop("configuration_id", None)
    if configuration_id is not None and session is not None:
        try:
            saved = await session.get(BacktestConfiguration, configuration_id)
            if saved:
                parameters = dict(saved.parameters or {})
                parameters.update({key: value for key, value in values.items() if value is not None})
                values = parameters
                values["symbol"] = saved.symbol
        except Exception:
            # A saved configuration is optional; the posted body remains valid.
            pass
    started = datetime.now(timezone.utc)
    run_id = str(uuid4())
    try:
        historical_data = values.get("data")
        if not historical_data:
            historical_data = await load_historical_data(
                session,
                symbol=values.get("symbol", "NIFTY"),
                start_date=values.get("start_date"),
                end_date=values.get("end_date"),
            )
        result = run_backtest(values, historical_data or None)
        warning = result.get("warning")
    except Exception as exc:  # API must remain usable when data is malformed/unavailable.
        result = {
            "status": "failed",
            "symbol": values.get("symbol", "NIFTY"),
            "configuration": values,
            "metrics": {},
            "equity_curve": [],
            "walk_forward": [],
            "regime_stats": {},
            "trades": [],
            "error": str(exc),
        }
        warning = "Backtest data unavailable"
    response = _response(run_id, result, started, warning)
    _RUNS[run_id] = {"response": response.model_dump(), "trades": result.get("trades", [])}
    persist_warning = await _persist(session, run_id, result, response, configuration_id)
    if persist_warning:
        response.warning = f"{response.warning}; {persist_warning}" if response.warning else persist_warning
        _RUNS[run_id]["response"] = response.model_dump()
    return response


def _from_memory(run_id: str) -> BacktestRunResponse | None:
    stored = _RUNS.get(run_id)
    return BacktestRunResponse(**stored["response"]) if stored else None


@router.get("/run/{run_id}", response_model=BacktestRunResponse)
async def get_backtest(run_id: str, session: AsyncSession | None = Depends(get_db)) -> BacktestRunResponse:
    memory = _from_memory(run_id)
    if memory:
        return memory
    if session is not None:
        try:
            model = await session.get(BacktestRun, run_id)
            if model:
                return BacktestRunResponse(
                    run_id=model.id,
                    status=model.status,
                    symbol=model.symbol,
                    started_at=model.started_at,
                    completed_at=model.completed_at,
                    configuration=model.parameters or {},
                    metrics=model.metrics or {},
                    equity_curve=model.equity_curve or [],
                    walk_forward=model.walk_forward or [],
                    regime_stats=model.regime_stats or {},
                    warning=model.warning,
                )
        except Exception:
            pass
    return BacktestRunResponse(run_id=run_id, status="unavailable", warning="Backtest run not found")


@router.get("/run/{run_id}/trades", response_model=list[BacktestTradeResponse])
async def get_backtest_trades(
    run_id: str,
    session: AsyncSession | None = Depends(get_db),
    limit: int = Query(1000, ge=1, le=5000),
) -> list[BacktestTradeResponse]:
    stored = _RUNS.get(run_id)
    if stored:
        return [BacktestTradeResponse(**trade) for trade in stored["trades"][:limit]]
    if session is not None:
        try:
            rows = (
                await session.execute(
                    select(BacktestTrade).where(BacktestTrade.run_id == run_id).order_by(BacktestTrade.trade_number).limit(limit)
                )
            ).scalars().all()
            return [
                BacktestTradeResponse(
                    id=row.id,
                    trade_number=row.trade_number,
                    symbol=row.symbol,
                    regime=row.regime or "unknown",
                    strategy_type=row.strategy_type or "IRON_CONDOR",
                    entry_date=row.entry_date,
                    exit_date=row.exit_date,
                    entry_spot=float(row.entry_spot) if row.entry_spot is not None else None,
                    exit_spot=float(row.exit_spot) if row.exit_spot is not None else None,
                    legs=row.legs or [],
                    gross_pnl=float(row.gross_pnl or 0),
                    commission=float(row.commission or 0),
                    slippage=float(row.slippage or 0),
                    net_pnl=float(row.net_pnl or 0),
                    return_pct=float(row.return_pct or 0),
                    exit_reason=row.exit_reason,
                )
                for row in rows
            ]
        except Exception:
            pass
    return []


@router.get("/compare", response_model=BacktestCompareResponse)
async def compare_backtests(
    run_ids: str | None = Query(None, description="Comma-separated run IDs"),
    session: AsyncSession | None = Depends(get_db),
) -> BacktestCompareResponse:
    ids = [item.strip() for item in (run_ids or "").split(",") if item.strip()]
    if not ids:
        ids = list(_RUNS)[-10:]
    runs: list[BacktestRunResponse] = []
    for run_id in ids:
        value = _from_memory(run_id)
        if value:
            runs.append(value)
    if not runs and session is not None:
        try:
            rows = (
                await session.execute(
                    select(BacktestRun).where(BacktestRun.id.in_(ids)).order_by(BacktestRun.completed_at.desc())
                )
            ).scalars().all()
            runs = [
                BacktestRunResponse(
                    run_id=row.id,
                    status=row.status,
                    symbol=row.symbol,
                    started_at=row.started_at,
                    completed_at=row.completed_at,
                    configuration=row.parameters or {},
                    metrics=row.metrics or {},
                    equity_curve=row.equity_curve or [],
                    walk_forward=row.walk_forward or [],
                    regime_stats=row.regime_stats or {},
                )
                for row in rows
            ]
        except Exception:
            pass
    warning = None if runs else "No backtest runs are available"
    return BacktestCompareResponse(runs=runs, warning=warning)


__all__ = ["router"]
