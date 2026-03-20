"""merge all feature migration heads

Revision ID: 36db0438bbf9
Revises: a1b2c3d4e5f6, b2c3d4e5f6a7, c3d4e5f6a7b8, d4e5f6a7b8c9, e5f6a7b8c9d0, f6a7b8c9d0e1
Create Date: 2026-03-20 12:55:59.374865

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "36db0438bbf9"
down_revision: str | Sequence[str] | None = (
    "a1b2c3d4e5f6",
    "b2c3d4e5f6a7",
    "c3d4e5f6a7b8",
    "d4e5f6a7b8c9",
    "e5f6a7b8c9d0",
    "f6a7b8c9d0e1",
)
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
