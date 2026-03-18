"""fix_armor_types_and_names

Revision ID: d0c8d71a3452
Revises: 2d25d3573fae
Create Date: 2026-03-17 20:40:13.811252

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'd0c8d71a3452'
down_revision: Union[str, Sequence[str], None] = '2d25d3573fae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Fix armor_type: Glove→Leg, Boots→Arm (were swapped in extraction)
    op.execute("UPDATE armor SET armor_type = 'Leg' WHERE armor_type = 'Glove'")
    op.execute("UPDATE armor SET armor_type = 'Arm' WHERE armor_type = 'Boots'")

    # Fix field_names to match canonical game names used in crafting recipes
    op.execute("UPDATE armor SET field_name = 'Cuisse' WHERE field_name = 'Bandage' AND armor_type = 'Leg'")
    op.execute("UPDATE armor SET field_name = 'Bandage' WHERE field_name = 'Buffle' AND armor_type = 'Arm'")
    op.execute("UPDATE armor SET field_name = 'Light_Greave' WHERE field_name = 'Light_Grieve'")
    op.execute("UPDATE armor SET field_name = 'Segmentata' WHERE field_name = 'Segementata'")


def downgrade() -> None:
    op.execute("UPDATE armor SET field_name = 'Segementata' WHERE field_name = 'Segmentata'")
    op.execute("UPDATE armor SET field_name = 'Light_Grieve' WHERE field_name = 'Light_Greave'")
    op.execute("UPDATE armor SET field_name = 'Buffle' WHERE field_name = 'Bandage' AND armor_type = 'Arm'")
    op.execute("UPDATE armor SET field_name = 'Bandage' WHERE field_name = 'Cuisse' AND armor_type = 'Leg'")

    op.execute("UPDATE armor SET armor_type = 'Boots' WHERE armor_type = 'Arm'")
    op.execute("UPDATE armor SET armor_type = 'Glove' WHERE armor_type = 'Leg'")
