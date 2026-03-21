"""add equip_slot to inventory_items

Revision ID: b1c2d3e4f5a6
Revises: a7b8c9d0e1f2
Create Date: 2026-03-21 17:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b1c2d3e4f5a6"
down_revision: str | Sequence[str] | None = "a7b8c9d0e1f2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add equip_slot column to inventory_items."""
    op.add_column("inventory_items", sa.Column("equip_slot", sa.String(20), nullable=True))


def downgrade() -> None:
    """Remove equip_slot column from inventory_items."""
    op.drop_column("inventory_items", "equip_slot")
