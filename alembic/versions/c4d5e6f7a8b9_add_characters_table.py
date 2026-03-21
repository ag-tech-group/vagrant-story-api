"""add characters table

Revision ID: c4d5e6f7a8b9
Revises: b3c4d5e6f7a8
Create Date: 2026-03-21 02:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c4d5e6f7a8b9"
down_revision: str | Sequence[str] | None = "b3c4d5e6f7a8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (name, role, description)
CHARACTERS = [
    # Main Characters
    (
        "Ashley Riot",
        "Protagonist, VKP Riskbreaker",
        "A member of the Valendia Knights of the Peace on a mission to pursue Sydney Losstarot.",
    ),
    (
        "Sydney Losstarot",
        "Antagonist, Mullenkamp Leader",
        "Inheritor of the bloodline of the Priestess Mullenkamp, leader of the revival of her religion.",
    ),
    (
        "Callo Merlose",
        "VKP Inquisitor",
        "Ashley''s partner in the Lea Monde incident, a VKP Inquisitor agent. Becomes Sydney''s hostage.",
    ),
    (
        "Romeo Guildenstern",
        "Crimson Blades Commander",
        "Commander of the Crimson Blades, the knightly order of the Iocus priesthood.",
    ),
    (
        "John Hardin",
        "Mullenkamp Second-in-Command",
        "Sydney''s faithful servant, aids in leading Mullenkamp and setting up Sigils.",
    ),
    (
        "Jan Rosencrantz",
        "Mercenary",
        "Red-clad swashbuckler, an immoral mercenary immune to the Dark with no allegiance.",
    ),
    (
        "Lady Samantha",
        "Crimson Blades Knight",
        "Romeo''s faithful companion, the only one who shows worry for the loss of troops.",
    ),
    (
        "Duke Bardorba",
        "Political Figure",
        "Hero of the Valendian Civil War and influential political figure controlling many events.",
    ),
    # Supporting Characters
    (
        "Father Duane",
        "Crimson Blades Captain",
        "One of the first Blades to fall. His death drives his brother Grissom to revenge.",
    ),
    (
        "Father Grissom",
        "Crimson Blades Commander",
        "Brother of Duane, a polished cleric hiding ruthlessness behind elegant niceties.",
    ),
    (
        "Sir Tieger",
        "Crimson Blades Knight",
        "Shown only with Lady Neesa. Gives up his life so she may tell the tale.",
    ),
    (
        "Lady Neesa",
        "Crimson Blades Knight",
        "Close associate of Sir Tieger, a hardened warrior.",
    ),
    (
        "Inquisitor Heldricht",
        "VKP Head Inquisitor",
        "Supervises VKP Inquisitors. Terse and direct with her pageboy cut and thin cigars.",
    ),
    (
        "Steward LeSait",
        "VKP Commander",
        "Commander of the Valendia Knights of the Peace.",
    ),
    (
        "Cardinal Batistum",
        "Religious Leader",
        "Powerful figure in Valendia''s religion, commands the Crimson Blades.",
    ),
    # Minor Characters
    (
        "Mandel",
        "Crimson Blades",
        "Killed by Ashley, reanimated as undead by the Dark.",
    ),
    (
        "Goodwin",
        "Crimson Blades",
        "Trapped in the Wine Cellar, teaches Ashley about Cloudstones.",
    ),
    (
        "Sackheim",
        "Crimson Blades",
        "Trapped in the Wine Cellar with Goodwin.",
    ),
    (
        "Bejart",
        "Crimson Blades",
        "Footsoldier slain by Ashley in the Town Center.",
    ),
    (
        "Sarjik",
        "Crimson Blades",
        "Footsoldier slain by Ashley in the Town Center.",
    ),
    (
        "Faendos",
        "Crimson Blades",
        "Accompanies Grissom into Snowfly Forest, disappears.",
    ),
    (
        "Lamkin",
        "Crimson Blades",
        "Accompanies Grissom into Snowfly Forest, disappears.",
    ),
]


def upgrade() -> None:
    """Create characters table and populate with data."""
    op.create_table(
        "characters",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("role", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), server_default="", nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    for name, role, description in CHARACTERS:
        op.execute(
            f"INSERT INTO characters (name, role, description) "
            f"VALUES ('{name}', '{role}', '{description}')"
        )


def downgrade() -> None:
    """Drop characters table."""
    op.drop_table("characters")
