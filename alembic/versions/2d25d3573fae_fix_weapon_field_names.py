"""fix_weapon_field_names

Revision ID: 2d25d3573fae
Revises: b0d0c8bef8bc
Create Date: 2026-03-17 19:56:51.965413

"""
from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '2d25d3573fae'
down_revision: str | Sequence[str] | None = 'b0d0c8bef8bc'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

NAME_FIXES = {
    "Holy_Wind": "Holy_Win",
    "Balbriggin": "Balbriggan",
    "Cranquein": "Cranequin",
    "Khophish": "Khopesh",
}


def upgrade() -> None:
    for old, new in NAME_FIXES.items():
        op.execute(
            f"UPDATE weapons SET field_name = '{new}' WHERE field_name = '{old}'"
        )


def downgrade() -> None:
    for old, new in NAME_FIXES.items():
        op.execute(
            f"UPDATE weapons SET field_name = '{old}' WHERE field_name = '{new}'"
        )
