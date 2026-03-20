"""add sigils table

Revision ID: c3d4e5f6a7b8
Revises: b73583770546
Create Date: 2026-03-20 03:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c3d4e5f6a7b8"
down_revision: str | Sequence[str] | None = "b73583770546"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Cross-referenced from sigils.txt and sigils_2.txt
SIGILS = [
    (
        "Acacia Sigil",
        "Great Cathedral L1",
        "A Light in the Dark",
        "Arch Dragon",
        "Hall of Broken Vows (Great Cathedral L2)",
    ),
    (
        "Anemone Sigil",
        "Iron Maiden B1",
        "Knotting",
        "Wyvern Queen",
        "Urge the Boy On (The Keep)",
    ),
    (
        "Aster Sigil",
        "Undercity East",
        "Catspaw Blackmarket",
        "Chest",
        "Dream of the Holy Land (Limestone Quarry)",
    ),
    (
        "Azalea Sigil",
        "Iron Maiden B2",
        "The Shin-Vice",
        "Ogre Zombie",
        "Wiping Blood from Blades (The Keep)",
    ),
    (
        "Calla Sigil",
        "Great Cathedral L2",
        "Hall of Broken Vows",
        "Flame Dragon",
        "Heretic''s Story (Great Cathedral L3)",
    ),
    (
        "Cattleya Sigil",
        "Undercity West",
        "Fear of the Fall",
        "Dark Elemental",
        "Rue Crimnade (Town Center East)",
    ),
    (
        "Chamomile Sigil",
        "Wine Cellar",
        "Gallows",
        "Minotaur",
        "Smokebarrel Stair (Wine Cellar)",
    ),
    (
        "Clematis Sigil",
        "Undercity West",
        "Larder for a Lean Winter",
        "Chest",
        "Dream of the Holy Land (Limestone Quarry)",
    ),
    (
        "Columbine Sigil",
        "Iron Maiden B1",
        "Burial",
        "Iron Golem",
        "A Storm of Arrows (The Keep)",
    ),
    (
        "Eulalia Sigil",
        "Undercity East",
        "Bazaar of the Bizarre",
        "Lich",
        "The Dreamer''s Climb (Limestone Quarry)",
    ),
    (
        "Fern Sigil",
        "Abandoned Mines B1",
        "Coal Mine Storage",
        "Chest",
        "Live Long and Prosper (Abandoned Mines B1)",
    ),
    (
        "Hyacinth Sigil",
        "Abandoned Mines B1",
        "Battle''s Beginning",
        "Wyvern",
        "Earthquake''s Mark (Abandoned Mines B1)",
    ),
    (
        "Kalmia Sigil",
        "Iron Maiden B1",
        "Starvation",
        "Wraith",
        "A Storm of Arrows (The Keep)",
    ),
    (
        "Laurel Sigil",
        "Great Cathedral L1",
        "Monk''s Leap",
        "Lich",
        "Poisoned Chapel (Great Cathedral L1)",
    ),
    (
        "Lily Sigil",
        "Catacombs",
        "Beast''s Domain",
        "Lizardman",
        "Withered Spring (Catacombs)",
    ),
    (
        "Mandrake Sigil",
        "Iron Maiden B1",
        "The Cauldron",
        "Wraith",
        "Rue Aliano (Town Center South)",
    ),
    (
        "Marigold Sigil",
        "Iron Maiden B2",
        "The Saw",
        "Dragon Zombie",
        "A Taste of the Spoils (The Keep)",
    ),
    (
        "Melissa Sigil",
        "Undercity East",
        "Gemsword Blackmarket",
        "Nightstalker",
        "The Laborer''s Bonfire (Limestone Quarry)",
    ),
    (
        "Palm Sigil",
        "Great Cathedral L3",
        "Hopes of the Idealist",
        "Dao",
        "Melodies of Madness (Great Cathedral L2)",
    ),
    (
        "Schirra Sigil",
        "Iron Maiden B2",
        "Pressing",
        "Ravana",
        "A Taste of the Spoils (The Keep)",
    ),
    (
        "Stock Sigil",
        "Undercity East",
        "Sale of the Sword",
        "Chest",
        "Blackmarket of Wines (Wine Cellar)",
    ),
    (
        "Tearose Sigil",
        "Abandoned Mines B2",
        "Dining in Darkness",
        "Sky Dragon",
        "The Cauldron (Iron Maiden B1)",
    ),
    (
        "Tigertail Sigil",
        "Iron Maiden B3",
        "The Iron Maiden",
        "Asura",
        "Wiping Blood from Blades (The Keep)",
    ),
    (
        "Verbena Sigil",
        "Iron Maiden B2",
        "Ordeal by Fire",
        "Dark Dragon",
        "Urge the Boy On (The Keep)",
    ),
]


def upgrade() -> None:
    """Create sigils table and populate with data."""
    op.create_table(
        "sigils",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("area", sa.String(length=100), server_default="", nullable=False),
        sa.Column("room", sa.String(length=100), server_default="", nullable=False),
        sa.Column("source", sa.String(length=200), server_default="", nullable=False),
        sa.Column("door_unlocks", sa.Text(), server_default="", nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    for name, area, room, source, door_unlocks in SIGILS:
        op.execute(
            f"INSERT INTO sigils (name, area, room, source, door_unlocks) "
            f"VALUES ('{name}', '{area}', '{room}', '{source}', '{door_unlocks}')"
        )


def downgrade() -> None:
    """Drop sigils table."""
    op.drop_table("sigils")
