from pydantic import BaseModel, Field

from app.models.common import ApiMeta


class OptionsResponse(BaseModel):
    symbol: str = "NIFTY"
    expiry: str | None = None
    spot: float | None = None
    rows: list[dict] = Field(default_factory=list)
    expiries: list[str] = Field(default_factory=list)
    meta: ApiMeta
