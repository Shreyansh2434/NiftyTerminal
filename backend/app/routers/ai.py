"""Phase 6 offline-first copilot API."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.db.database import optional_session
from app.schemas.ai import AnalogueRequest, CopilotQueryRequest, FinSQLRequest, ToolRequest
from app.services.fin_sql import ReadOnlySQLError, fin_sql
from app.services.ai_copilot import ai_copilot
from app.services.analogue_engine import analogue_engine

router = APIRouter(prefix="/ai", tags=["phase6-ai"])


@router.get("/tools")
async def tools() -> dict:
    return {"tools": sorted(ai_copilot.tools()), "live_trading": False, "source": "offline-deterministic"}


@router.get("/copilot")
async def copilot(symbol: str = "NIFTY") -> dict:
    return ai_copilot.snapshot(symbol)


@router.post("/copilot/query")
async def copilot_query(request: CopilotQueryRequest) -> dict:
    return ai_copilot.answer(request.query, request.symbol)


@router.post("/fin-sql")
async def financial_sql(request: FinSQLRequest) -> dict:
    try:
        generated = fin_sql.generate(request.query)
    except ReadOnlySQLError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not request.execute:
        return {**generated, "executed": False, "message": "SQL generated; execution is opt-in"}
    async with optional_session() as session:
        if session is None:
            raise HTTPException(status_code=503, detail="Database is unavailable; SQL was not executed")
        try:
            result = await session.execute(text(generated["sql"]), generated["parameters"])
            rows = [dict(row) for row in result.mappings().all()]
        except Exception as exc:
            raise HTTPException(status_code=422, detail="Read-only query could not execute") from exc
    return {**generated, "executed": True, "rows": rows, "sample_size": len(rows)}


@router.post("/tool")
async def call_tool(request: ToolRequest) -> dict:
    try:
        return {"tool": request.tool, "result": ai_copilot.call_tool(request.tool, **request.arguments)}
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/quote/{symbol}")
async def quote(symbol: str = "NIFTY") -> dict:
    return ai_copilot.quote(symbol)


@router.get("/options/{symbol}")
async def options(symbol: str = "NIFTY", strikes: int = 5) -> dict:
    return ai_copilot.options(symbol, strikes)


@router.post("/backtest")
async def backtest(arguments: dict | None = None) -> dict:
    return ai_copilot.backtest(**(arguments or {}))


@router.post("/monte-carlo")
async def monte_carlo(arguments: dict | None = None) -> dict:
    return ai_copilot.monte_carlo(**(arguments or {}))


@router.post("/analogues")
async def analogues(request: AnalogueRequest) -> dict:
    return {"matches": analogue_engine.find(request.current, request.history, request.limit), "source": "offline-deterministic"}
