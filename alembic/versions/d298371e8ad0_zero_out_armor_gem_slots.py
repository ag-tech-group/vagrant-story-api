"""zero out armor gem slots

Revision ID: d298371e8ad0
Revises: 292babe4c51e
Create Date: 2026-03-20 23:53:16.700735

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d298371e8ad0"
down_revision: str | Sequence[str] | None = "292babe4c51e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Armor (Helm/Body/Leg/Arm) cannot have gems — only shields and blades (via grips) can.
    # The gem_slots values were junk data from extraction.
    op.execute(
        "UPDATE armor SET gem_slots = 0 WHERE armor_type IN ('Helm', 'Body', 'Leg', 'Arm')"
    )


def downgrade() -> None:
    pass
