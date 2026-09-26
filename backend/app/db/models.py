from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Integer, Numeric, String, Text, Float, Boolean, JSON, TypeDecorator, func
from sqlalchemy.dialects.postgresql import JSONB as PostgresJSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class PortableJSON(TypeDecorator):
    """Use JSONB on PostgreSQL and JSON on local SQLite smoke databases."""

    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(PostgresJSONB() if dialect.name == "postgresql" else JSON())


class MarketSnapshot(Base):
    __tablename__ = "market_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), index=True)
    spot: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    change: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    change_percent: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    payload: Mapped[dict] = mapped_column(PortableJSON, default=dict)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


class OptionChainSnapshot(Base):
    __tablename__ = "option_chain_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), index=True)
    expiry: Mapped[str | None] = mapped_column(String(20), nullable=True)
    payload: Mapped[dict] = mapped_column(PortableJSON, default=dict)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


class SignalSnapshot(Base):
    __tablename__ = "signal_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), index=True)
    signal: Mapped[str] = mapped_column(String(30))
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(6, 3), nullable=True)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    payload: Mapped[dict] = mapped_column(PortableJSON, default=dict)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


class OHLCV(Base):
    """Daily or intraday OHLCV history used by backfill jobs."""

    __tablename__ = "ohlcv"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), index=True)
    interval: Mapped[str] = mapped_column(String(20), default="1d")
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    open: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    high: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    low: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    close: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    volume: Mapped[int | None] = mapped_column(Integer, nullable=True)


class OptionsChain(Base):
    """Persisted normalized option-chain snapshot."""

    __tablename__ = "options_chain"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), index=True)
    expiry: Mapped[str | None] = mapped_column(String(20), nullable=True)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    payload: Mapped[dict] = mapped_column(PortableJSON, default=dict)


class IVHistory(Base):
    """Historical implied-volatility observations."""

    __tablename__ = "iv_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), index=True)
    expiry: Mapped[str | None] = mapped_column(String(20), nullable=True)
    strike: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    call_iv: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    put_iv: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


class BacktestConfiguration(Base):
    """Saved, reproducible parameters for an options backtest."""

    __tablename__ = "backtest_configuration"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    symbol: Mapped[str] = mapped_column(String(20), default="NIFTY")
    parameters: Mapped[dict] = mapped_column(PortableJSON, default=dict)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class BacktestRun(Base):
    """A completed or in-progress backtest and its derived result payload."""

    __tablename__ = "backtest_run"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    configuration_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    symbol: Mapped[str] = mapped_column(String(20), default="NIFTY")
    status: Mapped[str] = mapped_column(String(20), default="completed", index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    initial_capital: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("100000"))
    parameters: Mapped[dict] = mapped_column(PortableJSON, default=dict)
    metrics: Mapped[dict] = mapped_column(PortableJSON, default=dict)
    equity_curve: Mapped[list] = mapped_column(PortableJSON, default=list)
    walk_forward: Mapped[list] = mapped_column(PortableJSON, default=list)
    regime_stats: Mapped[dict] = mapped_column(PortableJSON, default=dict)
    warning: Mapped[str | None] = mapped_column(Text, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)


class BacktestTrade(Base):
    """One strategy round trip produced by a backtest run."""

    __tablename__ = "backtest_trades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[str] = mapped_column(String(36), index=True)
    trade_number: Mapped[int] = mapped_column(Integer)
    symbol: Mapped[str] = mapped_column(String(20), default="NIFTY")
    regime: Mapped[str | None] = mapped_column(String(30), nullable=True)
    strategy_type: Mapped[str] = mapped_column(String(30), default="IRON_CONDOR")
    entry_date: Mapped[date] = mapped_column(Date, index=True)
    exit_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    entry_spot: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    exit_spot: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    legs: Mapped[list] = mapped_column(PortableJSON, default=list)
    gross_pnl: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("0"))
    commission: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("0"))
    slippage: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("0"))
    net_pnl: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("0"))
    return_pct: Mapped[Decimal] = mapped_column(Numeric(12, 6), default=Decimal("0"))
    exit_reason: Mapped[str | None] = mapped_column(String(40), nullable=True)


