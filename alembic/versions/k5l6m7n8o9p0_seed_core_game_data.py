"""seed core game data

Revision ID: k5l6m7n8o9p0
Revises: j4k5l6m7n8o9
Create Date: 2026-03-26 12:00:00.000000

"""

import json
from collections.abc import Sequence
from pathlib import Path

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "k5l6m7n8o9p0"
down_revision: str | Sequence[str] | None = "j4k5l6m7n8o9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

DATA_DIR = Path(__file__).parent.parent.parent / "data"

# ── Blade name localizations (French → English) ──────────────────────────
# (game_id, new_english_name, new_field_name)
BLADE_NAME_LOCALIZATIONS = [
    (1, "Battle Knife", "Battle_Knife"),
    (2, "Scramasax", "Scramasax"),
    (3, "Dirk", "Dirk"),
    (6, "Cinquedea", "Cinquedea"),
    (7, "Kris", "Kris"),
    (9, "Khukuri", "Khukuri"),
    (10, "Baselard", "Baselard"),
    (12, "Jamadhar", "Jamadhar"),
    (13, "Spatha", "Spatha"),
    (14, "Scimitar", "Scimitar"),
    (15, "Rapier", "Rapier"),
    (16, "Short Sword", "Short_Sword"),
    (19, "Falchion", "Falchion"),
    (20, "Shotel", "Shotel"),
    (21, "Khora", "Khora"),
    (24, "Rhomphaia", "Rhomphaia"),
    (25, "Broad Sword", "Broad_Sword"),
    (26, "Norse Sword", "Norse_Sword"),
    (30, "Schiavona", "Schiavona"),
    (34, "Holy Win", "Holy_Win"),
    (35, "Hand Axe", "Hand_Axe"),
    (36, "Battle Axe", "Battle_Axe"),
    (37, "Francisca", "Francisca"),
    (38, "Tabarzin", "Tabarzin"),
    (39, "Chamkaq", "Chamkaq"),
    (40, "Tabar", "Tabar"),
    (41, "Bullova", "Bullova"),
    (43, "Goblin Club", "Goblin_Club"),
    (44, "Spiked Club", "Spiked_Club"),
    (45, "Ball Mace", "Ball_Mace"),
    (46, "Footman's Mace", "Footmans_Mace"),
    (49, "Bec de Corbin", "Bec_de_Corbin"),
    (50, "War Maul", "War_Maul"),
    (51, "Guisarme", "Guisarme"),
    (53, "Sabre Halberd", "Sabre_Halberd"),
    (54, "Balbriggan", "Balbriggan"),
    (57, "Wizard Staff", "Wizard_Staff"),
    (58, "Clergy Rod", "Clergy_Rod"),
    (59, "Summoner Baton", "Summoner_Baton"),
    (60, "Shamanic Staff", "Shamanic_Staff"),
    (61, "Bishop's Crosier", "Bishops_Crosier"),
    (62, "Sage's Cane", "Sages_Cane"),
    (63, "Langdebeve", "Langdebeve"),
    (65, "Footman's Mace", "Footmans_Mace_Heavy"),
    (70, "Hand of Light", "Hand_of_Light"),
    (71, "Spear", "Spear"),
    (72, "Glaive", "Glaive"),
    (73, "Scorpion", "Scorpion"),
    (76, "Awl Pike", "Awl_Pike"),
    (77, "Boar Spear", "Boar_Spear"),
    (78, "Fauchard", "Fauchard"),
    (83, "Gastraph Bow", "Gastraph_Bow"),
    (85, "Target Bow", "Target_Bow"),
    (86, "Windlass", "Windlass"),
    (87, "Cranequin", "Cranequin"),
    (90, "Arbalest", "Arbalest"),
]

# ── Blade hands mapping ──────────────────────────────────────────────────
BLADE_TYPE_HANDS = {
    "Dagger": "1H",
    "Sword": "1H",
    "Axe / Mace": "1H",
    "Great Sword": "2H",
    "Great Axe": "2H",
    "Staff": "2H",
    "Heavy Mace": "2H",
    "Polearm": "2H",
    "Crossbow": "2H",
}

