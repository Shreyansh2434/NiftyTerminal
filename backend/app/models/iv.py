from pydantic import BaseModel, Field

from app.models.common import ApiMeta


class IVPoint(BaseModel):
    strike: float
    call_iv: float | None = None
    put_iv: float | None = None


class IVResponse(BaseModel):
    symbol: str = "NIFTY"
    spot: float | None = None
    atm_iv: float | None = None
    call_iv: float | None = None
    put_iv: float | None = None
    points: list[IVPoint] = Field(default_factory=list)
    meta: ApiMeta
