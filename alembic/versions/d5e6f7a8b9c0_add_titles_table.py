"""add titles table

Revision ID: d5e6f7a8b9c0
Revises: c4d5e6f7a8b9
Create Date: 2026-03-21 02:01:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d5e6f7a8b9c0"
down_revision: str | Sequence[str] | None = "c4d5e6f7a8b9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (number, name, requirement)
TITLES = [
    (1, "Seeker of Truth", "Finish the game once"),
    (2, "Conqueror of the Dark", "Finish the game within ten hours"),
    (3, "Treasure Hunter", "Check all the chests in the game"),
    (4, "Wanderer in Darkness", "Visit every map location in the game"),
    (5, "Destroyer of Gaeus", "Defeat Damascus Golem in Forgotten Passage"),
    (6, "Hunter of the Snowplains", "Defeat Damascus Crab in Snowfly Forest East"),
    (7, "Ally of the Wood", "Defeat Ravana in Iron Maiden B2"),
    (8, "Slayer of the Wyrm", "Defeat Dragon Zombie in Iron Maiden B2"),
    (9, "Vanquisher of Death", "Defeat Death and Ogre Zombie in Iron Maiden B2"),
    (10, "Warrior of Asura", "Defeat Asura in Iron Maiden B3"),
    (
        11,
        "Conqueror of Time",
        "Receive an ''Excellent!!'' rating for all Time Attack battles",
    ),
    (12, "Knight of Brilliance", "Turn out more than 30 Chain Abilities in a row"),
    (13, "Bearer of the New World", "Find the rare item Gold Key"),
    (14, "Hoard-Finder", "Find the rare item Chest Key"),
    (15, "Hands of Might", "Master all Break Arts"),
    (16, "Hands of Skill", "Master all Battle Abilities"),
    (17, "Wanderer of the Wyrding", "Finish the game without saving at any point"),
    (18, "Adventurer of Legend", "Finish the game without using Magic"),
    (19, "Lone Werreour", "Finish the game without using Battle Abilities"),
    (20, "Knight of Pride", "Finish the game without using Break Arts"),
    (21, "Blood-thirsty Hunter", "Defeat each class of monster 5,000 times"),
    (
        22,
        "Master of Arms",
        "Attack enemies 5,000 times with each type of weapon",
    ),
    (
        23,
        "Silent Assassin",
        "Attack over 500 times with a weapon in the Dagger group",
    ),
    (
        24,
        "Great Swordsman",
        "Attack over 500 times with a weapon in the Sword group",
    ),
    (
        25,
        "Master of Blades",
        "Attack over 500 times with a weapon in the Great Sword group",
    ),
    (
        26,
        "Steel Dragoon",
        "Attack over 500 times with a weapon in the Axe/Mace group",
    ),
    (
        27,
        "The Earthshaker",
        "Attack over 500 times with a weapon in the Great Axe group",
    ),
    (
        28,
        "Sweeper of the Dark",
        "Attack over 500 times with a weapon in the Staff group",
    ),
    (
        29,
        "Acolyte of Iron",
        "Attack over 500 times with a weapon in the Heavy Mace group",
    ),
    (
        30,
        "Spearsman of the Gale",
        "Attack over 500 times with a weapon in the Polearm group",
    ),
    (
        31,
        "Heaven''s Huntsman",
        "Attack over 500 times with a weapon in the Crossbow group",
    ),
    (32, "Master of Martial Artist", "Attack over 500 times with bare hands"),
]


def upgrade() -> None:
    """Create titles table and populate with data."""
    op.create_table(
        "titles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("requirement", sa.Text(), server_default="", nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    for number, name, requirement in TITLES:
        op.execute(
            f"INSERT INTO titles (number, name, requirement) "
            f"VALUES ({number}, '{name}', '{requirement}')"
        )


def downgrade() -> None:
    """Drop titles table."""
    op.drop_table("titles")
