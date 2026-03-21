"""add chests and chest_items tables

Revision ID: f1a2b3c4d5e6
Revises: e6f7a8b9c0d1
Create Date: 2026-03-21 18:00:00.000000

"""

import re
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f1a2b3c4d5e6"
down_revision: str | Sequence[str] | None = "e6f7a8b9c0d1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Material code mapping
MATERIAL_MAP = {
    "B": "Bronze",
    "S": "Silver",
    "I": "Iron",
    "H": "Hagane",
    "D": "Damascus",
    "W": "Wood",
    "L": "Leather",
}

# Known consumable names (partial match patterns)
CONSUMABLES = {
    "Cure Root",
    "Cure Bulb",
    "Cure Potion",
    "Cure Tonic",
    "Vera Root",
    "Vera Bulb",
    "Vera Potion",
    "Vera Tonic",
    "Mana Root",
    "Mana Bulb",
    "Mana Potion",
    "Mana Tonic",
    "Spirit Orison",
    "Acolyte's Nostrum",
    "Saint's Nostrum",
    "Sorcerer's Reagent",
    "Alchemist's Reagent",
    "Yggdrasil's Tears",
    "Faerie Wing",
    "Eye of Argon",
    "Snowfly Drought",
    "Elixir of Queens",
    "Elixir of Kings",
    "Elixir of Sages",
    "Elixir of Mages",
    "Audentia",
    "Valens",
    "Prudens",
    "Virtus",
    "Volare",
}

# Known accessory names
ACCESSORIES = {
    "Salamander Ring",
    "Undine Bracelet",
    "Sylphid Ring",
    "Gnome Bracelet",
    "Titan's Ring",
    "Beaded Anklet",
    "Edgar's Earrings",
    "Diadra's Earring",
    "Kadesh Ring",
    "Agales's Chain",
    "Pushpaka",
}

# Known grip names (partial — ending patterns)
GRIP_NAMES = {
    "Wooden Grip",
    "Swept Hilt",
    "Cross Guard",
    "Sand Face",
    "Counter Guard",
    "Knuckle Guard",
    "Power Palm",
    "Heavy Grip",
    "Sarissa Grip",
    "Side Ring",
    "Gendarme",
    "Runkasyle",
    "Bhuj Type",
    "Spiculum Pole",
    "Framea Pole",
    "Spiral Pole",
    "Winged Pole",
    "Simple Bolt",
    "Steel Bolt",
    "Stone Bullet",
    "Sonic Bullet",
    "Falarica Bolt",
    "Ahlspies",
    "Elephant",
    "Grimoire Grip",
    "Dragonhead",
}

# Known shield names
SHIELD_NAMES = {
    "Buckler",
    "Targe",
    "Pelta Shield",
    "Quad Shield",
    "Circle Shield",
    "Tower Shield",
    "Spiked Shield",
    "Heater Shield",
    "Round Shield",
    "Kite Shield",
    "Casserole Shield",
    "Oval Shield",
    "Knight Shield",
    "Rondanche",
    "Hoplite Shield",
}

# Known armor names
ARMOR_NAMES = {
    "Leather Glove",
    "Reinforced Glove",
    "Knuckles",
    "Cuirass",
    "Long Boots",
    "Bear Mask",
    "Ring Mail",
    "Ring Leggings",
    "Ring Sleeve",
    "Chain Coif",
    "Chain Sleeve",
    "Chain Mail",
    "Breastplate",
    "Fusskampf",
    "Barbut",
    "Sallet",
    "Gauntlet",
    "Vambrace",
    "Brigandine",
    "Missaglia",
    "Plate Glove",
    "Burgonet",
    "Fluted Armor",
    "Fluted Glove",
    "Fluted Leggings",
    "Close Helm",
    "Plate Mail",
    "Hoplite Helm",
    "Hoplite Leggings",
    "Hoplite Glove",
    "Hoplite Armor",
    "Lionhead",
    "Ghost Hound",
}

# Known key names
KEY_NAMES = {
    "Silver Key",
    "Gold Key",
    "Iron Key",
    "Steel Key",
    "Chest Key",
}


