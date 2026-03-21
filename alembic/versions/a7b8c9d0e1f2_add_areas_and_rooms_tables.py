"""add areas and rooms tables

Revision ID: a7b8c9d0e1f2
Revises: aa9dcf05f69f
Create Date: 2026-03-21 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a7b8c9d0e1f2"
down_revision: str | Sequence[str] | None = "aa9dcf05f69f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# ── Area and Room data ────────────────────────────────────────────
# Compiled from chests, grimoires, sigils, keys, and workshops.
# "Town Centre" normalized to "Town Center".

AREAS = [
    "Abandoned Mines B1",
    "Abandoned Mines B2",
    "Catacombs",
    "Escapeway",
    "Forgotten Pathway",
    "Great Cathedral B1",
    "Great Cathedral L1",
    "Great Cathedral L2",
    "Great Cathedral L3",
    "Iron Maiden B1",
    "Iron Maiden B2",
    "Iron Maiden B3",
    "Limestone Quarry",
    "Sanctum",
    "Snowfly Forest",
    "Snowfly Forest East",
    "Temple of Kiltia",
    "The Keep",
    "Town Center East",
    "Town Center South",
    "Town Center West",
    "Undercity East",
    "Undercity West",
    "Wine Cellar",
]

# (area_name, room_name) — every unique room from all data sources
ROOMS = [
    ("Abandoned Mines B1", "Battle's Beginning"),
    ("Abandoned Mines B1", "Coal Mine Storage"),
    ("Abandoned Mines B1", "Miners' Resting Hall"),
    ("Abandoned Mines B1", "Mining Regrets"),
    ("Abandoned Mines B1", "Rust in Peace"),
    ("Abandoned Mines B1", "The Battle's Beginning"),
    ("Abandoned Mines B1", "The Smeltry"),
    ("Abandoned Mines B1", "Traitor's Parting"),
    ("Abandoned Mines B2", "Acolyte's Burial Vault"),
    ("Abandoned Mines B2", "Delusions of Happiness"),
    ("Abandoned Mines B2", "Dining in Darkness"),
    ("Abandoned Mines B2", "Hidden Resources"),
    ("Abandoned Mines B2", "Suicidal Desires"),
    ("Abandoned Mines B2", "The Miner's End"),
    ("Abandoned Mines B2", "Tomb of the Reborn"),
    ("Catacombs", "Bandits' Hideout"),
    ("Catacombs", "Beast's Domain"),
    ("Catacombs", "Rodent-Ridden Chamber"),
    ("Catacombs", "The Beast's Domain"),
    ("Catacombs", "The Lamenting Mother"),
    ("Catacombs", "The Withered Spring"),
    ("Catacombs", "Withered Spring"),
    ("Escapeway", "Buried Alive"),
    ("Escapeway", "Fear and Loathing"),
    ("Escapeway", "Where Body and Soul Part"),
    ("Forgotten Pathway", "Awaiting Retribution"),
    ("Forgotten Pathway", "The Fallen Knight"),
    ("Great Cathedral B1", "Order and Chaos"),
    ("Great Cathedral B1", "Truth and Lies"),
    ("Great Cathedral L1", "A Light in the Dark"),
    ("Great Cathedral L1", "Monk's Leap"),
    ("Great Cathedral L1", "The Flayed Confessional"),
    ("Great Cathedral L1", "Where Darkness Spreads"),
    ("Great Cathedral L2", "An Arrow into Darkness"),
    ("Great Cathedral L2", "Hall of Broken Vows"),
    ("Great Cathedral L2", "Maelstrom of Malice"),
    ("Great Cathedral L2", "What Ails You, Kills You"),
    ("Great Cathedral L3", "Hopes of the Idealist"),
    ("Iron Maiden B1", "Burial"),
    ("Iron Maiden B1", "Knotting"),
    ("Iron Maiden B1", "Spanish Tickler"),
    ("Iron Maiden B1", "Starvation"),
    ("Iron Maiden B1", "The Branks"),
    ("Iron Maiden B1", "The Cauldron"),
    ("Iron Maiden B1", "The Ducking Stool"),
    ("Iron Maiden B1", "The Judas Cradle"),
    ("Iron Maiden B1", "The Wheel"),
    ("Iron Maiden B2", "Lead Sprinkler"),
    ("Iron Maiden B2", "Ordeal by Fire"),
    ("Iron Maiden B2", "Pressing"),
    ("Iron Maiden B2", "Squassation"),
    ("Iron Maiden B2", "The Saw"),
    ("Iron Maiden B2", "The Shin-Vice"),
    ("Iron Maiden B3", "Dunking the Witch"),
    ("Iron Maiden B3", "Saint Elmo's Belt"),
    ("Iron Maiden B3", "The Iron Maiden"),
    ("Limestone Quarry", "Bonds of Friendship"),
    ("Limestone Quarry", "Companions in Arms"),
    ("Limestone Quarry", "Dream of the Holy Land"),
    ("Limestone Quarry", "Drowned in Fleeting Joy"),
    ("Limestone Quarry", "Excavated Hollow"),
    ("Limestone Quarry", "Hall of the Wage-Paying"),
    ("Limestone Quarry", "Stone and Sulfurous Fire"),
    ("Sanctum", "Alchemists' Laboratory"),
    ("Sanctum", "Hall of Sacrilege"),
    ("Sanctum", "The Cleansing Chantry"),
    ("Sanctum", "Theology Classroom"),
    ("Snowfly Forest", "Forest River"),
    ("Snowfly Forest", "Hewn from Nature"),
    ("Snowfly Forest", "Nature's Womb"),
    ("Snowfly Forest", "Return to the Land"),
    ("Snowfly Forest East", "Nature's Womb"),
    ("Temple of Kiltia", "Chapel of Meschaunce"),
    ("Temple of Kiltia", "Hall of Prayer"),
    ("Temple of Kiltia", "The Chapel of Meschaunce"),
    ("Temple of Kiltia", "Those who Fear the Light"),
    ("The Keep", "The Warrior's Rest"),
    ("Town Center East", "Gharmes Walk"),
    ("Town Center East", "Rue Crimnade"),
    ("Town Center East", "Rue Fisserano"),
    ("Town Center East", "The House Gilgitte"),
    ("Town Center South", "The House Khazabas"),
    ("Town Center West", "Rene Coast Road"),
    ("Town Center West", "Tircolas Flow"),
    ("Undercity East", "Arms Against Invaders"),
    ("Undercity East", "Bazaar of the Bizarre"),
    ("Undercity East", "Catspaw Blackmarket"),
    ("Undercity East", "Gemsword Blackmarket"),
    ("Undercity East", "Place of Free Words"),
    ("Undercity East", "Sale of the Sword"),
    ("Undercity East", "Weapons Not Allowed"),
    ("Undercity East", "Where Black Waters Ran"),
    ("Undercity West", "Bite The Master's Wounds"),
    ("Undercity West", "Corner of Prayers"),
    ("Undercity West", "Crumbling Market"),
    ("Undercity West", "Fear of the Fall"),
    ("Undercity West", "Larder for a Lean Winter"),
    ("Undercity West", "Nameless Dark Oblivion"),
    ("Undercity West", "Remembering Days of Yore"),
    ("Undercity West", "Sewer of Ravenous Rats"),
    ("Undercity West", "Sinner's Corner"),
    ("Undercity West", "The Children's Hideout"),
    ("Undercity West", "The Crumbling Market"),
    ("Undercity West", "The Washing-Woman's Way"),
    ("Undercity West", "Underdark Fishmarket"),
    ("Wine Cellar", "Blackmarket of Wines"),
    ("Wine Cellar", "Gallows"),
    ("Wine Cellar", "The Gallows"),
    ("Wine Cellar", "The Hero's Winehall"),
    ("Wine Cellar", "The Reckoning Room"),
    ("Wine Cellar", "Worker's Breakroom"),
]

# Normalization map: old area string -> normalized area name
# Used when matching existing table rows to area records
AREA_NORMALIZE = {
    "Town Centre South": "Town Center South",
    "Town Centre East": "Town Center East",
    "Town Centre West": "Town Center West",
}


def _esc(s):
    """Escape single quotes for SQL."""
    return s.replace("'", "''")


def upgrade() -> None:
    """Create areas and rooms tables, populate, add room_id to existing tables."""
    conn = op.get_bind()

    # ── Step 1: Create areas table ────────────────────────────────
    op.create_table(
        "areas",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # ── Step 2: Create rooms table ────────────────────────────────
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "area_id",
            sa.Integer(),
            sa.ForeignKey("areas.id"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # ── Step 3: Insert areas ──────────────────────────────────────
    for area_name in AREAS:
        conn.execute(sa.text(f"INSERT INTO areas (name) VALUES ('{_esc(area_name)}')"))

    # ── Step 4: Insert rooms ──────────────────────────────────────
    for area_name, room_name in ROOMS:
        conn.execute(
            sa.text(
                f"INSERT INTO rooms (area_id, name) "
                f"SELECT id, '{_esc(room_name)}' FROM areas "
                f"WHERE name = '{_esc(area_name)}'"
            )
        )

    # ── Step 5: Add room_id columns to existing tables ────────────
    op.add_column(
        "chests",
        sa.Column("room_id", sa.Integer(), sa.ForeignKey("rooms.id"), nullable=True),
    )
    op.add_column(
        "grimoires",
        sa.Column("room_id", sa.Integer(), sa.ForeignKey("rooms.id"), nullable=True),
    )
    op.add_column(
        "sigils",
        sa.Column("room_id", sa.Integer(), sa.ForeignKey("rooms.id"), nullable=True),
    )
    op.add_column(
        "keys",
        sa.Column("room_id", sa.Integer(), sa.ForeignKey("rooms.id"), nullable=True),
    )
    op.add_column(
        "workshops",
        sa.Column("room_id", sa.Integer(), sa.ForeignKey("rooms.id"), nullable=True),
    )

    # ── Step 6: Populate room_id for chests ───────────────────────
    # Chests use "Town Centre" in DB, normalize to "Town Center"
    conn.execute(
        sa.text(
            """
            UPDATE chests SET room_id = r.id
            FROM rooms r
            JOIN areas a ON r.area_id = a.id
            WHERE a.name = REPLACE(REPLACE(chests.area,
                'Town Centre South', 'Town Center South'),
                'Town Centre East', 'Town Center East')
            AND r.name = chests.room
            """
        )
    )

    # ── Step 7: Populate room_id for grimoires ────────────────────
    # Grimoire area strings use "Town Center" (already normalized) and
    # room strings with escaped apostrophes like "The Beast''s Domain"
    # in the migration data, but actual DB stores them unescaped.
    conn.execute(
        sa.text(
            """
            UPDATE grimoires SET room_id = r.id
            FROM rooms r
            JOIN areas a ON r.area_id = a.id
            WHERE a.name = grimoires.area
            AND r.name = grimoires.room
            """
        )
    )

    # ── Step 8: Populate room_id for sigils ───────────────────────
    conn.execute(
        sa.text(
            """
            UPDATE sigils SET room_id = r.id
            FROM rooms r
            JOIN areas a ON r.area_id = a.id
            WHERE a.name = sigils.area
            AND r.name = sigils.room
            """
        )
    )

    # ── Step 9: Populate room_id for keys ─────────────────────────
    # Keys have area/room strings; some keys have non-room areas like
    # "Beat the game" — those will remain NULL.
    conn.execute(
        sa.text(
            """
            UPDATE keys SET room_id = r.id
            FROM rooms r
            JOIN areas a ON r.area_id = a.id
            WHERE a.name = keys.area
            AND r.name = keys.room
            """
        )
    )

    # ── Step 10: Populate room_id for workshops ───────────────────
    # Workshop area format is "Area: Room" — need to split and match.
    # We update each workshop by matching the split values.
    conn.execute(
        sa.text(
            """
            UPDATE workshops SET room_id = r.id
            FROM rooms r
            JOIN areas a ON r.area_id = a.id
            WHERE workshops.area LIKE '%: %'
            AND a.name = TRIM(SPLIT_PART(workshops.area, ': ', 1))
            AND r.name = TRIM(SPLIT_PART(workshops.area, ': ', 2))
            """
        )
    )


def downgrade() -> None:
    """Remove room_id columns and drop areas/rooms tables."""
    op.drop_column("workshops", "room_id")
    op.drop_column("keys", "room_id")
    op.drop_column("sigils", "room_id")
    op.drop_column("grimoires", "room_id")
    op.drop_column("chests", "room_id")
    op.drop_table("rooms")
    op.drop_table("areas")
