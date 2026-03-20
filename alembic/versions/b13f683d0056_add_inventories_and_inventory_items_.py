"""add inventories and inventory_items tables

Revision ID: b13f683d0056
Revises: 36db0438bbf9
Create Date: 2026-03-20 14:36:34.898702

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b13f683d0056"
down_revision: str | Sequence[str] | None = "36db0438bbf9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "inventories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_inventories_user_id"), "inventories", ["user_id"], unique=False)
    op.create_table(
        "inventory_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("inventory_id", sa.Integer(), nullable=False),
        sa.Column("item_type", sa.String(length=50), nullable=False),
        sa.Column("item_id", sa.Integer(), nullable=False),
        sa.Column("material", sa.String(length=50), nullable=True),
        sa.Column("grip_id", sa.Integer(), nullable=True),
        sa.Column("gem_1_id", sa.Integer(), nullable=True),
        sa.Column("gem_2_id", sa.Integer(), nullable=True),
        sa.Column("gem_3_id", sa.Integer(), nullable=True),
        sa.Column("quantity", sa.Integer(), server_default="1", nullable=False),
        sa.ForeignKeyConstraint(["inventory_id"], ["inventories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("inventory_items")
    op.drop_index(op.f("ix_inventories_user_id"), table_name="inventories")
    op.drop_table("inventories")
