"""localize grip and gem names to english

Revision ID: 9be85acfddc4
Revises: f1a2b3c4d5e6
Create Date: 2026-03-21 14:07:41.115309

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9be85acfddc4"
down_revision: str | Sequence[str] | None = "f1a2b3c4d5e6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Grips that need special handling (field_name -> display_name)
GRIP_SPECIAL = [
    ("Murderers_Hilt", "Murderer's Hilt"),
]

# Gems that need special handling (field_name -> display_name)
GEM_SPECIAL = [
    ("Talos_Feldspear", "Talos Feldspar"),
]


def upgrade() -> None:
    # Grips: convert field_name underscores to spaces for display name
    op.execute("UPDATE grips SET name = REPLACE(field_name, '_', ' ')")

    # Apply grip special cases (apostrophes, spelling corrections)
    for field_name, display_name in GRIP_SPECIAL:
        safe_name = display_name.replace("'", "''")
        op.execute(f"UPDATE grips SET name = '{safe_name}' WHERE field_name = '{field_name}'")

    # Gems: convert field_name underscores to spaces for display name
    op.execute("UPDATE gems SET name = REPLACE(field_name, '_', ' ')")

    # Apply gem special cases (spelling corrections)
    for field_name, display_name in GEM_SPECIAL:
        safe_name = display_name.replace("'", "''")
        op.execute(f"UPDATE gems SET name = '{safe_name}' WHERE field_name = '{field_name}'")


def downgrade() -> None:
    # Revert grips to their original French names from the JSON seed data
    # This is a best-effort downgrade; the original French names would need
    # to be re-seeded from the JSON data for a full revert
    pass