def classify_item(name):
    """Determine item_type for a chest item by name."""
    if name.endswith(" Gem") or name in {
        "Braveheart Gem",
        "Haeralis Gem",
        "Iocus Gem",
        "Dragonite Gem",
        "White Queen Gem",
        "Undine Jasper Gem",
        "Manabreaker Gem",
        "Polaris Gem",
        "Salamander Ruby",
        "Nightkiller Gem",
        "Demonia Gem",
        "Speedster Gem",
        "Trinity Gem",
        "Hellraiser Gem",
        "Brainshield Gem",
        "Orion Gem",
        "Swan Song",
        "Dark Queen Gem",
        "Death Queen Gem",
        "Djinn Amber Gem",
        "Ifrit Carnelian Gem",
        "Marid Aquamarine Gem",
        "Dao Moonstone Gem",
        "Titan Malachite Gem",
        "Talos Feldspar Gem",
        "Morlock Jet Gem",
        "Angel Pearl Gem",
        "Sylphid Topaz Gem",
        "Balvus Gem",
        "Beowulf Gem",
        "Orlandu Gem",
        "Ogmius Gem",
        "Undine Jasper",
    }:
        return "gem"
    if name.startswith("Grimoire "):
        return "grimoire"
    if name.endswith(" Sigil"):
        return "sigil"
    if name in KEY_NAMES:
        return "key"
    if name in CONSUMABLES:
        return "consumable"
    if name in ACCESSORIES:
        return "accessory"
    # Check grip names (strip material/gem_slots for matching)
    base = re.sub(r"\[.*?\]", "", name).strip()
    if base in GRIP_NAMES:
        return "grip"
    if base in SHIELD_NAMES:
        return "shield"
    if base in ARMOR_NAMES:
        return "armor"
    return "blade"


def parse_item(raw):
    """Parse a raw item string into (name, material, gem_slots, quantity)."""
    raw = raw.strip()
    # Strip stray trailing ) that appears in some guide text (e.g. "Winged Pole[0])")
    if raw.endswith(")") and "(x" not in raw and "(" not in raw:
        raw = raw.rstrip(")")
    # Extract quantity: (x5)
    quantity = 1
    qty_match = re.search(r"\(x(\d+)\)$", raw)
    if qty_match:
        quantity = int(qty_match.group(1))
        raw = raw[: qty_match.start()].strip()

    # Extract bracket contents: [B], [B|1], [0], [1], [H|2]
    material = None
    gem_slots = None
    bracket_match = re.search(r"\[([^\]]*)\]$", raw)
    if bracket_match:
        bracket = bracket_match.group(1)
        raw = raw[: bracket_match.start()].strip()
        if "|" in bracket:
            parts = bracket.split("|")
            if parts[0] in MATERIAL_MAP:
                material = MATERIAL_MAP[parts[0]]
            gem_slots = int(parts[1])
        elif bracket in MATERIAL_MAP:
            material = MATERIAL_MAP[bracket]
        elif bracket.isdigit():
            gem_slots = int(bracket)

    # Strip grimoire spell name in parens: Grimoire Halte (Fixate) -> Grimoire Halte
    # But keep the (1) pattern for Grimoire Egout (1) etc as-is — those are odd
    if raw.startswith("Grimoire "):
        paren_match = re.search(r"\s*\([^)]+\)$", raw)
        if paren_match:
            raw = raw[: paren_match.start()].strip()

    name = raw.strip()
    return name, material, gem_slots, quantity


# ── Complete chest data from Spatvark Guide (GameFAQs) ──────────────
# Format: (area, room, lock_type, [items])
# Each item: raw string to parse

