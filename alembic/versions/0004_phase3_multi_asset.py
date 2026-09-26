"""Phase 3 multi-asset market intelligence tables."""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0004_phase3_multi_asset"
down_revision: Union[str, None] = "0003_strategy_type"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "market_assets",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("symbol", sa.String(32), nullable=False, unique=True),
        sa.Column("name", sa.String(120), nullable=False), sa.Column("exchange", sa.String(20), server_default="NSE"),
        sa.Column("asset_class", sa.String(30), server_default="EQUITY"), sa.Column("sector", sa.String(80), server_default="INDEX"),
        sa.Column("currency", sa.String(8), server_default="INR"), sa.Column("active", sa.Boolean(), server_default=sa.true()),
        sa.Column("metadata", sa.JSON(), server_default="{}"), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_market_assets_symbol", "market_assets", ["symbol"])
    op.create_table(
        "ohlcv_multi_asset", sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("symbol", sa.String(32), nullable=False), sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("interval", sa.String(12), server_default="1d"), sa.Column("open", sa.Numeric(18, 6)),
        sa.Column("high", sa.Numeric(18, 6)), sa.Column("low", sa.Numeric(18, 6)), sa.Column("close", sa.Numeric(18, 6)),
        sa.Column("volume", sa.Integer()), sa.Column("source", sa.String(30), server_default="offline"),
    )
    op.create_index("ix_ohlcv_multi_asset_symbol", "ohlcv_multi_asset", ["symbol"])
    op.create_index("ix_ohlcv_multi_asset_timestamp", "ohlcv_multi_asset", ["timestamp"])
    op.create_table(
        "market_sentiment", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("symbol", sa.String(32), nullable=False),
        sa.Column("score", sa.Float(), server_default="0"), sa.Column("label", sa.String(20), server_default="NEUTRAL"),
        sa.Column("confidence", sa.Float(), server_default="0"), sa.Column("headlines", sa.JSON(), server_default="[]"),
        sa.Column("captured_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "sector_performance", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("sector", sa.String(80), nullable=False),
        sa.Column("return_pct", sa.Float(), server_default="0"), sa.Column("advance_count", sa.Integer(), server_default="0"),
        sa.Column("decline_count", sa.Integer(), server_default="0"), sa.Column("constituents", sa.JSON(), server_default="[]"),
        sa.Column("captured_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "backtests_multi_asset", sa.Column("id", sa.String(36), primary_key=True), sa.Column("strategy", sa.String(80), server_default="equal_weight_momentum"),
        sa.Column("symbols", sa.JSON(), server_default="[]"), sa.Column("parameters", sa.JSON(), server_default="{}"),
        sa.Column("status", sa.String(20), server_default="completed"), sa.Column("metrics", sa.JSON(), server_default="{}"),
        sa.Column("per_asset", sa.JSON(), server_default="{}"), sa.Column("per_sector", sa.JSON(), server_default="{}"),
        sa.Column("per_regime", sa.JSON(), server_default="{}"), sa.Column("equity_curve", sa.JSON(), server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    for table in ("backtests_multi_asset", "sector_performance", "market_sentiment", "ohlcv_multi_asset", "market_assets"):
        op.drop_table(table)
