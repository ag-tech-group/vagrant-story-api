"""rename weapons table to blades

Revision ID: 5cfa7076d3f0
Revises: de2340170673
Create Date: 2026-03-20 18:17:57.417238

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5cfa7076d3f0"
down_revision: str | Sequence[str] | None = "de2340170673"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.rename_table("weapons", "blades")


def downgrade() -> None:
    op.rename_table("blades", "weapons")
