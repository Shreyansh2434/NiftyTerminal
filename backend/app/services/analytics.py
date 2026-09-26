from collections.abc import Iterable


def calculate_pcr(rows: Iterable[dict]) -> float | None:
    call_oi = sum(max(0, int(row.get("call_oi", 0) or 0)) for row in rows)
    put_oi = sum(max(0, int(row.get("put_oi", 0) or 0)) for row in rows)
    return round(put_oi / call_oi, 3) if call_oi else None


def calculate_max_pain(rows: Iterable[dict]) -> tuple[float | None, dict[str, float]]:
    normalized = list(rows)
    if not normalized:
        return None, {}
    payouts: dict[str, float] = {}
    strikes = [float(row["strike"]) for row in normalized]
    for settlement in strikes:
        payout = 0.0
        for row in normalized:
            strike = float(row["strike"])
            payout += int(row.get("call_oi", 0) or 0) * max(0.0, settlement - strike)
            payout += int(row.get("put_oi", 0) or 0) * max(0.0, strike - settlement)
        payouts[str(settlement)] = round(payout, 2)
    return min(strikes, key=lambda strike: payouts[str(strike)]), payouts


def calculate_levels(rows: Iterable[dict]) -> dict[str, float | None]:
    normalized = list(rows)
    calls = [row for row in normalized if row.get("call_oi", 0)]
    puts = [row for row in normalized if row.get("put_oi", 0)]
    call_wall = max(calls, key=lambda row: row["call_oi"])["strike"] if calls else None
    put_wall = max(puts, key=lambda row: row["put_oi"])["strike"] if puts else None
    support = (
        round(sum(row["strike"] * row["put_oi"] for row in puts) / sum(row["put_oi"] for row in puts), 2)
        if puts
        else None
    )
    resistance = (
        round(sum(row["strike"] * row["call_oi"] for row in calls) / sum(row["call_oi"] for row in calls), 2)
        if calls
        else None
    )
    return {"call_wall": call_wall, "put_wall": put_wall, "support": support, "resistance": resistance}


def infer_bias(pcr: float | None) -> str:
    if pcr is None:
        return "NEUTRAL"
    if pcr >= 1.2:
        return "BULLISH"
    if pcr <= 0.8:
        return "BEARISH"
    return "NEUTRAL"
