from pydantic import BaseModel, Field

from app.models.common import ApiMeta


class NoTradeResponse(BaseModel):
    symbol: str = "NIFTY"
    no_trade: bool = True
    status: str = "NO_TRADE"
    reasons: list[str] = Field(default_factory=list)
    meta: ApiMeta
