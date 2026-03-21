"""add hands column to blades

Revision ID: 292babe4c51e
Revises: 0b7ab1be21e2
Create Date: 2026-03-20 23:31:30.161486

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "292babe4c51e"
down_revision: str | Sequence[str] | None = "0b7ab1be21e2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BLADE_TYPE_HANDS = {
    "Dagger": "1H",
    "Sword": "1H",
    "Axe / Mace": "1H",
    "Great Sword": "2H",
    "Great Axe": "2H",
    "Staff": "2H",
    "Heavy Mace": "2H",
    "Polearm": "2H",
    "Crossbow": "2H",
}


def upgrade() -> None:
    op.add_column(
        "blades",
        sa.Column("hands", sa.String(2), server_default="1H", nullable=False),
    )
    for blade_type, hands in BLADE_TYPE_HANDS.items():
        escaped = blade_type.replace("'", "''")
        op.execute(f"UPDATE blades SET hands = '{hands}' WHERE blade_type = '{escaped}'")


def downgrade() -> None:
    op.drop_column("blades", "hands")
