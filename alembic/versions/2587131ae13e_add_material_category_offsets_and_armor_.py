"""add material category offsets and armor base stats

Revision ID: 2587131ae13e
Revises: d5f249b2dc57
Create Date: 2026-03-20 18:31:25.289780

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2587131ae13e"
down_revision: str | Sequence[str] | None = "d5f249b2dc57"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Material IDs: Wood=1, Leather=2, Bronze=3, Iron=4, Hagane=5, Silver=6, Damascus=7

# Per-category offsets from base stats.
# (material_name, blade_str, blade_int, blade_agi, shield_str, shield_int, shield_agi,
#  armor_str, armor_int, armor_agi)
MATERIAL_OFFSETS = [
    ("Wood", 0, 0, 0, 1, 6, 0, 0, 0, 0),
    ("Leather", 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Bronze", 2, 1, -2, 2, 1, -2, 2, -4, -2),
    ("Iron", 4, 1, -2, 4, 2, -2, 4, -3, -2),
    ("Hagane", 6, 2, -1, 6, 2, -1, 6, -3, -1),
    ("Silver", 3, 1, -1, 3, 1, -1, 3, -4, -1),
    ("Damascus", 8, 3, -1, 8, 3, -1, 8, -2, -1),
]

# Armor base stats: (armor_id, str, int, agi)
# These are Leather-base for Helm/Body/Leg/Arm, Wood-base for Shield.
ARMOR_BASE_STATS = [
    # Shields (Wood base)
    (112, 6, 9, -1),
    (113, 6, 10, -1),
    (114, 7, 10, -1),
    (115, 8, 13, -1),
    (116, 9, 13, -1),
    (117, 13, 16, -2),
    (118, 13, 17, -2),
    (119, 15, 19, -2),
    (120, 16, 19, -2),
    (121, 16, 20, -2),
    (122, 19, 22, -2),
    (123, 19, 23, -2),
    (124, 19, 24, -2),
    (125, 22, 30, -3),
    (126, 24, 29, -3),
    (127, 26, 26, -3),
    # Helm (Leather base)
    (128, 1, 8, 0),
    (129, 2, 9, 0),
    (130, 1, 15, 0),
    (131, 2, 8, -1),
    (132, 3, 10, -1),
    (133, 3, 10, -1),
    (134, 4, 10, -1),
    (135, 5, 11, -1),
    (136, 6, 12, -1),
    (137, 7, 13, -1),
    (138, 8, 14, -2),
    (139, 9, 15, -2),
    (140, 10, 16, -2),
    (141, 11, 20, -2),
    (142, 12, 18, -2),
    (143, 13, 17, -2),
    # Body (Leather base)
    (144, 5, 10, 0),
    (145, 5, 15, 0),
    (146, 3, 25, 0),
    (147, 7, 13, 0),
    (148, 8, 13, -1),
    (149, 7, 17, -1),
    (150, 9, 17, -1),
    (151, 11, 17, -2),
    (152, 13, 18, -1),
    (153, 15, 20, -1),
    (154, 17, 21, -2),
    (155, 18, 21, -2),
    (156, 18, 22, -2),
    (157, 18, 26, -3),
    (158, 19, 24, -3),
    (159, 20, 23, -3),
    # Leg (Leather base)
    (160, 1, 12, 0),
    (161, 2, 8, 0),
    (162, 2, 10, 0),
    (163, 3, 10, 0),
    (164, 4, 10, 0),
    (165, 5, 11, -1),
    (166, 6, 12, -1),
    (167, 7, 13, -1),
    (168, 8, 14, -1),
    (169, 9, 15, -2),
    (170, 10, 16, -3),
    (171, 11, 16, -2),
    (172, 12, 17, -2),
    (173, 13, 23, -3),
    (174, 14, 22, -3),
    (175, 15, 20, -3),
    # Arm (Leather base)
    (176, 1, 13, 0),
    (177, 2, 9, 0),
    (178, 2, 9, 0),
    (179, 3, 10, 0),
    (180, 4, 10, -1),
    (181, 4, 11, -1),
    (182, 5, 11, -1),
    (183, 6, 12, -1),
    (184, 7, 13, -1),
    (185, 1, 14, -1),
    (186, 8, 14, -2),
    (187, 9, 15, -1),
    (188, 10, 16, -3),
    (189, 11, 20, -3),
    (190, 12, 19, -3),
    (191, 13, 18, -3),
]

# Previous shield stats for downgrade (Wood-base values that were already stored)
OLD_SHIELD_STATS = [
    (112, 5, 3, -1),
    (113, 5, 4, -1),
    (114, 6, 4, -1),
    (115, 7, 7, -1),
    (116, 8, 7, -1),
    (117, 12, 10, -2),
    (118, 12, 11, -2),
    (119, 14, 13, -2),
    (120, 15, 13, -2),
    (121, 15, 14, -2),
    (122, 18, 16, -2),
    (123, 18, 17, -2),
    (124, 18, 18, -2),
    (125, 21, 24, -3),
    (126, 23, 23, -3),
    (127, 25, 20, -3),
]


def upgrade() -> None:
    # Add per-category offset columns to materials
    for col in [
        "blade_str",
        "blade_int",
        "blade_agi",
        "shield_str",
        "shield_int",
        "shield_agi",
        "armor_str",
        "armor_int",
        "armor_agi",
    ]:
        op.add_column("materials", sa.Column(col, sa.Integer(), server_default="0", nullable=False))

    # Populate material offsets
    for name, b_s, b_i, b_a, s_s, s_i, s_a, a_s, a_i, a_a in MATERIAL_OFFSETS:
        op.execute(
            f"UPDATE materials SET "
            f"blade_str={b_s}, blade_int={b_i}, blade_agi={b_a}, "
            f"shield_str={s_s}, shield_int={s_i}, shield_agi={s_a}, "
            f"armor_str={a_s}, armor_int={a_i}, armor_agi={a_a} "
            f"WHERE name='{name}'"
        )

    # Update armor base stats (shields get correct Wood-base, armor gets Leather-base)
    for armor_id, s, i, a in ARMOR_BASE_STATS:
        op.execute(f"UPDATE armor SET str={s}, int={i}, agi={a} WHERE id={armor_id}")


def downgrade() -> None:
    # Revert armor stats: shields back to old values, armor back to 0/0/0
    for armor_id, s, i, a in OLD_SHIELD_STATS:
        op.execute(f"UPDATE armor SET str={s}, int={i}, agi={a} WHERE id={armor_id}")
    # Reset non-shield armor stats to 0/0/0
    for armor_id, _, _, _ in ARMOR_BASE_STATS:
        if armor_id > 127:  # Non-shield items
            op.execute(f"UPDATE armor SET str=0, int=0, agi=0 WHERE id={armor_id}")

    # Remove offset columns
    for col in [
        "blade_str",
        "blade_int",
        "blade_agi",
        "shield_str",
        "shield_int",
        "shield_agi",
        "armor_str",
        "armor_int",
        "armor_agi",
    ]:
        op.drop_column("materials", col)
