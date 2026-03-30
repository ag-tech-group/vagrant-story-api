"""add dp/pp stats to inventory items

Revision ID: a1b2c3d4e5f7
Revises: cf2ec699ae97
Create Date: 2026-03-29

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f7"
down_revision: str | Sequence[str] | None = "cf2ec699ae97"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("inventory_items", sa.Column("dp_current", sa.Integer(), nullable=True))
    op.add_column("inventory_items", sa.Column("dp_max", sa.Integer(), nullable=True))
    op.add_column("inventory_items", sa.Column("pp_current", sa.Integer(), nullable=True))
    op.add_column("inventory_items", sa.Column("pp_max", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("inventory_items", "pp_max")
    op.drop_column("inventory_items", "pp_current")
    op.drop_column("inventory_items", "dp_max")
    op.drop_column("inventory_items", "dp_current")
