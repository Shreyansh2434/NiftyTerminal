from pydantic import BaseModel

from app.models.common import ApiMeta


class RegimeResponse(BaseModel):
    symbol: str = "NIFTY"
    regime: str = "NEUTRAL"
    bias: str = "NEUTRAL"
    score: float = 0.0
    rationale: str = "Insufficient market data for a directional regime."
    meta: ApiMeta