# Compatibility spelling used by an early Phase 2 draft.
BacktestTrades = BacktestTrade


# Phase 3 multi-asset persistence.  JSON is used rather than JSONB for these
# tables so local SQLite smoke tests and PostgreSQL deployments share a schema.
class MarketAsset(Base):
    __tablename__ = "market_assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    exchange: Mapped[str] = mapped_column(String(20), default="NSE")
    asset_class: Mapped[str] = mapped_column(String(30), default="EQUITY")
    sector: Mapped[str] = mapped_column(String(80), default="INDEX")
    currency: Mapped[str] = mapped_column(String(8), default="INR")
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class OHLCVMultiAsset(Base):
    __tablename__ = "ohlcv_multi_asset"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    interval: Mapped[str] = mapped_column(String(12), default="1d")
    open: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    high: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    low: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    close: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    volume: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source: Mapped[str] = mapped_column(String(30), default="offline")


class MarketSentiment(Base):
    __tablename__ = "market_sentiment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    label: Mapped[str] = mapped_column(String(20), default="NEUTRAL")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    headlines: Mapped[list] = mapped_column(JSON, default=list)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


class SectorPerformance(Base):
    __tablename__ = "sector_performance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sector: Mapped[str] = mapped_column(String(80), index=True)
    return_pct: Mapped[float] = mapped_column(Float, default=0.0)
    advance_count: Mapped[int] = mapped_column(Integer, default=0)
    decline_count: Mapped[int] = mapped_column(Integer, default=0)
    constituents: Mapped[list] = mapped_column(JSON, default=list)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


class MultiAssetBacktest(Base):
    __tablename__ = "backtests_multi_asset"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    strategy: Mapped[str] = mapped_column(String(80), default="equal_weight_momentum")
    symbols: Mapped[list] = mapped_column(JSON, default=list)
    parameters: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(20), default="completed", index=True)
    metrics: Mapped[dict] = mapped_column(JSON, default=dict)
    per_asset: Mapped[dict] = mapped_column(JSON, default=dict)
    per_sector: Mapped[dict] = mapped_column(JSON, default=dict)
    per_regime: Mapped[dict] = mapped_column(JSON, default=dict)
    equity_curve: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# Naming aliases used by API-facing Phase 3 integrations.
OhlcvMultiAsset = OHLCVMultiAsset
BacktestsMultiAsset = MultiAssetBacktest


class ExecutionHistory(Base):
    """Immutable execution intent/result record.  Paper executions are the default."""

    __tablename__ = "execution_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_order_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    side: Mapped[str] = mapped_column(String(8))
    quantity: Mapped[int] = mapped_column(Integer)
    order_type: Mapped[str] = mapped_column(String(20), default="MARKET")
    limit_price: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    mode: Mapped[str] = mapped_column(String(12), default="paper")
    status: Mapped[str] = mapped_column(String(20), default="accepted", index=True)
    average_price: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    risk_checks: Mapped[dict] = mapped_column(PortableJSON, default=dict)
    response: Mapped[dict] = mapped_column(PortableJSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


class AuditLog(Base):
    """Append-only audit trail for user and system actions."""

    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_type: Mapped[str] = mapped_column(String(60), index=True)
    actor: Mapped[str] = mapped_column(String(120), default="system")
    correlation_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    payload: Mapped[dict] = mapped_column(PortableJSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


class Phase4MarketSnapshot(Base):
    """Normalized market snapshot used by chart and execution safety services."""

    __tablename__ = "market_snapshot"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    last_price: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    bid: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    ask: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    volume: Mapped[int] = mapped_column(Integer, default=0)
    payload: Mapped[dict] = mapped_column(PortableJSON, default=dict)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


class VolumeProfile(Base):
    """Persisted price-bucket volume profile and order-flow summary."""

    __tablename__ = "volume_profile"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    interval: Mapped[str] = mapped_column(String(20), default="1d")
    bins: Mapped[list] = mapped_column(PortableJSON, default=list)
    point_of_control: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    value_area_low: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    value_area_high: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


# Explicit Phase 4 aliases keep both descriptive and specification spellings available.
MarketSnapshotPhase4 = Phase4MarketSnapshot
