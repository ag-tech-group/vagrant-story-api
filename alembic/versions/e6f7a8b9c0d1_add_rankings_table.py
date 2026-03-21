"""add rankings table

Revision ID: e6f7a8b9c0d1
Revises: d5e6f7a8b9c0
Create Date: 2026-03-21 02:02:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e6f7a8b9c0d1"
down_revision: str | Sequence[str] | None = "d5e6f7a8b9c0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (level, name, requirement)
RANKINGS = [
    (1, "Normal Agent", "0 Points"),
    (2, "Gladiator", "500,000 Points"),
    (3, "Daredevil", "1,000,000 Points"),
    (4, "Berserker", "2,000,000 Points"),
    (5, "Destroyer", "3,000,000 Points"),
    (6, "Spectrebane", "4,000,000 Points"),
    (7, "Paladin", "5,000,000 Points"),
    (8, "Mystic Wanderer", "8,000,000 Points"),
    (9, "Blade Master", "12,000,000 Points"),
    (10, "Master Gladiator", "16,000,000 Points"),
    (11, "Courageous Adventurer", "24,000,000 Points"),
    (12, "Dragon Slayer", "32,000,000 Points"),
    (13, "Raging Berserker", "40,000,000 Points"),
    (14, "Radiant Knight", "60,000,000 Points + 8 Titles"),
    (15, "Grand Paladin", "75,000,000 Points + 12 Titles"),
    (16, "Grand Master Breaker", "100,000,000 Points + 16 Titles"),
]


def upgrade() -> None:
    """Create rankings table and populate with data."""
    op.create_table(
        "rankings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("requirement", sa.String(length=200), server_default="", nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    for level, name, requirement in RANKINGS:
        op.execute(
            f"INSERT INTO rankings (level, name, requirement) "
            f"VALUES ({level}, '{name}', '{requirement}')"
        )


def downgrade() -> None:
    """Drop rankings table."""
    op.drop_table("rankings")