# ── Grip name special cases ──────────────────────────────────────────────
GRIP_NAME_SPECIALS = [
    ("Murderers_Hilt", "Murderer's Hilt"),
]

# ── Gem name special cases ───────────────────────────────────────────────
GEM_NAME_SPECIALS = [
    ("Talos_Feldspear", "Talos Feldspar"),
]

# ── Shield display name fixes ────────────────────────────────────────────
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

# ── Armor base stats (field_name, str, int, agi) ────────────────────────
# Leather-base for armor, Wood-base for shields
ARMOR_BASE_STATS = [
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
    # Shield (Wood base)
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

# ── Material category offsets ────────────────────────────────────────────
# (name, blade_str, blade_int, blade_agi, shield_str, shield_int, shield_agi,
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


def _table_has_rows(conn, table_name: str) -> bool:
    """Check if a table already has data."""
    result = conn.execute(sa.text(f"SELECT EXISTS (SELECT 1 FROM {table_name} LIMIT 1)"))
    return result.scalar()


def upgrade() -> None:
    """Seed blades, grips, armor, gems, materials, and crafting recipes."""
    conn = op.get_bind()

    # ── 1. Blades ─────────────────────────────────────────────────────
    if not _table_has_rows(conn, "blades"):
        blades_data = json.loads((DATA_DIR / "weapons.json").read_text())
        for blade in blades_data:
            conn.execute(
                sa.text(
                    "INSERT INTO blades "
                    "(game_id, field_name, name, description_fr, wep_file_id, blade_type, "
                    'damage_type, risk, "str", "int", agi, "range", damage, hands) '
                    "VALUES (:game_id, :field_name, :name, :description_fr, :wep_file_id, "
                    ":blade_type, :damage_type, :risk, :str, :int, :agi, :range, :damage, :hands)"
                ),
                {
                    "game_id": blade["id"],
                    "field_name": blade["field_name"],
                    "name": blade["name"],
                    "description_fr": blade.get("description_fr", ""),
                    "wep_file_id": blade.get("wep_file_id", 0),
                    "blade_type": blade["blade_type"],
                    "damage_type": blade["damage_type"],
                    "risk": blade.get("risk", 0),
                    "str": blade.get("str", 0),
                    "int": blade.get("int", 0),
                    "agi": blade.get("agi", 0),
                    "range": blade.get("range", 0),
                    "damage": blade.get("damage", 0),
                    "hands": "1H",  # default; corrected below
                },
            )

        # Apply English name localizations
        for game_id, eng_name, eng_field in BLADE_NAME_LOCALIZATIONS:
            conn.execute(
                sa.text(
                    "UPDATE blades SET name = :name, field_name = :field_name "
                    "WHERE game_id = :game_id"
                ),
                {"name": eng_name, "field_name": eng_field, "game_id": game_id},
            )

        # Set correct hands based on blade_type
        for blade_type, hands in BLADE_TYPE_HANDS.items():
            conn.execute(
                sa.text("UPDATE blades SET hands = :hands WHERE blade_type = :blade_type"),
                {"hands": hands, "blade_type": blade_type},
            )

    # ── 2. Grips ──────────────────────────────────────────────────────
    if not _table_has_rows(conn, "grips"):
        grips_data = json.loads((DATA_DIR / "grips.json").read_text())
        for grip in grips_data:
            conn.execute(
                sa.text(
                    "INSERT INTO grips "
                    "(game_id, field_name, name, description_fr, wep_file_id, grip_type, "
                    '"str", "int", agi, dp, pp, compatible_weapons, blunt, edged, piercing, '
                    "gem_slots) "
                    "VALUES (:game_id, :field_name, :name, :description_fr, :wep_file_id, "
                    ":grip_type, :str, :int, :agi, :dp, :pp, :compatible_weapons, :blunt, "
                    ":edged, :piercing, :gem_slots)"
                ),
                {
                    "game_id": grip["id"],
                    "field_name": grip["field_name"],
                    "name": grip["name"],
                    "description_fr": grip.get("description_fr", ""),
                    "wep_file_id": grip.get("wep_file_id", 0),
                    "grip_type": grip.get("grip_type", ""),
                    "str": grip.get("str", 0),
                    "int": grip.get("int", 0),
                    "agi": grip.get("agi", 0),
                    "dp": grip.get("dp"),
                    "pp": grip.get("pp"),
                    "compatible_weapons": grip.get("compatible_weapons", ""),
                    "blunt": grip.get("blunt", 0),
                    "edged": grip.get("edged", 0),
                    "piercing": grip.get("piercing", 0),
                    "gem_slots": grip.get("gem_slots", 0),
                },
            )

        # Localize grip names: field_name underscores → spaces
        conn.execute(sa.text("UPDATE grips SET name = REPLACE(field_name, '_', ' ')"))
        for field_name, display_name in GRIP_NAME_SPECIALS:
            conn.execute(
                sa.text("UPDATE grips SET name = :name WHERE field_name = :field_name"),
                {"name": display_name, "field_name": field_name},
            )

    # ── 3. Armor ──────────────────────────────────────────────────────
    if not _table_has_rows(conn, "armor"):
        armor_data = json.loads((DATA_DIR / "armors.json").read_text())
        for armor in armor_data:
            conn.execute(
                sa.text(
                    "INSERT INTO armor "
                    "(game_id, field_name, name, description_fr, wep_file_id, armor_type, "
                    '"str", "int", agi, gem_slots, '
                    "human, beast, undead, phantom, dragon, evil, "
                    "fire, water, wind, earth, light, dark, "
                    "blunt, edged, piercing, physical) "
                    "VALUES (:game_id, :field_name, :name, :description_fr, :wep_file_id, "
                    ":armor_type, :str, :int, :agi, :gem_slots, "
                    ":human, :beast, :undead, :phantom, :dragon, :evil, "
                    ":fire, :water, :wind, :earth, :light, :dark, "
                    ":blunt, :edged, :piercing, :physical)"
                ),
                {
                    "game_id": armor["id"],
                    "field_name": armor["field_name"],
                    "name": armor["name"],
                    "description_fr": armor.get("description_fr", ""),
                    "wep_file_id": armor.get("wep_file_id", 0),
                    "armor_type": armor["armor_type"],
                    "str": armor.get("str", 0),
                    "int": armor.get("int", 0),
                    "agi": armor.get("agi", 0),
                    "gem_slots": armor.get("gem_slots", 0),
                    "human": armor.get("human", 0),
                    "beast": armor.get("beast", 0),
                    "undead": armor.get("undead", 0),
                    "phantom": armor.get("phantom", 0),
                    "dragon": armor.get("dragon", 0),
                    "evil": armor.get("evil", 0),
                    "fire": armor.get("fire", 0),
                    "water": armor.get("water", 0),
                    "wind": armor.get("wind", 0),
                    "earth": armor.get("earth", 0),
                    "light": armor.get("light", 0),
                    "dark": armor.get("dark", 0),
                    "blunt": armor.get("blunt", 0),
                    "edged": armor.get("edged", 0),
                    "piercing": armor.get("piercing", 0),
                    "physical": armor.get("physical", 0),
                },
            )

        # Fix armor display names: field_name underscores → spaces (non-Shield)
        conn.execute(
            sa.text(
                "UPDATE armor SET name = REPLACE(field_name, '_', ' ') WHERE armor_type != 'Shield'"
            )
        )

        # Fix shield display names
        for field_name, display_name in SHIELD_NAME_FIXES:
            conn.execute(
                sa.text("UPDATE armor SET name = :name WHERE field_name = :field_name"),
                {"name": display_name, "field_name": field_name},
            )

        # Shields without special names: use field_name as-is (already single words)
        conn.execute(
            sa.text(
                "UPDATE armor SET name = field_name "
                "WHERE armor_type = 'Shield' AND name != REPLACE(field_name, '_', ' ')"
                "  AND field_name NOT IN ("
                "    'Spiked', 'Casserole', 'Heater', 'Oval', 'Knight', "
                "    'Hoplite', 'Jazeraint', 'Dread', 'Pelta', 'Quad', "
                "    'Circle', 'Tower', 'Round', 'Kite'"
                "  )"
            )
        )

        # Apply correct base stats
        for field_name, s, i, a in ARMOR_BASE_STATS:
            conn.execute(
                sa.text(
                    'UPDATE armor SET "str" = :s, "int" = :i, agi = :a '
                    "WHERE field_name = :field_name"
                ),
                {"s": s, "i": i, "a": a, "field_name": field_name},
            )

        # Zero out gem_slots for non-shield armor
        conn.execute(
            sa.text(
                "UPDATE armor SET gem_slots = 0 WHERE armor_type IN ('Helm', 'Body', 'Leg', 'Arm')"
            )
        )

    # ── 4. Gems ───────────────────────────────────────────────────────
    if not _table_has_rows(conn, "gems"):
        gems_data = json.loads((DATA_DIR / "gems.json").read_text())
        for gem in gems_data:
            conn.execute(
                sa.text(
                    "INSERT INTO gems "
                    "(game_id, field_name, name, description_fr, description, magnitude, "
                    'affinity_type, gem_type, "str", "int", agi, '
                    "human, beast, undead, phantom, dragon, evil, "
                    "physical, fire, water, wind, earth, light, dark) "
                    "VALUES (:game_id, :field_name, :name, :description_fr, :description, "
                    ":magnitude, :affinity_type, :gem_type, :str, :int, :agi, "
                    ":human, :beast, :undead, :phantom, :dragon, :evil, "
                    ":physical, :fire, :water, :wind, :earth, :light, :dark)"
                ),
                {
                    "game_id": gem["id"],
                    "field_name": gem["field_name"],
                    "name": gem["name"],
                    "description_fr": gem.get("description_fr", ""),
                    "description": gem.get("description", ""),
                    "magnitude": gem.get("magnitude", ""),
                    "affinity_type": gem.get("affinity_type", ""),
                    "gem_type": gem.get("gem_type", ""),
                    "str": gem.get("str", 0),
                    "int": gem.get("int", 0),
                    "agi": gem.get("agi", 0),
                    "human": gem.get("human", 0),
                    "beast": gem.get("beast", 0),
                    "undead": gem.get("undead", 0),
                    "phantom": gem.get("phantom", 0),
                    "dragon": gem.get("dragon", 0),
                    "evil": gem.get("evil", 0),
                    "physical": gem.get("physical", 0),
                    "fire": gem.get("fire", 0),
                    "water": gem.get("water", 0),
                    "wind": gem.get("wind", 0),
                    "earth": gem.get("earth", 0),
                    "light": gem.get("light", 0),
                    "dark": gem.get("dark", 0),
                },
            )

        # Localize gem names: field_name underscores → spaces
        conn.execute(sa.text("UPDATE gems SET name = REPLACE(field_name, '_', ' ')"))
        for field_name, display_name in GEM_NAME_SPECIALS:
            conn.execute(
                sa.text("UPDATE gems SET name = :name WHERE field_name = :field_name"),
                {"name": display_name, "field_name": field_name},
            )

    # ── 5. Materials ──────────────────────────────────────────────────
    if not _table_has_rows(conn, "materials"):
        materials_data = json.loads((DATA_DIR / "materials.json").read_text())
        for mat in materials_data:
            conn.execute(
                sa.text(
                    "INSERT INTO materials "
                    "(name, tier, str_modifier, int_modifier, agi_modifier, "
                    "human, beast, undead, phantom, dragon, evil, "
                    "fire, water, wind, earth, light, dark, "
                    "blade_str, blade_int, blade_agi, "
                    "shield_str, shield_int, shield_agi, "
                    "armor_str, armor_int, armor_agi) "
                    "VALUES (:name, :tier, :str_modifier, :int_modifier, :agi_modifier, "
                    ":human, :beast, :undead, :phantom, :dragon, :evil, "
                    ":fire, :water, :wind, :earth, :light, :dark, "
                    ":blade_str, :blade_int, :blade_agi, "
                    ":shield_str, :shield_int, :shield_agi, "
                    ":armor_str, :armor_int, :armor_agi)"
                ),
                {
                    "name": mat["name"],
                    "tier": mat["tier"],
                    "str_modifier": mat.get("str_modifier", 0),
                    "int_modifier": mat.get("int_modifier", 0),
                    "agi_modifier": mat.get("agi_modifier", 0),
                    "human": mat.get("human", 0),
                    "beast": mat.get("beast", 0),
                    "undead": mat.get("undead", 0),
                    "phantom": mat.get("phantom", 0),
                    "dragon": mat.get("dragon", 0),
                    "evil": mat.get("evil", 0),
                    "fire": mat.get("fire", 0),
                    "water": mat.get("water", 0),
                    "wind": mat.get("wind", 0),
                    "earth": mat.get("earth", 0),
                    "light": mat.get("light", 0),
                    "dark": mat.get("dark", 0),
                    # Defaults; updated below from MATERIAL_OFFSETS
                    "blade_str": 0,
                    "blade_int": 0,
                    "blade_agi": 0,
                    "shield_str": 0,
                    "shield_int": 0,
                    "shield_agi": 0,
                    "armor_str": 0,
                    "armor_int": 0,
                    "armor_agi": 0,
                },
            )

        # Apply material category offsets
        for name, b_s, b_i, b_a, s_s, s_i, s_a, a_s, a_i, a_a in MATERIAL_OFFSETS:
            conn.execute(
                sa.text(
                    "UPDATE materials SET "
                    "blade_str = :bs, blade_int = :bi, blade_agi = :ba, "
                    "shield_str = :ss, shield_int = :si, shield_agi = :sa, "
                    "armor_str = :as_, armor_int = :ai, armor_agi = :aa "
                    "WHERE name = :name"
                ),
                {
                    "name": name,
                    "bs": b_s,
                    "bi": b_i,
                    "ba": b_a,
                    "ss": s_s,
                    "si": s_i,
                    "sa": s_a,
                    "as_": a_s,
                    "ai": a_i,
                    "aa": a_a,
                },
            )

    # ── 6. Crafting recipes ───────────────────────────────────────────
    if not _table_has_rows(conn, "crafting_recipes"):
        recipes_data = json.loads((DATA_DIR / "crafting_recipes.json").read_text())
        for recipe in recipes_data:
            conn.execute(
                sa.text(
                    "INSERT INTO crafting_recipes "
                    "(category, sub_category, input_1, input_2, result, tier_change, has_swap) "
                    "VALUES (:category, :sub_category, :input_1, :input_2, :result, "
                    ":tier_change, :has_swap)"
                ),
                {
                    "category": recipe["category"],
                    "sub_category": recipe["sub_category"],
                    "input_1": recipe["input_1"],
                    "input_2": recipe["input_2"],
                    "result": recipe["result"],
                    "tier_change": recipe["tier_change"],
                    "has_swap": recipe["has_swap"],
                },
            )

    # ── 7. Material recipes ───────────────────────────────────────────
    if not _table_has_rows(conn, "material_recipes"):
        mat_recipes_data = json.loads((DATA_DIR / "material_recipes.json").read_text())
        for recipe in mat_recipes_data:
            conn.execute(
                sa.text(
                    "INSERT INTO material_recipes "
                    "(category, sub_category, input_1, input_2, material_1, material_2, "
                    "result_material, tier_change) "
                    "VALUES (:category, :sub_category, :input_1, :input_2, :material_1, "
                    ":material_2, :result_material, :tier_change)"
                ),
                {
                    "category": recipe["category"],
                    "sub_category": recipe["sub_category"],
                    "input_1": recipe["input_1"],
                    "input_2": recipe["input_2"],
                    "material_1": recipe["material_1"],
                    "material_2": recipe["material_2"],
                    "result_material": recipe["result_material"],
                    "tier_change": recipe["tier_change"],
                },
            )


def downgrade() -> None:
    """Remove all seeded core game data."""
    conn = op.get_bind()

    # Delete in reverse order (no FK dependencies between these tables)
    conn.execute(sa.text("DELETE FROM material_recipes"))
    conn.execute(sa.text("DELETE FROM crafting_recipes"))
    conn.execute(sa.text("DELETE FROM materials"))
    conn.execute(sa.text("DELETE FROM gems"))
    conn.execute(sa.text("DELETE FROM armor"))
    conn.execute(sa.text("DELETE FROM grips"))
    conn.execute(sa.text("DELETE FROM blades"))
