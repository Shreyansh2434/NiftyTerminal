from typing import Any

from app.services.market_data import market_data


async def get_iv(symbol: str = "NIFTY") -> dict[str, Any]:
    data = await market_data.fetch_chain(symbol)
    rows = data.get("rows", [])
    points = [
        {
            "strike": row["strike"],
            "call_iv": row.get("call_iv"),
            "put_iv": row.get("put_iv"),
        }
        for row in rows
        if row.get("call_iv") is not None or row.get("put_iv") is not None
    ]
    values = [
        value
        for point in points
        for value in (point.get("call_iv"), point.get("put_iv"))
        if value is not None
    ]
    spot = data.get("spot")
    atm_point = min(points, key=lambda point: abs(point["strike"] - spot)) if points and spot is not None else None
    return {
        **data,
        "atm_iv": (
            round(sum(value for value in (atm_point.get("call_iv"), atm_point.get("put_iv")) if value is not None) / len([value for value in (atm_point.get("call_iv"), atm_point.get("put_iv")) if value is not None]), 2)
            if atm_point and any(value is not None for value in (atm_point.get("call_iv"), atm_point.get("put_iv")))
            else None
        ),
        "call_iv": _mean(row.get("call_iv") for row in rows),
        "put_iv": _mean(row.get("put_iv") for row in rows),
        "points": points,
    }


def _mean(values: Any) -> float | None:
    valid = [float(value) for value in values if value is not None]
    return round(sum(valid) / len(valid), 2) if valid else None
