"""fix weapon blade_type labels

Revision ID: cd8fb71e975b
Revises: f6d096e20deb
Create Date: 2026-03-19 17:40:39.528358

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'cd8fb71e975b'
down_revision: Union[str, Sequence[str], None] = 'f6d096e20deb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# The original data extraction had scrambled blade_type labels.
# Order matters: rename to temp values first to avoid collisions.
RENAMES = [
    ("Axe", "_temp_axe_mace"),
    ("Mace", "_temp_great_axe"),
    ("Staff", "_temp_heavy_mace"),
    ("Heavy Mace", "_temp_polearm"),
    ("Great Axe", "_temp_staff"),
    ("Polearm", "_temp_crossbow"),
    ("_temp_axe_mace", "Axe / Mace"),
    ("_temp_great_axe", "Great Axe"),
    ("_temp_heavy_mace", "Heavy Mace"),
    ("_temp_polearm", "Polearm"),
    ("_temp_staff", "Staff"),
    ("_temp_crossbow", "Crossbow"),
]

REVERSE_RENAMES = [
    ("Axe / Mace", "_temp_axe_mace"),
    ("Great Axe", "_temp_great_axe"),
    ("Heavy Mace", "_temp_heavy_mace"),
    ("Polearm", "_temp_polearm"),
    ("Staff", "_temp_staff"),
    ("Crossbow", "_temp_crossbow"),
    ("_temp_axe_mace", "Axe"),
    ("_temp_great_axe", "Mace"),
    ("_temp_heavy_mace", "Staff"),
    ("_temp_polearm", "Heavy Mace"),
    ("_temp_staff", "Great Axe"),
    ("_temp_crossbow", "Polearm"),
]


def upgrade() -> None:
    for old, new in RENAMES:
        op.execute(
            f"UPDATE weapons SET blade_type = '{new}' WHERE blade_type = '{old}'"
        )


def downgrade() -> None:
    for old, new in REVERSE_RENAMES:
        op.execute(
            f"UPDATE weapons SET blade_type = '{new}' WHERE blade_type = '{old}'"
        )
