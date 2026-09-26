from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    database: bool
    market_data: str
    generated_at: datetime
    details: dict[str, Any] = Field(default_factory=dict)
