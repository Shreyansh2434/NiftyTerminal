"""Add Phase 2 backtest persistence and the sample configuration."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_backtest"
down_revision: Union[str, None] = "0001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "backtest_configuration",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False, unique=True),
        sa.Column("symbol", sa.String(20), nullable=False, server_default="NIFTY"),
        sa.Column("parameters", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("description", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_backtest_configuration_name", "backtest_configuration", ["name"])
    op.create_table(
        "backtest_run",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("configuration_id", sa.Integer()),
        sa.Column("symbol", sa.String(20), nullable=False, server_default="NIFTY"),
        sa.Column("status", sa.String(20), nullable=False, server_default="completed"),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("start_date", sa.DateTime(timezone=True)),
        sa.Column("end_date", sa.DateTime(timezone=True)),
        sa.Column("initial_capital", sa.Numeric(18, 4), nullable=False, server_default="100000"),
        sa.Column("parameters", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("metrics", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("equity_curve", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("walk_forward", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("regime_stats", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("warning", sa.Text()),
        sa.Column("error", sa.Text()),
    )
    op.create_index("ix_backtest_run_configuration_id", "backtest_run", ["configuration_id"])
    op.create_index("ix_backtest_run_status", "backtest_run", ["status"])
    op.create_table(
        "backtest_trades",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("run_id", sa.String(36), nullable=False),
        sa.Column("trade_number", sa.Integer(), nullable=False),
        sa.Column("symbol", sa.String(20), nullable=False, server_default="NIFTY"),
        sa.Column("regime", sa.String(30)),
        sa.Column("entry_date", sa.Date(), nullable=False),
        sa.Column("exit_date", sa.Date()),
        sa.Column("entry_spot", sa.Numeric(14, 4)),
        sa.Column("exit_spot", sa.Numeric(14, 4)),
        sa.Column("legs", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("gross_pnl", sa.Numeric(18, 4), nullable=False, server_default="0"),
        sa.Column("commission", sa.Numeric(18, 4), nullable=False, server_default="0"),
        sa.Column("slippage", sa.Numeric(18, 4), nullable=False, server_default="0"),
        sa.Column("net_pnl", sa.Numeric(18, 4), nullable=False, server_default="0"),
        sa.Column("return_pct", sa.Numeric(12, 6), nullable=False, server_default="0"),
        sa.Column("exit_reason", sa.String(40)),
    )
    op.create_index("ix_backtest_trades_run_id", "backtest_trades", ["run_id"])
    op.create_index("ix_backtest_trades_entry_date", "backtest_trades", ["entry_date"])
    op.bulk_insert(
        sa.table(
            "backtest_configuration",
            sa.column("name", sa.String),
            sa.column("symbol", sa.String),
            sa.column("parameters", sa.JSON),
            sa.column("description", sa.Text),
        ),
        [
            {
                "name": "NIFTY Iron Condor — Balanced",
                "symbol": "NIFTY",
                "parameters": {
                    "initial_capital": 100000,
                    "lot_size": 50,
                    "entry_days": 5,
                    "holding_days": 5,
                    "short_delta": 0.16,
                    "wing_width": 150,
                    "commission_per_contract": 20,
                    "slippage_bps": 4,
                    "spread_bps": 10,
                    "train_days": 126,
                    "test_days": 63,
                },
                "description": "Conservative walk-forward iron-condor sample",
            }
        ],
    )


def downgrade() -> None:
    op.drop_index("ix_backtest_trades_entry_date", table_name="backtest_trades")
    op.drop_index("ix_backtest_trades_run_id", table_name="backtest_trades")
    op.drop_table("backtest_trades")
    op.drop_index("ix_backtest_run_status", table_name="backtest_run")
    op.drop_index("ix_backtest_run_configuration_id", table_name="backtest_run")
    op.drop_table("backtest_run")
    op.drop_index("ix_backtest_configuration_name", table_name="backtest_configuration")
    op.drop_table("backtest_configuration")