CHESTS = [
    # Wine Cellar
    (
        "Wine Cellar",
        "Worker's Breakroom",
        None,
        [
            "Hand Axe[B]",
            "Wooden Grip[0]",
            "Buckler[W|0]",
            "Leather Glove[L]",
            "Vera Bulb (x5)",
            "Cure Bulb (x5)",
        ],
    ),
    (
        "Wine Cellar",
        "The Reckoning Room",
        None,
        [
            "Gastraph Bow[B]",
            "Simple Bolt[0]",
            "Reinforced Glove[L]",
            "Vera Root (x3)",
            "Cure Root (x3)",
        ],
    ),
    (
        "Wine Cellar",
        "Blackmarket of Wines",
        None,
        [
            "Cure Potion",
            "Cure Bulb (x5)",
        ],
    ),
    (
        "Wine Cellar",
        "The Gallows",
        None,
        [
            "Pelta Shield[W|1]",
            "Vera Bulb (x3)",
            "Yggdrasil's Tears (x15)",
        ],
    ),
    (
        "Wine Cellar",
        "The Hero's Winehall",
        None,
        [
            "Spear[B]",
            "Spiculum Pole[1]",
            "Braveheart Gem",
            "Cure Bulb (x3)",
        ],
    ),
    (
        "Wine Cellar",
        "The Gallows",
        "Chest Key",
        [
            "Circle Shield[D|1]",
            "Titan Malachite Gem",
            "Cure Potion (x3)",
            "Vera Potion",
        ],
    ),
    # Catacombs
    (
        "Catacombs",
        "Rodent-Ridden Chamber",
        None,
        [
            "Goblin Club[I]",
            "Wooden Grip[0]",
            "Cross Guard[1]",
            "Cuirass[L]",
            "Long Boots[L]",
            "Iocus Gem",
            "Mana Root (x3)",
            "Cure Bulb (x3)",
        ],
    ),
    (
        "Catacombs",
        "The Lamenting Mother",
        None,
        [
            "Broad Sword[B]",
            "Swept Hilt[0]",
            "Knuckles[B]",
            "Elixir of Queens",
        ],
    ),
    (
        "Catacombs",
        "Bandits' Hideout",
        None,
        [
            "Scramasax[S]",
            "Swept Hilt[0]",
            "Targe[B|1]",
            "Knuckles[B]",
            "Bear Mask[L]",
            "Haeralis Gem",
            "Spirit Orison (x3)",
            "Eye of Argon (x3)",
        ],
    ),
    # Sanctum
    (
        "Sanctum",
        "Alchemists' Laboratory",
        None,
        [
            "Langdebeve[B]",
            "Sand Face[1]",
            "Dragonite Gem",
            "Grimoire Halte (Fixate)",
        ],
    ),
    # Abandoned Mines B1
    (
        "Abandoned Mines B1",
        "Miners' Resting Hall",
        "Unlock Spell",
        [
            "Guisarme[B]",
            "Sand Face[1]",
            "Quad Shield[B|1]",
            "Salamander Ruby",
            "Ring Mail[B]",
            "Ring Leggings[B]",
            "White Queen Gem",
            "Grimoire Visible (Eureka)",
            "Cure Bulb (x5)",
        ],
    ),
    (
        "Abandoned Mines B1",
        "Coal Mine Storage",
        None,
        [
            "Ring Sleeve[B]",
            "Chain Coif[B]",
            "Undine Jasper Gem",
            "Fern Sigil",
        ],
    ),
    (
        "Abandoned Mines B1",
        "Rust in Peace",
        "Unlock Spell",
        [
            "Chain Sleeve[B]",
            "Salamander Ring",
            "Manabreaker Gem",
            "Elixir of Sages",
            "Grimoire Undine (Frost Fusion)",
        ],
    ),
    (
        "Abandoned Mines B1",
        "Mining Regrets",
        None,
        [
            "Voulge[D]",
            "Winged Pole[0]",
            "Polaris Gem",
            "Mana Potion (x3)",
        ],
    ),
    # Abandoned Mines B2
    (
        "Abandoned Mines B2",
        "Delusions of Happiness",
        None,
        [
            "Sabre Halberd[H]",
            "Sarissa Grip[1]",
            "Kris[D]",
            "Heater Shield[I|2]",
            "Orion Gem",
            "Swan Song",
            "Vera Potion (x3)",
            "Grimoire Salamandre (Spark Fusion)",
        ],
    ),
    (
        "Abandoned Mines B2",
        "Hidden Resources",
        "Chest Key",
        [
            "Kudi[S]",
            "Knuckle Guard[2]",
            "Tower Shield[I|1]",
            "Breastplate[I]",
            "Fusskampf[H]",
            "Trinity Gem",
            "Saint's Nostrum (x3)",
            "Grimoire Mollesse (Restoration)",
        ],
    ),
    (
        "Abandoned Mines B2",
        "Acolyte's Burial Vault",
        None,
        [
            "Corcesca[H]",
            "Spiculum Pole[0]",
            "Framea Pole[2]",
            "Circle Shield[H|1]",
            "Brainshield Gem",
            "Gauntlet[H]",
            "Hellraiser Gem",
            "Grimoire Vie (Surging Balm)",
        ],
    ),
    (
        "Abandoned Mines B2",
        "Suicidal Desires",
        None,
        [
            "Footman's Mace[H]",
            "Sarissa Grip[1]",
            "Target Bow[I]",
            "Barbut[S]",
            "Gnome Bracelet",
            "Elixir of Queens",
            "Vera Bulb (x3)",
        ],
    ),
    # Limestone Quarry
    (
        "Limestone Quarry",
        "Bonds of Friendship",
        None,
        [
            "Schiavona[H]",
            "Counter Guard[1]",
            "Cranequin[I]",
            "Side Ring[2]",
            "Brigandine[H]",
            "Rondanche[H]",
            "Lionhead",
            "Snowfly Drought (x5)",
            "Grimoire Benir (Blessing)",
        ],
    ),
    (
        "Limestone Quarry",
        "Stone and Sulfurous Fire",
        None,
        [
            "Morning Star[H]",
            "Runkasyle[2]",
            "Balbriggan[B]",
            "Power Palm[3]",
            "Kite Shield[H|2]",
            "Talos Feldspar Gem",
            "Acolyte's Nostrum (x3)",
            "Grimoire Egout (Drain Heart)",
        ],
    ),
    (
        "Limestone Quarry",
        "Excavated Hollow",
        None,
        [
            "Brigandine[H]",
            "Heavy Grip[1]",
            "Elephant[3]",
            "Casserole Shield[H|2]",
            "Missaglia[I]",
            "Beaded Anklet",
            "Elixir of Queens",
            "Grimoire Flamme (Flame Sphere)",
        ],
    ),
    (
        "Limestone Quarry",
        "Drowned in Fleeting Joy",
        None,
        [
            "Falarica Bolt[1]",
            "Plate Glove[H]",
            "Elixir of Mages",
            "Mana Potion (x5)",
        ],
    ),
    (
        "Limestone Quarry",
        "Companions in Arms",
        "Unlock Spell",
        [
            "Executioner[D]",
            "Side Ring[2]",
            "Balvus Gem",
            "Beowulf Gem",
            "Spiral Pole[3]",
            "Casserole Shield[D|2]",
            "Orlandu Gem",
            "Ogmius Gem",
            "Close Helm[D]",
            "Plate Mail[D]",
            "Edgar's Earrings",
            "Grimoire Fleau (Avalanche)",
        ],
    ),
    # Temple of Kiltia
    (
        "Temple of Kiltia",
        "The Chapel of Meschaunce",
        None,
        [
            "Mjolnir[H]",
            "Runkasyle[2]",
            "Sonic Bullet[1]",
            "Ghost Hound",
            "Cure Potion (x2)",
            "Mana Potion (x2)",
            "Silver Key",
        ],
    ),
    # Great Cathedral L1
    (
        "Great Cathedral L1",
        "Where Darkness Spreads",
        None,
        [
            "Oval Shield[H|2]",
            "Morlock Jet Gem",
            "Burgonet[H]",
            "Mana Bulb (x5)",
            "Elixir of Queens",
        ],
    ),
    (
        "Great Cathedral L1",
        "The Flayed Confessional",
        None,
        [
            "Fluted Armor[H]",
            "Fluted Glove[H]",
            "Vera Potion (x3)",
            "Saint's Nostrum",
        ],
    ),
    # Great Cathedral L2
    (
        "Great Cathedral L2",
        "An Arrow into Darkness",
        None,
        [
            "Fluted Leggings[H]",
            "Fluted Glove[H]",
            "Eye of Argon (x5)",
            "Cure Potion",
        ],
    ),
    # Forgotten Pathway
    (
        "Forgotten Pathway",
        "The Fallen Knight",
        None,
        [
            "Kadesh Ring",
            "Orlandu Gem",
            "Elixir of Queens",
            "Steel Key",
        ],
    ),
    (
        "Forgotten Pathway",
        "Awaiting Retribution",
        None,
        [
            "Diadra's Earring",
            "Ogmius Gem",
            "Elixir of Queens",
        ],
    ),
    # Escapeway
    (
        "Escapeway",
        "Where Body and Soul Part",
        "Unlock Spell",
        [
            "Double Blade[S]",
            "Runkasyle[2]",
            "Vera Bulb (x5)",
            "Elixir of Mages",
        ],
    ),
    (
        "Escapeway",
        "Buried Alive",
        None,
        [
            "Bec de Corbin[D]",
            "Grimoire Grip[2]",
            "Grimoire Radius (Radial Surge)",
            "Grimoire Meteore (Meteor)",
        ],
    ),
    # Iron Maiden B1
    (
        "Iron Maiden B1",
        "The Wheel",
        "Unlock Spell",
        [
            "Griever[H]",
            "Bhuj Type[3]",
            "Baselard[H]",
            "Djinn Amber Gem",
            "Valens",
        ],
    ),
    (
        "Iron Maiden B1",
        "The Judas Cradle",
        None,
        [
            "Bastard Sword[H]",
            "Power Palm[3]",
            "Bullova[H]",
            "Ifrit Carnelian Gem",
            "Prudens",
        ],
    ),
    (
        "Iron Maiden B1",
        "The Ducking Stool",
        None,
        [
            "Khora[H]",
            "Power Palm[3]",
            "Pole Axe[H]",
            "Marid Aquamarine Gem",
            "Virtus",
        ],
    ),
    (
        "Iron Maiden B1",
        "The Branks",
        "Chest Key",
        [
            "Double Blade[H]",
            "Bhuj Type[3]",
            "Bec de Corbin[H]",
            "Dao Moonstone Gem",
            "Volare",
        ],
    ),
    # Iron Maiden B2
    (
        "Iron Maiden B2",
        "Lead Sprinkler",
        None,
        [
            "Hoplite Helm[H]",
            "Mana Potion (x3)",
        ],
    ),
    (
        "Iron Maiden B2",
        "Squassation",
        None,
        [
            "Hoplite Shield[H]",
            "Cure Potion (x3)",
        ],
    ),
    # Iron Maiden B3
    (
        "Iron Maiden B3",
        "Saint Elmo's Belt",
        None,
        [
            "Hoplite Leggings[H]",
            "Hoplite Glove[H]",
            "Elixir of Kings",
            "Elixir of Queens",
        ],
    ),
    (
        "Iron Maiden B3",
        "Dunking the Witch",
        None,
        [
            "Hoplite Armor[H]",
            "Hoplite Glove[H]",
            "Elixir of Kings",
            "Elixir of Queens",
        ],
    ),
    # Undercity West
    (
        "Undercity West",
        "The Children's Hideout",
        None,
        [
            "Shamshir[S]",
            "Knuckle Guard[2]",
            "Footman's Mace[H]",
            "Steel Bolt[1]",
            "Spiked Shield[I|1]",
            "White Queen Gem",
            "Sallet[H]",
            "Undine Bracelet",
            "Speedster Gem",
            "Grimoire Dissiper (Dispel)",
        ],
    ),
    (
        "Undercity West",
        "Larder for a Lean Winter",
        None,
        [
            "Tabar[H]",
            "Heavy Grip[1]",
            "Vambrace[H]",
            "Elixir of Sages",
            "Alchemist's Reagent (x5)",
            "Clematis Sigil",
        ],
    ),
    (
        "Undercity West",
        "The Crumbling Market",
        None,
        [
            "Agales's Chain",
            "Elixir of Queens",
            "Valens",
            "Gold Key",
        ],
    ),
    # Undercity East
    (
        "Undercity East",
        "Weapons Not Allowed",
        None,
        [
            "Falchion[B]",
            "Counter Guard[1]",
            "Stone Bullet[1]",
            "Titan's Ring",
            "Grimoire Nuageux (Psychodrain)",
            "Iron Key",
        ],
    ),
    (
        "Undercity East",
        "Sale of the Sword",
        None,
        [
            "Ahlspies[1]",
            "Pushpaka",
            "Grimoire Tardif (Leadbones)",
            "Stock Sigil",
        ],
    ),
    (
        "Undercity East",
        "Catspaw Blackmarket",
        None,
        [
            "Round Shield[H|2]",
            "Dark Queen Gem",
            "Grimoire Paralysie (Stun Cloud)",
            "Aster Sigil",
        ],
    ),
    # The Keep
    (
        "The Keep",
        "The Warrior's Rest",
        "Chest Key",
        [
            "Francisca[I]",
            "Gendarme[2]",
            "Tower Shield[I|1]",
            "Death Queen Gem",
            "Sallet[H]",
            "Sorcerer's Reagent (x3)",
        ],
    ),
    # Snowfly Forest
    (
        "Snowfly Forest",
        "Forest River",
        None,
        [
            "Knuckle Guard[2]",
            "Circle Shield[H|1]",
            "Djinn Amber Gem",
            "Chain Mail[1]",
            "Sylphid Ring",
            "Nightkiller Gem",
            "Acolyte's Nostrum (x3)",
            "Grimoire Agilite (Invigorate)",
        ],
    ),
    (
        "Snowfly Forest",
        "Hewn from Nature",
        None,
        [
            "Firangi[I]",
            "Cross Guard[1]",
            "Circle Shield[B|1]",
            "Sylphid Topaz Gem",
            "Demonia Gem",
            "Vera Tonic (x3)",
            "Cure Bulb (x3)",
        ],
    ),
    # Snowfly Forest East
    (
        "Snowfly Forest East",
        "Nature's Womb",
        None,
        [
            "Knight Shield[H|2]",
            "Djinn Amber Gem",
            "Acolyte's Nostrum (x3)",
        ],
    ),
    # Town Centre South
    (
        "Town Centre South",
        "The House Khazabas",
        "Unlock Spell",
        [
            "Eye of Argon (x10)",
            "Grimoire Muet (Silence)",
        ],
    ),
    # Town Centre East
    (
        "Town Centre East",
        "Gharmes Walk",
        "Chest Key",
        [
            "Falchion[S]",
            "Power Palm[3]",
            "Round Shield[S|2]",
            "Angel Pearl Gem",
            "Sorcerer's Reagent",
        ],
    ),
    (
        "Town Centre East",
        "The House Gilgitte",
        None,
        [
            "Khukuri[H]",
            "Power Palm[3]",
            "Dragonhead",
            "Faerie Wing (x5)",
            "Audentia",
        ],
    ),
]


