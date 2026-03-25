"""add encounter_drops table

Revision ID: i3j4k5l6m7n8
Revises: h2i3j4k5l6m7
Create Date: 2026-03-25 14:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "i3j4k5l6m7n8"
down_revision: str | Sequence[str] | None = "h2i3j4k5l6m7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create encounter_drops table."""
    op.create_table(
        "encounter_drops",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "encounter_id",
            sa.Integer(),
            sa.ForeignKey("enemy_encounters.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("body_part", sa.String(length=50), nullable=False),
        sa.Column("item", sa.String(length=100), nullable=False),
        sa.Column("material", sa.String(length=50), server_default="", nullable=False),
        sa.Column("drop_chance", sa.String(length=50), nullable=False),
        sa.Column("drop_value", sa.Integer(), server_default="0", nullable=False),
        sa.Column("grip", sa.String(length=100), server_default="", nullable=False),
        sa.Column("quantity", sa.Integer(), server_default="1", nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Drop encounter_drops table."""
    op.drop_table("encounter_drops")
