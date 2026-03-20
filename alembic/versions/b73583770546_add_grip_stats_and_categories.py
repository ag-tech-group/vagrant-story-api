"""add grip stats and categories

Revision ID: b73583770546
Revises: 707729c19d8e
Create Date: 2026-03-19 23:47:26.812290

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b73583770546"
down_revision: str | Sequence[str] | None = "707729c19d8e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "ALTER TABLE grips ALTER COLUMN grip_type TYPE VARCHAR(50) USING grip_type::VARCHAR(50)"
    )
    op.execute(
        "ALTER TABLE grips ADD COLUMN IF NOT EXISTS compatible_weapons VARCHAR(200) DEFAULT ''"
    )
    op.execute("ALTER TABLE grips ADD COLUMN IF NOT EXISTS blunt INTEGER DEFAULT 0")
    op.execute("ALTER TABLE grips ADD COLUMN IF NOT EXISTS edged INTEGER DEFAULT 0")
    op.execute("ALTER TABLE grips ADD COLUMN IF NOT EXISTS piercing INTEGER DEFAULT 0")
    op.execute("ALTER TABLE grips ADD COLUMN IF NOT EXISTS gem_slots INTEGER DEFAULT 0")
    op.execute(
        "UPDATE grips SET grip_type = 'Hilt', compatible_weapons = 'Dagger/Sword/Great Sword', blunt = 0, edged = 4, piercing = 1, gem_slots = 0, \"str\" = 1, \"int\" = 0, agi = -1 WHERE field_name = 'Short_Hilt'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Hilt', compatible_weapons = 'Dagger/Sword/Great Sword', blunt = 0, edged = 2, piercing = 4, gem_slots = 0, \"str\" = 1, \"int\" = 1, agi = -1 WHERE field_name = 'Swept_Hilt'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Hilt', compatible_weapons = 'Dagger/Sword/Great Sword', blunt = 8, edged = 6, piercing = 2, gem_slots = 1, \"str\" = 2, \"int\" = 2, agi = -1 WHERE field_name = 'Cross_Guard'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Hilt', compatible_weapons = 'Dagger/Sword/Great Sword', blunt = 0, edged = 5, piercing = 9, gem_slots = 2, \"str\" = 2, \"int\" = 2, agi = -2 WHERE field_name = 'Knuckle_Guard'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Hilt', compatible_weapons = 'Dagger/Sword/Great Sword', blunt = 0, edged = 8, piercing = 7, gem_slots = 1, \"str\" = 3, \"int\" = 2, agi = -2 WHERE field_name = 'Counter_Guard'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Hilt', compatible_weapons = 'Dagger/Sword/Great Sword', blunt = 10, edged = 12, piercing = 10, gem_slots = 2, \"str\" = 3, \"int\" = 3, agi = -2 WHERE field_name = 'Side_Ring'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Hilt', compatible_weapons = 'Dagger/Sword/Great Sword', blunt = 0, edged = 15, piercing = 12, gem_slots = 3, \"str\" = 4, \"int\" = 3, agi = -3 WHERE field_name = 'Power_Palm'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Hilt', compatible_weapons = 'Dagger/Sword/Great Sword', blunt = 0, edged = 13, piercing = 17, gem_slots = 2, \"str\" = 4, \"int\" = 4, agi = -3 WHERE field_name = 'Murderers_Hilt'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Hilt', compatible_weapons = 'Dagger/Sword/Great Sword', blunt = 20, edged = 20, piercing = 20, gem_slots = 3, \"str\" = 5, \"int\" = 4, agi = -3 WHERE field_name = 'Spiral_Hilt'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Haft', compatible_weapons = 'Axe/Mace/Great Axe/Heavy Mace/Staff', blunt = 5, edged = 1, piercing = 0, gem_slots = 0, \"str\" = 1, \"int\" = 0, agi = -2 WHERE field_name = 'Wooden_Grip'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Haft', compatible_weapons = 'Axe/Mace/Great Axe/Heavy Mace/Staff', blunt = 3, edged = 6, piercing = 0, gem_slots = 1, \"str\" = 1, \"int\" = 2, agi = -2 WHERE field_name = 'Sand_Face'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Haft', compatible_weapons = 'Axe/Mace/Great Axe/Heavy Mace/Staff', blunt = 8, edged = 4, piercing = 0, gem_slots = 0, \"str\" = 2, \"int\" = 1, agi = -2 WHERE field_name = 'Czekan_Type'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Haft', compatible_weapons = 'Axe/Mace/Great Axe/Heavy Mace/Staff', blunt = 6, edged = 9, piercing = 0, gem_slots = 1, \"str\" = 2, \"int\" = 2, agi = -3 WHERE field_name = 'Sarissa_Grip'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Haft', compatible_weapons = 'Axe/Mace/Great Axe/Heavy Mace/Staff', blunt = 6, edged = 15, piercing = 0, gem_slots = 1, \"str\" = 3, \"int\" = 1, agi = -3 WHERE field_name = 'Heavy_Grip'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Haft', compatible_weapons = 'Axe/Mace/Great Axe/Heavy Mace/Staff', blunt = 13, edged = 5, piercing = 0, gem_slots = 2, \"str\" = 3, \"int\" = 2, agi = -3 WHERE field_name = 'Gendarme'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Haft', compatible_weapons = 'Axe/Mace/Great Axe/Heavy Mace/Staff', blunt = 17, edged = 7, piercing = 0, gem_slots = 2, \"str\" = 4, \"int\" = 3, agi = -3 WHERE field_name = 'Runkastyle'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Haft', compatible_weapons = 'Axe/Mace/Great Axe/Heavy Mace/Staff', blunt = 21, edged = 9, piercing = 0, gem_slots = 2, \"str\" = 1, \"int\" = 8, agi = -4 WHERE field_name = 'Grimoire_Grip'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Haft', compatible_weapons = 'Axe/Mace/Great Axe/Heavy Mace/Staff', blunt = 8, edged = 19, piercing = 0, gem_slots = 3, \"str\" = 5, \"int\" = 1, agi = -4 WHERE field_name = 'Bhuj_Type'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Haft', compatible_weapons = 'Axe/Mace/Great Axe/Heavy Mace/Staff', blunt = 11, edged = 22, piercing = 0, gem_slots = 3, \"str\" = 6, \"int\" = 3, agi = -4 WHERE field_name = 'Elephant'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Shaft', compatible_weapons = 'Polearm', blunt = 11, edged = 0, piercing = 1, gem_slots = 0, \"str\" = 1, \"int\" = 0, agi = -3 WHERE field_name = 'Wooden_Pole'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Shaft', compatible_weapons = 'Polearm', blunt = 2, edged = 6, piercing = 16, gem_slots = 0, \"str\" = 3, \"int\" = 2, agi = -4 WHERE field_name = 'Winged_Pole'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Shaft', compatible_weapons = 'Polearm', blunt = 2, edged = 12, piercing = 4, gem_slots = 1, \"str\" = 2, \"int\" = 1, agi = -3 WHERE field_name = 'Spiculum_Pole'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Shaft', compatible_weapons = 'Polearm', blunt = 10, edged = 14, piercing = 12, gem_slots = 1, \"str\" = 5, \"int\" = 2, agi = -5 WHERE field_name = 'Ahlspies'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Shaft', compatible_weapons = 'Polearm', blunt = 16, edged = 4, piercing = 10, gem_slots = 2, \"str\" = 4, \"int\" = 3, agi = -4 WHERE field_name = 'Framea_Pole'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Shaft', compatible_weapons = 'Polearm', blunt = 15, edged = 6, piercing = 21, gem_slots = 3, \"str\" = 6, \"int\" = 5, agi = -5 WHERE field_name = 'Spiral_Pole'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Bolt', compatible_weapons = 'Crossbow', blunt = 1, edged = 0, piercing = 10, gem_slots = 0, \"str\" = 1, \"int\" = 0, agi = -1 WHERE field_name = 'Simple_Bolt'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Bolt', compatible_weapons = 'Crossbow', blunt = 2, edged = 0, piercing = 13, gem_slots = 1, \"str\" = 2, \"int\" = 0, agi = -1 WHERE field_name = 'Steel_Bolt'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Bolt', compatible_weapons = 'Crossbow', blunt = 17, edged = 0, piercing = 2, gem_slots = 1, \"str\" = 3, \"int\" = 1, agi = -1 WHERE field_name = 'Javelin_Bolt'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Bolt', compatible_weapons = 'Crossbow', blunt = 3, edged = 0, piercing = 20, gem_slots = 1, \"str\" = 4, \"int\" = 1, agi = -1 WHERE field_name = 'Falarica_Bolt'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Bolt', compatible_weapons = 'Crossbow', blunt = 23, edged = 0, piercing = 4, gem_slots = 1, \"str\" = 2, \"int\" = 0, agi = -2 WHERE field_name = 'Stone_Bullet'"
    )
    op.execute(
        "UPDATE grips SET grip_type = 'Bolt', compatible_weapons = 'Crossbow', blunt = 5, edged = 0, piercing = 25, gem_slots = 1, \"str\" = 4, \"int\" = 2, agi = -2 WHERE field_name = 'Sonic_Bullet'"
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
