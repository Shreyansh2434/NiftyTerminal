from datetime import datetime

from pydantic import BaseModel


class ApiMeta(BaseModel):
    source: str = "empty"
    cached: bool = False
    generated_at: datetime
    warning: str | None = None
