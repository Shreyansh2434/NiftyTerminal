"""Phase 4 safety-first execution, risk and observability API."""
from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.chart_data_engine import chart_data_engine
from app.services.compliance_engine import compliance_engine
from app.services.execution_engine import execution_engine
from app.services.portfolio_engine import portfolio_engine
from app.services.risk_engine import RiskEngine

router = APIRouter(tags=["phase4"])
risk_engine = RiskEngine()


class OrderRequest(BaseModel):
    symbol: str = "NIFTY"
    side: str = "BUY"
    quantity: int = Field(default=1, ge=1)
    price: float = Field(default=22184.6, gt=0)
    order_type: str = "MARKET"
    client_order_id: str | None = None


@router.get("/execution/preview")
async def execution_preview(symbol: str = "NIFTY", side: str = "BUY", quantity: int = 1, price: float = 22184.6) -> dict:
    return execution_engine.preview({"symbol": symbol, "side": side, "quantity": quantity, "price": price})


@router.post("/execution/paper")
async def paper_execution(order: OrderRequest) -> dict:
    result = execution_engine.execute_paper(order.model_dump())
    compliance_engine.record("paper_execution" if result["status"] == "filled" else "execution_rejected", result, correlation_id=order.client_order_id)
    return result


@router.get("/portfolio")
@router.get("/portfolio/risk")
async def portfolio(positions: str | None = None) -> dict:
    parsed = None
    if positions:
        parsed = [{"symbol": item.strip(), "quantity": 1, "price": 100.0} for item in positions.split(",") if item.strip()]
    return portfolio_engine.analyze(parsed)


@router.get("/risk")
async def risk() -> dict:
    return {"kill_switch": risk_engine.kill_switch_status(), "kelly_fraction": risk_engine.kelly_fraction(), "sample_position_size": risk_engine.size_for_risk(100000, 22184.6)}


@router.get("/chart-data")
@router.get("/chart/data")
async def chart_data(symbol: str = "NIFTY", points: int = 24) -> dict:
    return chart_data_engine.data(symbol, points)


@router.get("/audit")
@router.get("/audit/compliance")
async def audit() -> dict:
    return {"records": execution_engine.audit_records() + compliance_engine.records(), "count": len(execution_engine.audit_records()) + len(compliance_engine.records())}


@router.get("/compliance")
async def compliance() -> dict:
    return compliance_engine.summary()
