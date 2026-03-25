"""add enemy_encounters table

Revision ID: h2i3j4k5l6m7
Revises: 6dd1b9c3be01
Create Date: 2026-03-25 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "h2i3j4k5l6m7"
down_revision: str | Sequence[str] | None = "6dd1b9c3be01"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create enemy_encounters table."""
    op.create_table(
        "enemy_encounters",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "enemy_id",
            sa.Integer(),
            sa.ForeignKey("enemies.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "room_id",
            sa.Integer(),
            sa.ForeignKey("rooms.id"),
            nullable=False,
        ),
        sa.Column("condition", sa.String(length=500), server_default="", nullable=False),
        sa.Column("attacks", sa.String(length=500), server_default="", nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Drop enemy_encounters table."""
    op.drop_table("enemy_encounters")
