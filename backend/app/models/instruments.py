from pydantic import BaseModel, Field


class Instrument(BaseModel):
    symbol: str
    name: str
    kind: str = "index"
    active: bool = True


class InstrumentsResponse(BaseModel):
    instruments: list[Instrument] = Field(default_factory=list)
