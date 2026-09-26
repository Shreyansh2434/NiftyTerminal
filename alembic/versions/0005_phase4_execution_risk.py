"""Phase 4 execution, audit and chart analytics tables."""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0005_phase4_execution_risk"
down_revision: Union[str, None] = "0004_phase3_multi_asset"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "execution_history",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("client_order_id", sa.String(100), nullable=False, unique=True),
        sa.Column("symbol", sa.String(32), nullable=False),
        sa.Column("side", sa.String(8), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("order_type", sa.String(20), server_default="MARKET"),
        sa.Column("limit_price", sa.Numeric(18, 6)),
        sa.Column("mode", sa.String(12), server_default="paper"),
        sa.Column("status", sa.String(20), server_default="accepted"),
        sa.Column("average_price", sa.Numeric(18, 6)),
        sa.Column("risk_checks", sa.JSON(), server_default="{}"),
        sa.Column("response", sa.JSON(), server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_execution_history_symbol", "execution_history", ["symbol"])
    op.create_index("ix_execution_history_status", "execution_history", ["status"])
    op.create_table(
        "audit_log",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("event_type", sa.String(60), nullable=False),
        sa.Column("actor", sa.String(120), server_default="system"),
        sa.Column("correlation_id", sa.String(100)),
        sa.Column("payload", sa.JSON(), server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_audit_log_event_type", "audit_log", ["event_type"])
    op.create_table(
        "market_snapshot",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("symbol", sa.String(32), nullable=False),
        sa.Column("last_price", sa.Numeric(18, 6), nullable=False),
        sa.Column("bid", sa.Numeric(18, 6)), sa.Column("ask", sa.Numeric(18, 6)),
        sa.Column("volume", sa.Integer(), server_default="0"), sa.Column("payload", sa.JSON(), server_default="{}"),
        sa.Column("captured_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_market_snapshot_symbol", "market_snapshot", ["symbol"])
    op.create_table(
        "volume_profile",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("symbol", sa.String(32), nullable=False), sa.Column("interval", sa.String(20), server_default="1d"),
        sa.Column("bins", sa.JSON(), server_default="[]"), sa.Column("point_of_control", sa.Numeric(18, 6)),
        sa.Column("value_area_low", sa.Numeric(18, 6)), sa.Column("value_area_high", sa.Numeric(18, 6)),
        sa.Column("captured_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_volume_profile_symbol", "volume_profile", ["symbol"])


def downgrade() -> None:
    for table in ("volume_profile", "market_snapshot", "audit_log", "execution_history"):
        op.drop_table(table)
