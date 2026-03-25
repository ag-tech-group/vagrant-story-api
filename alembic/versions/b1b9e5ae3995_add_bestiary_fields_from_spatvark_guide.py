"""add bestiary fields from spatvark guide

Revision ID: b1b9e5ae3995
Revises: g1h2i3j4k5l6
Create Date: 2026-03-24 23:31:14.621163

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b1b9e5ae3995"
down_revision: str | Sequence[str] | None = "g1h2i3j4k5l6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add new bestiary fields from Spatvark's guide."""
    # Enemy table: add encyclopaedia_number, description, movement, is_boss
    op.add_column(
        "enemies",
        sa.Column("encyclopaedia_number", sa.Integer(), nullable=True),
    )
    op.add_column(
        "enemies",
        sa.Column(
            "description",
            sa.String(length=500),
            nullable=False,
            server_default="",
        ),
    )
    op.add_column(
        "enemies",
        sa.Column("movement", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "enemies",
        sa.Column("is_boss", sa.Boolean(), nullable=False, server_default="0"),
    )

    # EnemyBodyPart table: add evade, chain_evade
    op.add_column(
        "enemy_body_parts",
        sa.Column("evade", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "enemy_body_parts",
        sa.Column("chain_evade", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    """Remove bestiary fields added from Spatvark's guide."""
    op.drop_column("enemy_body_parts", "chain_evade")
    op.drop_column("enemy_body_parts", "evade")
    op.drop_column("enemies", "is_boss")
    op.drop_column("enemies", "movement")
    op.drop_column("enemies", "description")
    op.drop_column("enemies", "encyclopaedia_number")
