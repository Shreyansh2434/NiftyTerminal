"""Compatibility exports for option-chain persistence models."""

from app.db.models import OptionChainSnapshot, OptionsChain

OptionChain = OptionsChain

__all__ = ["OptionChainSnapshot", "OptionsChain", "OptionChain"]
