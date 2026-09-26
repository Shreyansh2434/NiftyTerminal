"""Store the selected Phase 2 strategy on each trade."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0003_strategy_type"
down_revision: Union[str, None] = "0002_backtest"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "backtest_trades",
        sa.Column("strategy_type", sa.String(30), nullable=False, server_default="IRON_CONDOR"),
    )


def downgrade() -> None:
    op.drop_column("backtest_trades", "strategy_type")
