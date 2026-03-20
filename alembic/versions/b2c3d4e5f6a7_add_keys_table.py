"""add keys table

Revision ID: b2c3d4e5f6a7
Revises: b73583770546
Create Date: 2026-03-20 02:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b2c3d4e5f6a7"
down_revision: str | Sequence[str] | None = "b73583770546"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Cross-referenced from keys.txt and keys_2.txt
KEYS = [
    (
        "Bronze Key",
        "Snowfly Forest",
        "Return to the Land",
        "Earth Dragon",
        "Rue Morge (Town Center South), Shasras Hill Parks (Town Center East)",
    ),
    (
        "Iron Key",
        "Undercity East",
        "Weapons Not Allowed",
        "Chest",
        "Crossroads of Rest (Undercity West), Remembering Days of Yore (Undercity West), "
        "The Sunless Way (Undercity West), Bandits' Hallow (Abandoned Mines B2), "
        "From Squire to Knight (Town Walls North), Noble Gold and Silk (Undercity East)",
    ),
    (
        "Silver Key",
        "Temple of Kiltia",
        "Chapel of Meschaunce",
        "Chest",
        "Sewer of Ravenous Rats (Undercity West), Shelter From the Quake (Escapeway), "
        "Everwant Passage (Abandoned Mines B1), The Washing Woman's Way (Undercity West), "
        "The Auction Block (Limestone Quarry), Those Who Drink the Dark (Temple of Kiltia), "
        "The Resentful Ones (Temple of Kiltia)",
    ),
    (
        "Gold Key",
        "Undercity West",
        "Crumbling Market",
        "Chest",
        "The Timely Dew of Sleep (Limestone Quarry), Shelter from the Quake (Escapeway), "
        "Tears From Empty Sockets (Undercity West), Corner of Prayers (Undercity West), "
        "The Soldier's Bedding (Keep)",
    ),
    (
        "Platinum Key",
        "Snowfly Forest",
        "Nature's Womb",
        "Damascus Crab",
        "Implement (Iron Maiden B1)",
    ),
    (
        "Steel Key",
        "Forgotten Pathway",
        "The Fallen Knight",
        "Chest",
        "Hanging (Iron Maiden B1)",
    ),
    (
        "Crimson Key",
        "Town Center West",
        "Tircolas Flow",
        "Duane",
        "Rue Vermilion (Town Center West)",
    ),
    (
        "Chest Key",
        "Iron Maiden B1",
        "Spanish Tickler",
        "Wyvern Knight",
        "The Gallows (Wine Cellar), Hidden Resources (Abandoned Mines B2), "
        "The Branks (Iron Maiden B1), The Warrior's Rest (Keep)",
    ),
    (
        "Rood Inverse",
        "Beat the game",
        "",
        "Clear Game reward",
        "Train and Grow Strong (City Walls East), Glacialdra Kirk Ruins (Town Center West), "
        "Crossroads of Rest (Undercity West)",
    ),
]


def upgrade() -> None:
    """Create keys table and populate with data."""
    op.create_table(
        "keys",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("area", sa.String(length=100), server_default="", nullable=False),
        sa.Column("room", sa.String(length=100), server_default="", nullable=False),
        sa.Column("source", sa.String(length=200), server_default="", nullable=False),
        sa.Column("locations_used", sa.Text(), server_default="", nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    for name, area, room, source, locations_used in KEYS:
        safe_name = name.replace("'", "''")
        safe_area = area.replace("'", "''")
        safe_room = room.replace("'", "''")
        safe_source = source.replace("'", "''")
        safe_locations = locations_used.replace("'", "''")
        op.execute(
            f"INSERT INTO keys (name, area, room, source, locations_used) "
            f"VALUES ('{safe_name}', '{safe_area}', '{safe_room}', "
            f"'{safe_source}', '{safe_locations}')"
        )


def downgrade() -> None:
    """Drop keys table."""
    op.drop_table("keys")
