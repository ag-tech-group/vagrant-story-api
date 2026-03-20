"""remove keys from consumables rename wine bottles

Revision ID: de2340170673
Revises: 79e6f0157e5c
Create Date: 2026-03-20 16:30:21.780677

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "de2340170673"
down_revision: str | Sequence[str] | None = "79e6f0157e5c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Remove keys that belong in the keys table, not consumables
    op.execute(
        "DELETE FROM consumables WHERE field_name IN ('Gold_Key', 'Silver_Key', 'Bronze_Key', 'Iron_Key')"
    )

    # Rename wine bottles to include "Wine"
    op.execute(
        "UPDATE consumables SET name = 'Virtus Wine', field_name = 'Virtus_Wine' WHERE field_name = 'Virtus'"
    )
    op.execute(
        "UPDATE consumables SET name = 'Valens Wine', field_name = 'Valens_Wine' WHERE field_name = 'Valens'"
    )
    op.execute(
        "UPDATE consumables SET name = 'Prudens Wine', field_name = 'Prudens_Wine' WHERE field_name = 'Prudens'"
    )
    op.execute(
        "UPDATE consumables SET name = 'Volare Wine', field_name = 'Volare_Wine' WHERE field_name = 'Volare'"
    )


def downgrade() -> None:
    # Revert wine names
    op.execute(
        "UPDATE consumables SET name = 'Virtus', field_name = 'Virtus' WHERE field_name = 'Virtus_Wine'"
    )
    op.execute(
        "UPDATE consumables SET name = 'Valens', field_name = 'Valens' WHERE field_name = 'Valens_Wine'"
    )
    op.execute(
        "UPDATE consumables SET name = 'Prudens', field_name = 'Prudens' WHERE field_name = 'Prudens_Wine'"
    )
    op.execute(
        "UPDATE consumables SET name = 'Volare', field_name = 'Volare' WHERE field_name = 'Volare_Wine'"
    )
