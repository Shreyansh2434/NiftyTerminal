from fastapi import APIRouter

from app.schemas import StatusResponse
from app.services.health import get_health, get_readiness

router = APIRouter(tags=["health"])


@router.get("/health", response_model=StatusResponse)
async def health() -> StatusResponse:
    return StatusResponse(**await get_health())


@router.get("/ready")
async def readiness() -> dict:
    return await get_readiness()
