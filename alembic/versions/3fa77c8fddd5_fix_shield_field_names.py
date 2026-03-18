"""fix_shield_field_names

Revision ID: 3fa77c8fddd5
Revises: 649d98be5148
Create Date: 2026-03-18 15:22:48.999018
"""

from alembic import op

revision: str = "3fa77c8fddd5"
down_revision: str | None = "649d98be5148"
branch_labels: None = None
depends_on: None = None


def upgrade() -> None:
    op.execute(
        "UPDATE armor SET field_name = REPLACE(field_name, '_Shield', '') "
        "WHERE armor_type = 'Shield' AND field_name LIKE '%_Shield'"
    )


def downgrade() -> None:
    op.execute(
        "UPDATE armor SET field_name = field_name || '_Shield' "
        "WHERE armor_type = 'Shield' AND field_name NOT LIKE '%_Shield'"
    )
