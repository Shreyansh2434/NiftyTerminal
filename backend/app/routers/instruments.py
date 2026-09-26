from fastapi import APIRouter

from app.models.instruments import InstrumentsResponse
from app.services.instruments import get_instruments

router = APIRouter(prefix="/instruments", tags=["instruments"])


@router.get("", response_model=InstrumentsResponse, name="instruments")
async def instruments() -> InstrumentsResponse:
    return InstrumentsResponse(instruments=get_instruments())