def _esc(s):
    """Escape single quotes for SQL."""
    return s.replace("'", "''")


def upgrade() -> None:
    """Create chests and chest_items tables, populate with data."""
    op.create_table(
        "chests",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("area", sa.String(length=100), nullable=False),
        sa.Column("room", sa.String(length=200), nullable=False),
        sa.Column("lock_type", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "chest_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "chest_id",
            sa.Integer(),
            sa.ForeignKey("chests.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("item_type", sa.String(length=50), nullable=False),
        sa.Column("item_name", sa.String(length=200), nullable=False),
        sa.Column("material", sa.String(length=50), nullable=True),
        sa.Column("gem_slots", sa.Integer(), nullable=True),
        sa.Column("quantity", sa.Integer(), server_default="1", nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Get a connection for raw SQL
    conn = op.get_bind()

    for area, room, lock_type, raw_items in CHESTS:
        lock_sql = f"'{_esc(lock_type)}'" if lock_type else "NULL"
        conn.execute(
            sa.text(
                f"INSERT INTO chests (area, room, lock_type) "
                f"VALUES ('{_esc(area)}', '{_esc(room)}', {lock_sql})"
            )
        )
        result = conn.execute(sa.text("SELECT MAX(id) FROM chests"))
        chest_id = result.scalar()

        for raw in raw_items:
            name, material, gem_slots, quantity = parse_item(raw)
            item_type = classify_item(name)

            mat_sql = f"'{_esc(material)}'" if material else "NULL"
            gs_sql = str(gem_slots) if gem_slots is not None else "NULL"

            conn.execute(
                sa.text(
                    f"INSERT INTO chest_items "
                    f"(chest_id, item_type, item_name, material, gem_slots, quantity) "
                    f"VALUES ({chest_id}, '{_esc(item_type)}', '{_esc(name)}', "
                    f"{mat_sql}, {gs_sql}, {quantity})"
                )
            )


def downgrade() -> None:
    """Drop chest_items and chests tables."""
    op.drop_table("chest_items")
    op.drop_table("chests")
