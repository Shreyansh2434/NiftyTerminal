"""Create the application persistence tables."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ohlcv",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("symbol", sa.String(length=20), nullable=False),
        sa.Column("interval", sa.String(length=20), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("open", sa.Numeric(14, 4)),
        sa.Column("high", sa.Numeric(14, 4)),
        sa.Column("low", sa.Numeric(14, 4)),
        sa.Column("close", sa.Numeric(14, 4)),
        sa.Column("volume", sa.Integer()),
    )
    op.create_index("ix_ohlcv_symbol", "ohlcv", ["symbol"])
    op.create_index("ix_ohlcv_timestamp", "ohlcv", ["timestamp"])
    op.create_table(
        "options_chain",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("symbol", sa.String(length=20), nullable=False),
        sa.Column("expiry", sa.String(length=20)),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
    )
    op.create_index("ix_options_chain_symbol", "options_chain", ["symbol"])
    op.create_index("ix_options_chain_captured_at", "options_chain", ["captured_at"])
    op.create_table(
        "iv_history",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("symbol", sa.String(length=20), nullable=False),
        sa.Column("expiry", sa.String(length=20)),
        sa.Column("strike", sa.Numeric(14, 4)),
        sa.Column("call_iv", sa.Numeric(10, 4)),
        sa.Column("put_iv", sa.Numeric(10, 4)),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_iv_history_symbol", "iv_history", ["symbol"])
    op.create_index("ix_iv_history_captured_at", "iv_history", ["captured_at"])


def downgrade() -> None:
    op.drop_index("ix_iv_history_captured_at", table_name="iv_history")
    op.drop_index("ix_iv_history_symbol", table_name="iv_history")
    op.drop_table("iv_history")
    op.drop_index("ix_options_chain_captured_at", table_name="options_chain")
    op.drop_index("ix_options_chain_symbol", table_name="options_chain")
    op.drop_table("options_chain")
    op.drop_index("ix_ohlcv_timestamp", table_name="ohlcv")
    op.drop_index("ix_ohlcv_symbol", table_name="ohlcv")
    op.drop_table("ohlcv")
