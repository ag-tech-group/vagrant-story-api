"""add enemy_drops table

Revision ID: 6dd1b9c3be01
Revises: b1b9e5ae3995
Create Date: 2026-03-25 01:20:22.478547

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6dd1b9c3be01"
down_revision: str | Sequence[str] | None = "b1b9e5ae3995"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create enemy_drops table."""
    op.create_table(
        "enemy_drops",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("enemy_id", sa.Integer(), nullable=False),
        sa.Column("body_part", sa.String(50), nullable=False),
        sa.Column("item", sa.String(100), nullable=False),
        sa.Column("material", sa.String(50), server_default="", nullable=False),
        sa.Column("drop_chance", sa.String(50), nullable=False),
        sa.Column("drop_value", sa.Integer(), server_default="0", nullable=False),
        sa.Column("grip", sa.String(100), server_default="", nullable=False),
        sa.Column("quantity", sa.Integer(), server_default="1", nullable=False),
        sa.ForeignKeyConstraint(["enemy_id"], ["enemies.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Drop enemy_drops table."""
    op.drop_table("enemy_drops")
