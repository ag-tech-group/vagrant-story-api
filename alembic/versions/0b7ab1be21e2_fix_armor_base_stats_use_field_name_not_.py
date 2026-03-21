"""fix armor base stats use field_name not id

Revision ID: 0b7ab1be21e2
Revises: 2587131ae13e
Create Date: 2026-03-20 19:06:11.945652

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0b7ab1be21e2"
down_revision: str | Sequence[str] | None = "2587131ae13e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (field_name, str, int, agi) — Leather-base for armor, Wood-base for shields
# Parsed from game guides armors.txt and shields.txt
ARMOR_STATS = [
    # Helm (Leather base)
    ("Bandana", 1, 8, 0),
    ("Bear_Mask", 2, 9, 0),
    ("Wizard_Hat", 1, 15, 0),
    ("Bone_Helm", 2, 8, -1),
    ("Chain_Coif", 3, 10, -1),
    ("Spangenhelm", 3, 10, -1),
    ("Cabasset", 4, 10, -1),
    ("Sallet", 5, 11, -1),
    ("Barbut", 6, 12, -1),
    ("Basinet", 7, 13, -1),
    ("Armet", 8, 14, -2),
    ("Close_Helm", 9, 15, -2),
    ("Burgonet", 10, 16, -2),
    ("Hoplite_Helm", 11, 20, -2),
    ("Jazeraint_Helm", 12, 18, -2),
    ("Dread_Helm", 13, 17, -2),
    # Body (Leather base)
    ("Jerkin", 5, 10, 0),
    ("Hauberk", 5, 15, 0),
    ("Wizard_Robe", 3, 25, 0),
    ("Cuirass", 7, 13, 0),
    ("Banded_Mail", 8, 13, -1),
    ("Ring_Mail", 7, 17, -1),
    ("Chain_Mail", 9, 17, -1),
    ("Breastplate", 11, 17, -2),
    ("Segmentata", 13, 18, -1),
    ("Scale_Armor", 15, 20, -1),
    ("Brigandine", 17, 21, -2),
    ("Plate_Mail", 18, 21, -2),
    ("Fluted_Armor", 18, 22, -2),
    ("Hoplite_Armor", 18, 26, -3),
    ("Jazeraint_Armor", 19, 24, -3),
    ("Dread_Armor", 20, 23, -3),
    # Leg (Leather base)
    ("Sandals", 1, 12, 0),
    ("Boots", 2, 8, 0),
    ("Long_Boots", 2, 10, 0),
    ("Cuisse", 3, 10, 0),
    ("Light_Greave", 4, 10, 0),
    ("Ring_Leggings", 5, 11, -1),
    ("Chain_Leggings", 6, 12, -1),
    ("Fusskampf", 7, 13, -1),
    ("Poleyn", 8, 14, -1),
    ("Jambeau", 9, 15, -2),
    ("Missaglia", 10, 16, -3),
    ("Plate_Leggings", 11, 16, -2),
    ("Fluted_Leggings", 12, 17, -2),
    ("Hoplite_Leggings", 13, 23, -3),
    ("Jazeraint_Leggings", 14, 22, -3),
    ("Dread_Leggings", 15, 20, -3),
    # Arm (Leather base)
    ("Bandage", 1, 13, 0),
    ("Leather_Glove", 2, 9, 0),
    ("Reinforced_Glove", 2, 9, 0),
    ("Knuckles", 3, 10, 0),
    ("Ring_Sleeve", 4, 10, -1),
    ("Chain_Sleeve", 4, 11, -1),
    ("Gauntlet", 5, 11, -1),
    ("Vambrace", 6, 12, -1),
    ("Plate_Glove", 7, 13, -1),
    ("Rondanche", 1, 14, -1),
    ("Tilt_Glove", 8, 14, -2),
    ("Freiturnier", 9, 15, -1),
    ("Fluted_Glove", 10, 16, -3),
    ("Hoplite_Glove", 11, 20, -3),
    ("Jazeraint_Glove", 12, 19, -3),
    ("Dread_Glove", 13, 18, -3),
]

# Shield stats (Wood base) — use short field_names matching production DB
SHIELD_STATS = [
    ("Buckler", 6, 9, -1),
    ("Pelta", 6, 10, -1),
    ("Targe", 7, 10, -1),
    ("Quad", 8, 13, -1),
    ("Circle", 9, 13, -1),
    ("Tower", 13, 16, -2),
    ("Spiked", 13, 17, -2),
    ("Round", 15, 19, -2),
    ("Kite", 16, 19, -2),
    ("Casserole", 16, 20, -2),
    ("Heater", 19, 22, -2),
    ("Oval", 19, 23, -2),
    ("Knight", 19, 24, -2),
    ("Hoplite", 22, 30, -3),
    ("Jazeraint", 24, 29, -3),
    ("Dread", 26, 26, -3),
]

# Also update shield names to English where they're still French
SHIELD_NAME_FIXES = [
    ("Spiked", "Spiked Shield"),
    ("Casserole", "Casserole Shield"),
    ("Heater", "Heater Shield"),
    ("Oval", "Oval Shield"),
    ("Knight", "Knight Shield"),
    ("Hoplite", "Hoplite Shield"),
    ("Jazeraint", "Jazeraint Shield"),
    ("Dread", "Dread Shield"),
    ("Pelta", "Pelta Shield"),
    ("Quad", "Quad Shield"),
    ("Circle", "Circle Shield"),
    ("Tower", "Tower Shield"),
    ("Round", "Round Shield"),
    ("Kite", "Kite Shield"),
]


def upgrade() -> None:
    # Update armor base stats (Leather-base)
    for field_name, s, i, a in ARMOR_STATS:
        op.execute(
            f'UPDATE armor SET "str"={s}, "int"={i}, agi={a} WHERE field_name=\'{field_name}\''
        )

    # Update shield base stats (Wood-base)
    for field_name, s, i, a in SHIELD_STATS:
        op.execute(
            f'UPDATE armor SET "str"={s}, "int"={i}, agi={a} WHERE field_name=\'{field_name}\''
        )

    # Fix shield display names
    for field_name, display_name in SHIELD_NAME_FIXES:
        op.execute(f"UPDATE armor SET name='{display_name}' WHERE field_name='{field_name}'")

    # Fix armor display names (French → English, use field_name as source)
    # Convert field_name underscores to spaces for display name
    for field_name, _, _, _ in ARMOR_STATS:
        display_name = field_name.replace("_", " ")
        op.execute(f"UPDATE armor SET name='{display_name}' WHERE field_name='{field_name}'")


def downgrade() -> None:
    pass
