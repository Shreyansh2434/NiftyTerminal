from app.models.instruments import Instrument


def get_instruments() -> list[Instrument]:
    return [
        Instrument(symbol="NIFTY", name="NIFTY 50", kind="index"),
        Instrument(symbol="BANKNIFTY", name="NIFTY Bank", kind="index"),
        Instrument(symbol="FINNIFTY", name="NIFTY Financial Services", kind="index"),
    ]
