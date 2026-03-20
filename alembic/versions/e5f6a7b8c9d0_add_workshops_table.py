"""add workshops table

Revision ID: e5f6a7b8c9d0
Revises: b73583770546
Create Date: 2026-03-20 05:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e5f6a7b8c9d0"
down_revision: str | Sequence[str] | None = "b73583770546"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Data from workshops.txt
WORKSHOPS = [
    (
        "Work of Art",
        "Catacombs: Withered Spring",
        "Wood, Leather, Bronze",
        "The first workshop encountered. Limited to basic materials.",
    ),
    (
        "The Magic Hammer",
        "Town Center West: Rene Coast Road",
        "Bronze, Iron",
        "Second workshop with access to Iron-tier crafting.",
    ),
    (
        "Keane''s Crafts",
        "The Keep: The Warrior''s Rest",
        "Bronze, Iron, Hagane",
        "Mid-game workshop with Hagane material support.",
    ),
    (
        "Junction Point",
        "Town Center East: Rue Crimnade",
        "Wood, Leather, Bronze, Iron, Hagane",
        "Accessible after obtaining the Cattleya Sigil. Wide material range.",
    ),
    (
        "Metal Works",
        "Town Center East: Rue Fisserano",
        "Silver, Damascus",
        "Late-game workshop specializing in rare metals.",
    ),
    (
        "Godhands",
        "Undercity West: Bite The Master''s Wounds",
        "Wood, Leather, Bronze, Hagane, Silver, Damascus",
        "The ultimate workshop available only in New Game Plus. Supports all materials.",
    ),
]


def upgrade() -> None:
    """Create workshops table and populate with data."""
    op.create_table(
        "workshops",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("area", sa.String(length=200), server_default="", nullable=False),
        sa.Column(
            "available_materials",
            sa.String(length=300),
            server_default="",
            nullable=False,
        ),
        sa.Column("description", sa.Text(), server_default="", nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    for name, area, materials, description in WORKSHOPS:
        op.execute(
            f"INSERT INTO workshops (name, area, available_materials, description) "
            f"VALUES ('{name}', '{area}', '{materials}', '{description}')"
        )


def downgrade() -> None:
    """Drop workshops table."""
    op.drop_table("workshops")
