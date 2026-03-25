"""add enemies and enemy_body_parts tables

Revision ID: g1h2i3j4k5l6
Revises: c2d3e4f5a6b7
Create Date: 2026-03-24 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "g1h2i3j4k5l6"
down_revision: str | Sequence[str] | None = "c2d3e4f5a6b7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create enemies and enemy_body_parts tables."""
    op.create_table(
        "enemies",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("enemy_class", sa.String(length=50), nullable=False),
        sa.Column("hp", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("mp", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("str", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("int", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("agi", sa.Integer(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "enemy_body_parts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "enemy_id",
            sa.Integer(),
            sa.ForeignKey("enemies.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("physical", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("air", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("fire", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("earth", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("water", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("light", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("dark", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("blunt", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("edged", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("piercing", sa.Integer(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Drop enemy_body_parts and enemies tables."""
    op.drop_table("enemy_body_parts")
    op.drop_table("enemies")
