"""add storage to inventory_items

Revision ID: c2d3e4f5a6b7
Revises: b1c2d3e4f5a6
Create Date: 2026-03-23 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c2d3e4f5a6b7"
down_revision: str | Sequence[str] | None = "b1c2d3e4f5a6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add storage column to inventory_items, defaulting to 'bag'."""
    op.add_column(
        "inventory_items",
        sa.Column("storage", sa.String(20), server_default="bag", nullable=False),
    )


def downgrade() -> None:
    """Remove storage column from inventory_items."""
    op.drop_column("inventory_items", "storage")
